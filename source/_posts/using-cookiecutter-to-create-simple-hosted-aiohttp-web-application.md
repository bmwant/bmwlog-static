---
title: Using cookiecutter to create simple hosted aiohttp web application
date: 2018-03-04 12:45:54
tags: [python, asyncio, heroku, web, tutorial]
author: Misha Behersky
language: en
---

### Overview
We will be using cookiecutter package to quickly spin up a simple web application using next stack: Python 3 + aiohttp + npm + Heroku. The main advantages of this approach is to have working and deployed application in couple of minutes. The only thing left is to update your business logic on back-end and to rearrange components on your html pages using one of the simplest css frameworks ([siimple](https://siimple.juanes.xyz/documentation/)).

### Prerequisites
If you do not have those yet make sure all of the dependencies are installed first
* [Python 3](install-python-on-ubuntu-xenial)
* [pipenv](https://pipenv.readthedocs.io/en/latest/)

```bash
$ pip install pipenv
```

*  [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
*  [NPM](https://www.npmjs.com/get-npm)

That should be enough to start.

### So easy?
Clone preexisting boilerplate code from github and answer couple of questions about your future project and you'll be good to go. Let's assume that our project name is `myapp`.

```bash
$ git clone git@github.com:bmwant/templio.git
$ pip install cookiecutter
# you might need root permissions for command above
# e.g. sudo -H pip install cookiecutter
$ cookiecutter templio
$ cd myaap
$ pipenv  install
$ npm install
```

Check and verify that our project works locally and everything is in place by launching it

```bash
$ pipenv shell
$ export PORT=8081  # 8080 is the default one so you can override to any
$ python runserver.py
```

Now visit `127.0.0.1:8081` in your browser and that's it.

### Deployment
It's time to make our site available for others via free hosting on [Heroku](https://devcenter.heroku.com/).
Create new application [here](https://dashboard.heroku.com/new-app) and type commands below

```bash
$ heroku login  # just one to sign into your account
$ cd myapp/
$ git init
$ heroku git:remote -a myapp
$ git add .  # add all files within our project
$ git commit -am "Initial commit"
$ git push heroku master
```

Now you can access your web application at `https://myapp.herokuapp.com/` and share that link with others!
Your regular developing workflow would look like this:
1. Make some changes locally (e.g. add new endpoints/templates)
2. Test modifications locally (via `python runserver.py`)
3. Commit changes to git repository
4. Deploy changes to remote (`git push heroku master`)

Basically, it's everything you need to now at this point to have a _ready-to-go_ web application. You can fork `templio` project and edit it according to your taste making it easier to create new projects from a scratch a lot faster than before.

### Resources
* [Cookiecutter docs](https://cookiecutter.readthedocs.io/en/latest/index.html)
* [aiohttp docs](https://aiohttp.readthedocs.io/en/stable/)
