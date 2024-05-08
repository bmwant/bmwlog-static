---
title: FastAPI middleware
tags: [python, fastapi, middleware, web, framework]
author: Misha Behersky
language: en
date: 2024-05-08 12:37:36
---

> **NOTE**: Python `3.11.9` and FastAPI `0.111.0` is used throughout this article.

Creating middleware within [FastAPI](https://fastapi.tiangolo.com/) framework is really simple: you just create a regular handler with extra `call_next` parameter and decorate it with `@app.middleware("http")`.

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.monotonic()
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    response.headers["X-Took"] = str(process_time)
    return response
```

Then you make sure to invoke rest of the processing chain by calling `await call_next(request)` and return `response` and the very end.

On the other hand, when it comes to something more complex like transforming existing body or modifying immutable headers, it's not that straightforward to do.

Usage of such a middleware is still simple, so in case you want to add automatic redirect to _https_ endpoints you can use provided [HTTPSRedirectMiddleware](https://fastapi.tiangolo.com/advanced/middleware/#httpsredirectmiddleware) one:

```python
app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
```

But writing your own sophisticated middleware is a bit trickier.

### Modifying request body

Let's imagine that we want to strip all the whitespace characters within the payload body we send to our server. First we would create a simple helper function which recursively modifies input data in place.

```python
def strip_whitespace(data: Any) -> Any:
    if isinstance(data, str):
        return data.strip()
    elif isinstance(data, dict):
        return {k: strip_whitespace(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [strip_whitespace(item) for item in data]

    return data
```

Just to be clear: you should use [Pydantic](https://fastapi.tiangolo.com/tutorial/body/#create-your-data-model) models in order to coerce/validate the data you pass to the handlers, so this is just an illustrative example here.

To define middleware you need to create a class that accepts [ASGI](https://asgi.readthedocs.io/en/latest/) app and make it callable by implementing `async def __call__(self, scope: Scope, receive: Receive, send: Send)` method

```python
from starlette.types import ASGIApp, Message, Receive, Scope, Send

PAYLOAD_METHODS = ["PUT", "POST", "PATCH"]

class WhitespaceStripMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or scope["method"] not in PAYLOAD_METHODS:
            await self.app(scope, receive, send)
            return

        async def update_body() -> Message:
            message = await receive()
            assert message["type"] == "http.request"

            try:
                body: bytes = message["body"].decode()
                json_body = json.loads(body)
            except (UnicodeDecodeError, json.JSONDecodeError):
                return message

            json_stripped = strip_whitespace(json_body)
            message["body"] = json.dumps(json_stripped).encode()
            return message

        await self.app(scope, update_body, send)
```

Note that we are also using [Starlette](https://www.starlette.io/) types here as FastAPI itself is based on the Starlette framework and heavily use its toolkit.

Main part here is `update_body` closure (just to simplify access to `receive` function, but it can be a method or a separate function as well).

```python
body: bytes = message["body"].decode()
json_body = json.loads(body)
```

We load json payload from our request first

```python
json_stripped = strip_whitespace(json_body)
message["body"] = json.dumps(json_stripped).encode()
```

and then transform it using previously implemented helper function. All of the downstreamed middleware alongside with route handlers will receive request containing our adjusted payload.

### Modifying response body

Now let's check even more complex middleware where we need to both modify response body and adjust response headers accordingly to the changes made.

We start by defining a similar middleware class which accepts app and has `__call__` method on it

```python
class ListWrapMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            responder = ListWrapResponder(self.app)
            await responder(scope, receive, send)
            return
        await self.app(scope, receive, send)
```

Here instead of having all the logic defined within middleware class we offload processing to a custom responder

```python
from starlette.datastructures import MutableHeaders

class ListWrapResponder:
    def __init__(self, app):
        self.app = app
        self.initial_message = {}

    async def __call__(self, scope, receive, send):
        self.send = send
        await self.app(scope, receive, self.wrap_data)

    async def wrap_data(self, message):
        message_type = message["type"]
        if message_type == "http.response.start":
            self.initial_message = message

        elif message_type == "http.response.body":
            try:
                body = message["body"].decode()
                json_body = json.loads(body)
            except (UnicodeDecodeError, json.JSONDecodeError):
                json_body = None

            if isinstance(json_body, list):
                data = {
                    "total": len(json_body),
                    "items": json_body,
                }
                new_body = json.dumps(data).encode()
                headers = MutableHeaders(raw=self.initial_message["headers"])
                headers["Content-Length"] = str(len(new_body))
                message["body"] = new_body

            await self.send(self.initial_message)
            await self.send(message)
```

First, we preserve the initial message and wait for the `response.body` message to come. Then we load json body the same way we did before and do any tranformation required. In the example above we wrap response into the nested stucture that count total elements in case of an array and add `total` property to it. The list itself is returned under the `items` property.

After that, we create headers structure that is allowed to be mutated and change [Content-Length](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Length) header to reflect that our data have been updated.

Finally, we send initial saved `response.start` part and our modified body back to the client (or to the any other middleware down the line).

To make sure that transformation are a part of request/response cycle we need to install it on the app.

```python
app.add_middleware(WhitespaceStripMiddleware)
app.add_middleware(ListWrapMiddleware)
```

### Running webserver

For the validation we are going to add a simple handler that echoes back the json payload being sent

```python
@app.post("/data")
async def handle_data(request: Request):
    payload = await request.json()
    return payload
```

Then, assuming you have just single `main.py` file for the webserver code you can run it as

```bash
fastapi dev
```

Triggering the request using curl should pass the data though our middleware and return modified structure with all the string values stripped.

```bash
curl -X POST -H "Content-Type: application/json" \
    http://127.0.0.1:8000/data \
    --data '[" one ", " two ", {"nested": "  three  "}]'
```

Response in your terminal for the request above should look like this

```json
{ "total": 3, "items": ["one", "two", { "nested": "three" }] }
```

As you can see we received data back wrapped into object with extra information and all of the values were subjects of leading/trailing whitespace removal.

At this point you should be able to implement any of the middleware logic in your app using the approach described. But before trying to invent anything, check this [repository](https://github.com/florimondmanca/awesome-asgi) which contains a lot of useful middleware, so you can cover most of the daily web-realted use cases.

Have fun, see you in the next one.

### Resources

- [How to write ASGI middleware](https://pgjones.dev/blog/how-to-write-asgi-middleware-2021/)
- [Advanced middleware in FastAPI](https://fastapi.tiangolo.com/advanced/middleware/)
