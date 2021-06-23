---
title: Proxy usage when making requests with Python
date: 2018-10-19 08:07:31
tags: [python, aiohttp, proxy, requests]
author: Misha Behersky
language: en
---

In this article I would like to describe [proxy](https://en.wikipedia.org/wiki/Proxy_server) usage techniques within Python code, starting from basic usage to advanced requests through intermediate proxy pool service.

### Why?
Sometimes you need to connect to some resource that may be blocked by your [ISP](https://en.wikipedia.org/wiki/Internet_service_provider), sometimes you want to hide your real IP address, sometimes you need to bypass rate limiting when using a web-crawler. (_NOTE_: not all proxies support all the features, see classification below).

When talking about anonymity (hiding real user who is making request) there are three types of proxies:
*  highly anonymous - the web server can't detect the fact you are using a proxy;
*  anonymous - the web server can know you are using a proxy, but it can't see your real IP;
*  transparent - the web server can know you are using a proxy and it can also see your real IP.

And yes, we'll be using free proxies that are available as public lists and anyone across the web can use them.

And yes, we'll be using [Python 3.7](https://docs.python.org/3/whatsnew/3.7.html).

### First approach. Regular simple request
The simplest way to use a proxy and to make requests in general is obviously through [requests](http://docs.python-requests.org/en/master/) package.

```python
import requests

url = 'http://checkip.amazonaws.com/'

proxies = {
    'http': '116.206.61.234:8080',
    'https': '116.206.61.234:8080',
}

r = requests.get(url, proxies=proxies)
print(r.status_code)
print(r.content)
```

The nice thing about this library is support of  HTTPS, HTTP Basic Auth and configuration via environment variables (`HTTP_PROXY` and `HTTPS_PROXY`). But in this article we will focus on asynchronous request and particularly on [aiohttp.client](https://docs.aiohttp.org/en/stable/client.html) library.

### Second approach. Using proxy pool
Let's begin with simple request using aiohttp.

```python
async with aiohttp.ClientSession() as session:
    async with session.get("http://python.org",
                           proxy="http://proxy.com") as resp:
        text = await resp.text()
        print(resp.status)
        print(resp.text)
```

Authentication and providing proxy url via environment is also supported

```python
async with aiohttp.ClientSession(trust_env=True) as session:
    async with session.get("http://python.org") as resp:
        print(resp.status)
```

This way you'll tell client to use same `HTTP_PROXY` and `HTTPS_PROXY` environment variable for your proxy. And for the authentication just provide your credentials within uri like this

```python
session.get("http://python.org",
            proxy="http://user:pass@some.proxy.com")
```

If you prefer `~/.netrc` file that would also work.
The example above is only ok when a proxy you are using is reliable and you need to make just a couple of requests. But what happens if proxy becomes unavailable, you hit requests limit or get any other connection related error. A pool of proxy servers may help to deal with all the issues mentioned. The simplest prototype of this system should:
* store a list of available proxy servers
* iterate over them via [round-robin](https://en.wikipedia.org/wiki/Round-robin_scheduling)
* check proxy availability and if works properly return it to use when making next request.

That's enough to begin with, so we can implement our first pool. We'll start with compiling a list of proxies from public resources like [Free Proxy List](https://free-proxy-list.net/) and [HideMy.name](https://hidemyna.me/en/proxy-list/). Storing this list locally gives us access speed advantage and ability to come up with individual set that will work best for a specific case.
Suppose we have a file `proxies.txt` and here's our pool class definition with methods we want to implement

```python
class ProxyPool(object):
    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._proxies = None

    @property
    def proxies(self):
        if self._proxies is None:
            self._proxies = self.load_proxies()
        return self._proxies

    async def __anext__(self):
        for proxy in itertools.cycle(self.proxies):
            if await self._check_proxy(proxy):
                yield proxy

    async def _check_proxy(self, proxy_url) -> bool:
        pass

    def __aiter__(self):
        return self.__anext__()

    async def get_proxy(self):
        it = self.__aiter__()
        return await it.__anext__()

    def load_proxies(self):
        with open('proxies.txt') as f:
            return [line.strip() for line in f.readlines()]

    def __len__(self):
        return len(self.proxies)
```

What do we have here? We lazily load proxies list from a file, then we have an infinite async iterator that goes through this list, check proxy availability and spit url to the caller. Also we have `get_proxy` method that helps retrieve single proxy at a time (we'll rewrite this method later, because right now it always returns same first proxy at each invocation). As a `check_url` I've used [Amazon Check IP](http://checkip.amazonaws.com/) but you can use anything reliable enough that will work for your case (e.g. [httpbin](https://httpbin.org/get)).
`_check_proxy` method implementation is also straightforward, but it introduces another `_check_response` function. In most cases checking response status should be enough (like `return resp.status == HTTPStatus.OK`) but we can add extra logic to confirm proxy works correctly.

```python
from aiohttp import client_exceptions

async def _check_proxy(self, proxy_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.check_url, proxy=proxy_url) as resp:
                return await self._check_response(resp, proxy_url)
    except (
        client_exceptions.ClientOSError,
        client_exceptions.ClientHttpProxyError,
        client_exceptions.ServerDisconnectedError,
        client_exceptions.ClientProxyConnectionError,
    ) as e:
        print('Failed proxy check: %s', e)
        return False
```

We need to catch all possible connection errors and skip this proxy in such cases. When checking response we might want to confirm that target server sees our IP as proxy IP (or at least includes it in response text in case of transparent proxy)

```python
from http import HTTPStatus
from urllib.parse import urlparse

async def _check_response(self, resp,  proxy_url) -> bool:
    text = await resp.text()
    netloc = urlparse(proxy_url).netloc
    ip, colon, port = netloc.partition(':')
    return resp.status == HTTPStatus.OK and ip in text
```

That's it for now, so we can actually make requests using our `ProxyPool`

```python
import asyncio
from aiohttp import ClientSession

async def fetch(url, proxy):
    async with ClientSession() as session:
        print(f'Requesting {url} using {proxy}')
        async with session.get(url, proxy=proxy) as response:
            return await response.text()

async def main():
    pool = ProxyPool(check_url='http://checkip.amazonaws.com/')
    url = 'https://httpbin.org/get'
    counter = 0
    async for proxy in pool:
        resp = await fetch(url, proxy=proxy)
        print(resp)
        if counter > 3:
            break

if __name__ == '__main__':
    asyncio.run(main())
```

As an output you might see something like this

```
Cannot connect to host 78.159.79.245:57107 ssl:None [Connect call failed ('78.159.79.245', 57107)]
Requesting https://httpbin.org/get using http://104.248.171.204:3128/
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
    "Host": "httpbin.org",
    "User-Agent": "Python/3.7 aiohttp/3.4.4"
  },
  "origin": "104.248.171.204",
  "url": "https://httpbin.org/get"
}
```

So it skips first item in our list and then it successfully makes request using next candidate from the pool, great job!
Assuming the code above works properly let's make some optimizations. First we need to make sure proxy list will be shared between `ProxyPool` instances not to make heavy  I/O operations on each instantiation. We are going to use class attribute for that

```python
from random import shuffle

class ProxyPool(object):

    _proxies = None

    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._instance_proxies = None

    @property
    def proxies(self):
        if ProxyPool._proxies is None:
            ProxyPool._proxies = self.load_proxies()

        if self._instance_proxies is None:
            self._instance_proxies = ProxyPool._proxies[:]
            shuffle(self._instance_proxies)
        return self._instance_proxies
```

As you see we are using same [lazy loading](https://en.wikipedia.org/wiki/Lazy_loading) technique but this time list of proxies is stored as a class attribute for all instances to share it. Additionally we shuffle this list per instance in case there will be multiple pools in our code.
This way we'll make sure load distribution between proxies instead of multiple connections trying to use on proxy at the same moment.

Another optimization will be related to iteration and `get_proxy` method. We want to store iterator state to resume from the last item and not just return first item from the list. Defining one more instance attribute will do the trick

```python
class ProxyPool(object):
    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._instance_proxies = None
        self._aiter = None

    @property
    def __aiter(self):
        if self._aiter is None:
            self._aiter = self.__anext__()
        return self._aiter

    def __aiter__(self):
        return self.__aiter

    async def get_proxy(self):
        it = self.__aiter__()
        return await it.__anext__()
```

We can reuse same instance of `async_generator` for each pool instance because `itertools.cycle` over our proxy list will never exhaust making sure we return new proxy on each call using round-robin algorithm. Confirm that with

```python
import asyncio

async def main():
    pool1 = ProxyPool()
    proxy1 = await pool1.get_proxy()
    proxy2 = await pool1.get_proxy()
    assert proxy1 != proxy2

    pool2 = ProxyPool()
    proxy3 = await pool2.get_proxy()
    proxy4 = await pool2.get_proxy()
    assert proxy3 != proxy4

    it1 = pool1.__aiter__()
    it2 = pool1.__aiter__()
    assert it1 is it2

    it3 = pool2.__aiter__()
    it4 = pool2.__aiter__()
    assert it3 is it4

if __name__ == '__main__':
    asyncio.run(main())
```

Now we have fully functional `ProxyPool` that can be used within our request-based application. For implementation reference you can check [this github code](https://github.com/bmwant/solenie/blob/master/jerry/proxy/file_pool.py).

### Third approach. Using middleman proxy service
For this case we'll be using [Scylla](https://github.com/imWildCat/scylla) project. First we need to launch a proxy service and the simplest way to accomplish this is by using [docker](https://www.docker.com/get-started)

```bash
$ docker run -d -p 8899:8899 -p 8081:8081 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest
$ docker ps
```

We can both retrieve list of proxies from scylla to use with our proxy pool or use it as a forward proxy server. For the latter one the usage is really simple, you just specify url to your proxy and for the each request it selects random proxy and
returns it to you.

```python
import asyncio
from aiohttp import ClientSession

async def fetch(url, proxy):
    async with ClientSession() as session:
        print(f'Requesting {url} using {proxy}')
        async with session.get(url, proxy=proxy) as response:
            text = await response.text()
            print(response.status)
            print(text)

async def main():
    url = 'http://api.ipify.org'
    proxy = 'http://127.0.0.1:8081'
    await fetch(url, proxy=proxy)

if __name__ == '__main__':
    asyncio.run(main())
```

As expected we get our proxy IP in output and it's similar to what we've seen earlier

```
Requesting http://api.ipify.org using http://127.0.0.1:8081
200
185.27.61.126
```

....but! With such a simplicity we have to pay a very high price

> Note: HTTPS requests are not supported at present.

To deal with this we need to apply this workaround

```python
async def get_proxy():
    scylla_url = 'http://localhost:8899/api/v1/proxies?https=true'
    async with ClientSession() as session:
        async with session.get(scylla_url) as response:
            result = await response.json()
            proxies = result['proxies']
            shuffle(proxies)
            return proxies[0]

async def main():
    url = 'https://kinopoisk.ru/'
    proxy_dict = await get_proxy()
    proxy_url = 'http://{0[ip]}:{0[port]}'.format(proxy_dict)
    await fetch(url, proxy=proxy_url)
```

In the code above we explicitly request proxy supporting `https` connection and randomly choose one of them. You can also sort `proxies` list based on `stability` property of each item. (_NOTE_: when building a url to proxy we still use **http** because only **http** proxies are supported. This implies all the data passed between you and proxy will be unencrypted, so make sure not to pass any sensitive data. Do not be confused that we filtered our proxies by **https** parameter, that only means proxy server can send https requests to other resources that enforces encryption, not that you can make secure requests).

I guess that's it for today. Don't be shy and leave your comments or share your knowledge about proxies below.

### Resources
* [Do not even try, you cannot use public proxies with Google](https://www.my-proxy.com/blog/google-proxies-dead)
* [Making an unlimited number of requests with aiohttp](https://medium.com/@cgarciae/making-an-infinite-number-of-requests-with-python-aiohttp-pypeln-3a552b97dc95)
* [Specify your proxy credentials in .netrc file](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html)
