---
title: OAuth for your aiohttp web application
date: 2018-03-18 16:28:25
tags: [python, oauth, aiohttp, web, ngrok]
author: Misha Behersky
---

It's pretty easy and convenient to use authorization on you service with a help of third party oauth services using popular web frameworks such as Flask ([Flask-OAuthlib](http://flask-oauthlib.readthedocs.io/en/latest/oauth2.html)). There are a lot of tutorials and examples for them but what about [aiohttp](https://aiohttp.readthedocs.io/en/stable/)?

In this article I'm going to show simple Github OAuth authorization in your web application using [aioauth-client](https://github.com/klen/aioauth-client).

### Starting from a scratch
Create main application script `app.py` and install requirements into your virtual env
```
$ mkvirtualenv -p python3 app
$ pip install aiohttp aioauth_client
```
and then create a simple endpoint. The simplest version of the server will look like this
```
from aiohttp import web

async def index(request):
    return web.Response(text='My app')


def main():
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app, port=8080)


if __name__ == '__main__':
    main()
```

Now let's register your new app on github and add `/auth` route to your application. [Click here](https://github.com/settings/applications/new) and register your app to obtain `client id` and `client secret` values. Note that while developing you may need proxy github request to your application running at localhost but that can be easily bypassed with a help of [ngrok](https://ngrok.com/). On the screenshot below you see tunnels such a values for ngrok tunnels to my local app.
![register your app](/img/article/0c1c642a0c9138528c89ad465b1b038d.png)

Do not worry, when going to production you will change those to your own domain. Just add secrets to your application file and create additional endpoint for authorization
```
GITHUB_CLIENT_ID = '<your-client-id>'
GITHUB_CLIENT_SECRET = '<your-client-secret>'

async def github_auth(request):
    github = GithubClient(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
    )

    if 'code' not in request.query:
        return web.HTTPFound(github.get_authorize_url(scope='user:email'))

    code = request.query['code']
    token, data = await github.get_access_token(code)
    print(token)
    print(data)
    return web.HTTPFound('/')

def main():
    ...
    app.router.add_get('/auth', github_auth)
```
Now visit `/auth` endpoint in your browser and you'll get redirected to github auth page and the you'll see a token in console output. This token allows you to do authorized requests and obtain data you may be interested in defined by [scope](https://developer.github.com/apps/building-oauth-apps/scopes-for-oauth-apps/#available-scopes) your request. We now can make a request using this token and retrieve some information about user like this
```
    ...
    code = request.query['code']
    token, data = await github.get_access_token(code)
    github = GithubClient(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        access_token=token
    )
    user, info = await github.user_info()
    return web.Response(text=json.dumps(info))
```
and browser will render a page with data like **login**, **id**, **email**, etc. This has no much use though as long as we do not store this token anywhere in order for other routes to be able make same request too. Meet `aiohttp-session` for the rescue
```
$ pip install cryptography aiohttp_session
```
The simplest way is to store our session data as an encrypted cookie and that will be shared between all our requests. Get this package configured first
```
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

def main():
    ...
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    aiohttp_session.setup(app, EncryptedCookieStorage(secret_key))
```
As another helper utility we will create `login_required` decorator requiring endpoint to pass authorization first or reuse existing info stored within our session.
```
def login_required(fn):
    async def wrapped(request, **kwargs):
        session = await get_session(request)

        if 'token' not in session:
            return web.HTTPFound('/auth?redirect_uri={}'.format(request.url))

        github = GithubClient(
            client_id=config.GITHUB_CLIENT_ID,
            client_secret=config.GITHUB_CLIENT_SECRET,
            access_token=session['token']
        )
        user, info = await github.user_info()

        return await fn(request, user, **kwargs)

    return wrapped
```
Note additional parameter `redirect_uri` allowing us to continue browsing our web site starting from the last page visited not from the index one.
And below is a modified version of `github_auth` function
```
async def github_auth(request):
    github = GithubClient(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
    )
    session = await aiohttp_session.get_session(request)

    if 'code' not in request.query:
        redirect_uri = request.query.get('redirect_uri', '/')
        session['redirect_uri'] = redirect_uri
        return web.HTTPFound(github.get_authorize_url(scope='user:email'))

    code = request.query['code']
    token, _ = await github.get_access_token(code)

    session['token'] = token
    next_uri = session.pop('redirect_uri', '/')
    return web.HTTPFound(next_uri)
```
We are following the same steps as previously but this time we store `token` in our session and therefore no need to request it each time user hits the endpoint.
Finally decorate any of your endpoints as shown below and access your user info in a handy way.
```
@login_required
async def only_authorized_access(request, user):
    return web.Response(text=f'Hello, {user.username} in our restricted area!')
		
def main():
    ...
    app.router.add_get('/restricted', only_authorized_access)
```
Visiting `/restricted` will show such you a message

> Hello, bmwant in our restricted area!

### Summary
I have covered only basic usage of the package for authorization but you should keep in mind that connecting other networks like Bitbucket, Facebook, Google, Twitter, VK, Yandex is as easy as adding singe endpoint to existing code. Next steps will be storing your user in Redis cache (and not making query to third party services on each request) and implementing `/logout` route (just deleting a token from a session and redirecting to index page). At this point you should be good to go developing your application with simple authorization in place.

### Resources
* [More examples of aioauth usage](https://github.com/klen/aioauth-client/tree/develop/example)
* [aiohttp-session docs](http://aiohttp-session.readthedocs.io/en/latest/)
* [Article about ngrok usage (in Ukrainian)](http://bmwlog.pp.ua/post/75)