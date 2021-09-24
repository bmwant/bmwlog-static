---
title: Using Poetry in production
date: 2019-05-28 06:41:38
tags: [python, poetry, docker, ansible, devops]
author: Misha Behersky
language: en
---

In this article I want to share my experience of using [Poetry](https://poetry.eustace.io/docs/) dependency manager in production environment. At the moment of writing it's still [immature](https://github.com/sdispater/poetry/issues) and have no major release yet (only *alpha pre-release* [version is available](https://github.com/sdispater/poetry/releases/tag/1.0.0a3)). Nevertheless I was able to successfully adopt it for real production Python web application (Docker/Python/Django) as well as migrate engine of this blog to use it (so if you are reading this article all the things is going good so far). I'll provide some code snippets to show basic ideas for migration/integration of the tool and you will be able to find complete examples of such usages within [repository for this blog](https://github.com/bmwant/bmwlog).

### Local installation and usage
I would not go through all the details of why you need to use additional tool to manage your Python dependencies. If you are here I assume that you know why you need it (check [[1]](https://www.kennethreitz.org/essays/a-better-pip-workflow) [[2]](http://andrewsforge.com/article/python-new-package-landscape/) [[3]](https://nvie.com/posts/pin-your-packages/) if you are not sure why you've landed here). There were a lot of attempts [[1]](https://github.com/mitsuhiko/pipsi) [[2]](https://github.com/jazzband/pip-tools) [[3]](https://github.com/pypa/pipenv) for creating similar tool and it's just another step forward [to make built-in pip](https://pip.pypa.io/en/stable/news/) capable of fulfilling all the developer's needs.

Let's start with your development environment and install Poetry locally with this command

```bash
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

and make sure executable is available within your shell

```bash
$ cat ~/.poetry/env >> ~/.bashrc
$ source ~/.poetry/env
$ poetry --version
```

Now type `poetry init` and go through interactive process of creating a `pyproject.toml` file for your project (if you want to skip searching for every library during this feel free to do that later). Adding new package or dev dependency looks like this

```bash
$ poetry add django==2.0.12
$ poetry add --dev django-debug-toolbar==1.5
```

See [this link](https://poetry.eustace.io/docs/versions/#version-constraints) for version constraints.

Then you will be able to `poetry install` on any other machine or `poetry install --no-dev` for production environment.

Once you have Poetry installed you can run any regular command you want with `poetry run`. For example you can launch your unittest with

```bash
$ poetry run pytest -sv tests/
```

In case you do not want to type two extra words you can just execute `poetry shell` which is the equivalent of activating virtual environment within current shell. Note that Poetry is able not only to install dependencies into your virtual environment but also to create a new one automatically. It nicely works with [pyenv](https://github.com/pyenv/pyenv) and allows you to create virtual environment with any specific Python version. You can {% post_link using-pyenv-on-ubuntu 'read more about pyenv here' %} but basically it looks like this

```bash
$ pyenv local 3.6.8
$ poetry install
```

Poetry will use Python version installed by pyenv and create virtualenv using it for you. Now everything is ready for you to create new features and test them.

### Travis CI integration
After having everything locally you might want your continuous integration service to use the same environment when running test suite for your code. Here's an example of how Poetry can be installed on [Travis CI](https://travis-ci.org/)

```yaml
before_install:
  - pip install --upgrade pip
  - curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
  - export PATH="$HOME/.poetry/bin:$PATH"
install:
  - poetry install
```

Just add/update `before_install` section of your `.travis.yml` config and you will be able to use Poetry the same way as you do locally

```yaml
script:
  - poetry run pytest -sv tests/
```

As I mentioned before Poetry works really well with pyenv, so that gives you another advantage here: you will be able to install any patch release versions of Python (*like 3.5.2*) to make sure the exact same version is used across all your environments (Travis allows you to [specify only minor](https://docs.travis-ci.com/user/languages/python/#specifying-python-versions) releases)

```yaml
env:
  global:
    - PYTHON_VERSION=3.5.2
language: generic
before_install:
  # Update pyenv and install Python
  - cd $(pyenv root)
  - git fetch && git checkout v1.2.11
  - pyenv install $PYTHON_VERSION
  - cd - && pyenv local $PYTHON_VERSION
```

Travis has pyenv preinstalled but the version is slightly outdated and doesn't contain most of the recent releases, so we need couple of extra steps to upgrade it. Now we can move on and deploy our code to production environment once CI build is green.

### Deploying with Ansible
The only thing you want to double check on a production environment is that every Python-related command should be executed with `poetry run`. Besides that you only need to install Poetry

```yaml
- name: install Poetry
  shell: >
    set -o pipefail &&
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

and install dependencies with it instead of invoking [pip module](https://docs.ansible.com/ansible/latest/modules/pip_module.html) or directly executing `pip install -r requirements.txt`

```yaml
- name: install Python requirements with Poetry
  environment:
    PATH: "{{ ansible_env.HOME }}/.poetry/bin:{{ ansible_env.PATH }}"
  shell: "poetry install"
  args:
    chdir: "{{ project_root }}"
```

You might want to manage your virtual environment elsewhere (when not using pyenv for example), so don't forget to update `environment` in your Python-related tasks with `VIRTUAL_ENV: "{{ venv_directory }}"`. Now you are able to launch your application with any kind of an entrypoint

```bash
$ poetry run gunicorn myproject.wsgi
$ poetry run python manage.py runserver
$ poetry run run.py  # etc
```

**NOTE**: `poetry run` just makes sure you are using proper virtual environment, so if you want to have even more control for some reason you can definitely do something like `{{ venv_directory }}/bin/python -c "import django; print(django.__version__)"`. To figure out a path to your virtual environment (in case it was created with Poetry) just invoke `poetry env info -p` command. Poetry is agnostic to a tool you use for virtual environment creation (either [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), [conda](https://docs.conda.io/en/latest/) etc) and it just ensures your dependency tree resolves properly and is consistent with `pyproject.toml`/`poetry.lock` files.

### Docker integration
Docker provides you high level of isolation but once again: you want all your environments to be consistent and that's why you need to use Poetry when building Docker images too. `Dockerfile` requires minimum modifications, so just add installation command you are already familiar with.

```dockerfile
# install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH "/home/user/.poetry/bin:${PATH}"

# add and install python requirements
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# run server
CMD ["poetry", "run", "python", "run.py"]
```

Another good idea is to override entrypoint, so each time running your image will not require extra `poetry run` typing. `docker run -it myproject:latest python` will bring you straight to the Python shell within proper environment.

```dockerfile
ENTRYPOINT ["poetry", "run"]
CMD ["python", "run.py"]
```

Additionally you might want to tag your image based on the environment it contains, so this command `sha1sum poetry.lock | awk '{ print $1 }'` will create a unique tag based on hash sum of your dependencies. In case you have your own tagging schema you may want at least [label](https://docs.docker.com/config/labels-custom-metadata/) an image with this tag.

### Note for Heroku users
[Heroku](https://www.heroku.com/) is a great service allowing you to quickly deploy your relatively small applications and it's [Python buildpack](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python) even has [an integration with pipenv](https://github.com/heroku/heroku-buildpack-python/blob/master/bin/steps/pipenv). Unfortunately Poetry is not supported at the moment, so you need to manually export your dependencies to regular `requirements.txt` file

```bash
$ poetry self:update --preview  # to be able use export feature
$ poetry export -f requirements.txt
```

You might want to setup [git hooks](https://githooks.com/) on commit/push to automatically export requirements before deployments. Once file is in place you trigger deploy as you usually do

```bash
$ heroku buildpacks:set heroku/python
$ git push heroku master
```

Now you have a good understanding of how Poetry is integrated with variety of instruments and it will be easy to do the same set up with any other tool your stack requires.

### Resources
* [Travis config example](https://github.com/bmwant/bmwlog/blob/master/.travis.yml)
* [Ansible playbook example](https://github.com/bmwant/bmwlog/blob/master/deploy/ansible/roles/app/tasks/main.yml)
* [Dockerfile example](https://github.com/bmwant/bmwlog/blob/master/Dockerfile)
* [Python dependency management](https://hynek.me/articles/python-app-deps-2018/)
