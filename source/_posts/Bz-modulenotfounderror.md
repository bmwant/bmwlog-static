---
title: bz2 ModuleNotFoundError
date: 2018-06-05 16:38:36
tags: [ubuntu, python, pipenv, virtualenv, fix]
author: Misha Behersky
---

![error](/img/article/7e0e1cbd8d1d3c458a9c036e01f569be.png)

This error means that you have missing `bz2` headers (probably because you've built python from sources without this option enabled), so you need to install them first (for Ubuntu/Debian):
```bash
# apt-get install libbz2-dev
```
Now we need to reconfigure your python and reinstall it once again (version `3.6.5` for example below)
```bash
$ tar -xvf Python-3.6.5.tar.xz
$ cd Python-3.6.5/
$ ./configure
$ make
$ sudo make install
```
Check whether it works properly now
```bash
$ python3.6 - c "import bz2"
```
should return without any errors. And make sure to recreate your virtual environment which will use new python executable
```bash
$ pipenv --python 3.6.5
$ pipenv install
```
You should be all set up now, continue the adventure!