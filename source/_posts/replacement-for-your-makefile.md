---
title: Replacement for your Makefile
date: 2016-10-19 15:48:23
tags: [python, make, devops, infra, tools]
author: Misha Behersky
language: en
---

### Intro

Makefile is a [gnu utility](https://www.gnu.org/software/make/manual/make.html) that was aimed to simplify compilation process. You can forget long command with dozens of flags or params and with makefile u have targets and they can save your time while typing complicated command. If you familiar with bash aliases then it's very similar concept. That helps a lot in day to day tasks. The command below would be easy as `make tests`

```makefile
tests:
  @pip install -r requirements/test-requirements.txt
  @py.test --junitxml=./testResults.xml --cov-config=.unit_coveragerc --cov-report xml --cov ./ test/
```

But in a large project this file can grow up to 1K lines of code which is hard to read and understand because of such reasons:

* you should learn completely different syntax (that differs even from bash scripts you probably use too)
* hard to understand for newcomers and some rules are really hard to remember
* you cannot use it on different platforms like FreeBSD
* you want to have same language across your projects, it's more convenient

So, meet [pyinvoke](http://www.pyinvoke.org) - a tool that helps you deal with issues above and can completely replace makefile. It's very similar to the [Ruby Rake](https://github.com/ruby/rake) one.
In typical python project you have a bunch of task you use from time to time - just use the decorator and write them as usual python functions.

What will you have out of the box:

* namespacing
* task aliasing
* before/after hooks
* parallel execution
* flag-based style of command-line parsing
* multiple tasks in single invocation

The tool is python 3 compatible and has no other dependencies. It's definitely worth it to try this tool.

### My slides from PyCon Poland 2016 Lightning talk

<iframe src="//www.slideshare.net/slideshow/embed_code/key/3JUtakXCYqnKwc" width="510" height="420" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen></iframe>

### Resources

* [Makefile tutorial](http://medium.com/@tomchentw/makefile-to-automate-things-304ce6779bf)
