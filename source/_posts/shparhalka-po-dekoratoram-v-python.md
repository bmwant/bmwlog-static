---
title: Шпаргалка по декораторам в Python
date: 2015-03-19 18:58:34
tags: [python, cheatsheet, decorator]
author: Misha Behersky
language: ua
archived: true
---

Приклади для написання власних декораторів (з параметрами і без) на випадок, якщо синтаксис трохи підзабувся.

```python
from functools import wraps

def decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before func call
        result = func(*args, **kwargs)
        # Do something after func call
        return result
    return wrapper

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before func call
        result = func(*args, **kwargs)
        # Do something after func call
        return result
    return wrapper
```

Два приклади для декораторів без параметрів; другий з використанням `functools.wraps`, яка потрібна для того, щоб зберегти оригінальне ім'я і докстрінг функції замість її декоратора.

```python
from functools import wraps

def decorator(arg1, arg2):
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            # Do something before func call
            result = func(*args, **kwargs)
            # Do something after func call

            # Also you can use additonal arguments
            result = result * arg1 + arg2

            return result
        return wrapper
    return outer_wrapper

def decorator(arg1, arg2):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Do something before func call
            result = func(*args, **kwargs)
            # Do something after func call

            # Also you can use additonal arguments
            result = result * arg1 + arg2

            return result
        return wrapper
    return outer_wrapper
```

Аналогічно для декоратора з параметрами. Додається ще одна функція-обгортка.
Також для спрощення роботи з декораторами існує модуль [wrapt](https://github.com/GrahamDumpleton/wrapt), який прискорює написання коду і ще багато всього (див. документацію).

### Ресурси

* [Документація по functools](https://docs.python.org/2/library/functools.html)
* [Документація модуля wrapt](http://wrapt.readthedocs.org/en/latest/index.html)
