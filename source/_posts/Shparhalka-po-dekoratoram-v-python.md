---
title: Шпаргалка по декораторам в Python
date: 2015-03-19 18:58:34
tags: [python, cheatsheet, decorator]
author: Misha Behersky
---

<p>
 Приклади для написання власних декораторів (з параметрами і без) на випадок, якщо синтаксис трохи підзабувся.
</p>
<pre>
<code class="language-python">from functools import wraps

def decorator(func):
    def wrapper(*args, **kwargs):
        #Do something before func call
        result = func(*args, **kwargs)
        #Do something after func call
        return result
    return wrapper

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #Do something before func call
        result = func(*args, **kwargs)
        #Do something after func call
        return result
    return wrapper  </code></pre>
<p>
 Два приклади для декораторів без параметрів; другий з використанням
 <strong>
  functools.wraps
 </strong>
 , яка потрібна для того, щоб зберегти оригінальне ім'я і докстрінг функції замість її декоратора.
</p>
<pre>
<code class="language-python">from functools import wraps

def decorator(arg1, arg2):
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            #Do something before func call
            result = func(*args, **kwargs)
            #Do something after func call
            
            #Also you can use additonal arguments
            result = result * arg1 + arg2
            
            return result
        return wrapper
    return outer_wrapper

def decorator(arg1, arg2):
    def outer_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            #Do something before func call
            result = func(*args, **kwargs)
            #Do something after func call
            
            #Also you can use additonal arguments
            result = result * arg1 + arg2
            
            return result
        return wrapper
    return outer_wrapper</code></pre>
<p>
 Аналогічно для декоратора з параметрами. Додається ще одна функція-обгортка.
</p>
<p>
 Також для спрощення роботи з декораторами існує модуль
 <a href="https://github.com/GrahamDumpleton/wrapt" target="_blank">
  wrapt
 </a>
 , який прискорює написання коду і ще багато всього (
 <em>
  див. документацію
 </em>
 )
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="https://docs.python.org/2/library/functools.html" target="_blank">
  Документація по functools
 </a>
</p>
<p>
 <a href="http://wrapt.readthedocs.org/en/latest/index.html" target="_blank">
  Документація модуля wrapt
 </a>
</p>