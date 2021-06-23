---
title: leak package
date: 2017-06-26 11:24:15
tags: [python, utils, pypi]
author: Misha Behersky
language: en
---

### Intro

In this article I'm going to describe small utility that is intended to provide some useful information about packages released to the [PyPI](https://pypi.python.org/pypi). `leak` is a tool that shows you all the releases of a package specified that can be downloaded and installed. Sometimes it's very useful to see a list of them in order to be able install next/previous major/minor release of a package. And therefore to see all the versions available you need to manually go to the project's page and find the version you are interested in.

Recent versions of `pip` also know how to do it, so right now `leak` kinda overlaps with what we have as a built in feature (example pip output below)

```
Could not find a version that satisfies the requirement django==5.2.3
(from versions: 1.1.3, 1.1.4, 1.2, 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5,
1.2.6, 1.2.7, 1.3, 1.3.1, 1.3.2, 1.3.3, 1.3.4, 1.3.5, 1.3.6, 1.3.7,
1.4, 1.4.1, 1.4.2, 1.4.3,
```

### Usage

Installation of the package is simple and straightforward. Just type

```bash
$ pip install leak
$ leak
```

e.g.

```bash
$ leak django
```

It will display you sorted list of available versions and highlight the **most popular one** and the **most recent one** (with number of downloads and release date correspondingly). It will also provide short description, package home page URL and author's name as well as email.

![terminal](/old/article/014a00967ecb3e51bd9b36a1191ffccc.png)

### Implementation

Behind the scenes there is simple requests-based script that calls PyPI api `http://pypi.python.org/pypi/{package_name}/json` and just parses result printing it as a table with colorized text.

It's still under *not-so-active* development, so feel free to open an issue/PR or just write me an email with any improvement you want to see within this tool.

See you!

### Resources

* [Link to the page on PyPI](https://pypi.python.org/pypi/leak)
* [Link to the GitHub repository](https://github.com/bmwant/leak)
* [Core utilities for python packaging](https://github.com/pypa/packaging)
* [How to properly version you package not adding headeache for others](http://semver.org)
* [How to print colored output in console](https://pypi.python.org/pypi/termcolor)
* [...but I recommend to use click instead though](http://click.pocoo.org/5/utils/#ansi-colors)
