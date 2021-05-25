---
title: Using pyenv on Ubuntu
date: 2019-02-05 10:00:53
tags: [python, cheatsheet, linux, python3, virtualenv]
author: Misha Behersky
---

[Pyenv](https://github.com/pyenv/pyenv) is a tool that allows you to easily install multiple different Python versions and flawlessly switch between them. Pyenv is not a replacement for [virtual environment](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) but it can also help you manage those.
The easiest way to obtain pyenv along with a set of useful plugins is the following

```
$ curl https://pyenv.run | bash
```

You can list plugins installed via

```
$ ls -1 ~/.pyenv/plugins/
```

The [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) one is used to manage you virtual environments and also will be mentioned below.

Update your shell login file `~/.bashrc` with content

```
export PATH="/home/user/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

and restart terminal or `source ~/.bashrc` in current session and you are good to go.

### Install new version of Python
To make sure every version of Python will be built without any errors and all the modules will work out of the box you should install development packages in advance

```
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

After that you want to check which options you are allowed to choose from

```
$ pyenv install --list
```

and to be more specific you can do something like ` pyenv install --list | grep 3.5`

```
$ pyenv install 3.5.6
```

If you are interested about what's happening under the hood you can provide `--verbose` flag. Once you successfully installed it you can list all the versions available with

```
$ pyenv versions
```

**NOTE**: Sometimes you might need to pass custom flags to a build process in order to tune your installation. This can be done in a such way `$ CONFIGURE_OPTS=--enable-shared pyenv install 2.7.6`

The best way to deal with multiple Python versions on the same system is by leveraging virtual environments (see the section below). But in case you want to set a version globally (across every shell) or locally (per specific directory) you can use commands

```
$ pyenv global 2.7.6  # will be used py all shells
$ pyenv local 3.5.6  # will be used per directory; overrides version defined above
```

### Working with virtual environments
Create virtual environment

```
$ pyenv virtualenv [version] [name]
$ pyenv virtualenv 3.5.6 venv
```

Activate earlier created virtual environment

```
$ pyenv activate [name]
$ pyenv activate venv
```

and deactivate it (usual `deactivate` will not work)

```
$ pyenv deactivate [name]
$ pyenv deactivate venv
```

You can also spawn a REPL with specific python version without creating virtual environment in current shell like this

```
$ pyenv shell 3.5.6  # set specified python version for current session
$ python --version  # check the version of python used
Python 3.5.6
$ pyenv shell  # without an argument it will output version the has been set
3.5.6
$ pyenv shell --unset  # restore to regular settings
$ python --version  # check default one is invoked
Python 2.7.15rc1
$ pyenv shell
pyenv: no shell-specific version configured
```

To list all available virtual environments on your system invoke

```
$ pyenv virtualenvs
```

### Resources
* [Commands reference](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md)
* [Build Python manually from source code](https://bmwlog.pp.ua/post/install-python-on-ubuntu-xenial)
* [Passing configure options to a build process](https://github.com/pyenv/pyenv/issues/86)
* [Pyenv troubleshooting](https://github.com/pyenv/pyenv/wiki#troubleshooting--faq)