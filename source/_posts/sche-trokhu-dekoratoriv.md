---
title: Ще трохи декораторів
date: 2015-10-26 18:14:27
tags: [python, decorator]
author: Misha Behersky
language: ua
archived: true
---

### Декоратори на основі класів

У всіх прикладах буде створюватися декоратор, що надає функцію логування (вивід в консоль перед і після виконання нашої функції)

```python
def my_func():
    """
    Docstring of my function
    """
    print('Inside my_func')
```

Найпростіший варіант, декоратор без параметрів, без збереження оригінального імені та докстрінга:

```python
class MyDecorator1(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print('Before function %s call' % self.func.__name__)
        result = self.func(*args, **kwargs)
        print('After %s was called' % self.func.__name__)
        return result
```

Аналогічний варіант з використанням `functools.update_wrapper`

```python
class MyDecorator2(object):
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print('Before function %s call' % self.func.__name__)
        result = self.func(*args, **kwargs)
        print('After %s was called' % self.func.__name__)
        return result
```

Декорується аналогічно першому варіанту, але додатково можна звертатися до атрибутів `__doc__`, `__name__` початкової функції:

```python
@MyDecorator2
def my_func():
    ...

print(my_func.__name__)
print(my_func.__doc__)
```

Декоратор з параметром (можна декількома) з `functools.wraps`

```python
class MyDecorator3(object):
    def __init__(self, argument):
        self.argument = argument
        print('Called with argument: %s' % argument)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Before function %s call' % func.__name__)
            result = func(*args, **kwargs)
            print('After %s was called' % func.__name__)
        return wrapper

@MyDecorator3(5)
def my_func():
    ...
```

Стосовно використання, то найчастіше декоратори на основі класів застосовують, коли необхідно зберігати деякий стан. Також, якщо логіка декоратора дещо складна і потрібно декілька додадкових методів (щоб все це знаходилося поруч). Для прикладу: декоратор, що рахує кількість викликів даної функції

```python
class MyDecorator4(object):
    def __init__(self, func):
        self.func = func
        self.times = 0
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.times += 1
        result = self.func(*args, **kwargs)
        print('Function %s has been called %d times' % (self.func.__name__,
                                                        self.times))
        return result


my_func()
my_func()
```

### Декоратор з опціональним параметром

Повернемося до декораторів на основі функцій і розглянемо таку ситуацію. Є декоратор, що приймає опціональний параметр

```python
def decorator1(argument=None):
    if argument is not None:
        print(argument)
    ...
```

Коли ми хочемо викликати його з параметром, ми пишемо

```python
@decorator1(100)
def my_func():
    ...
```

але коли опускаємо опціональний параметр

```python
@decorator1()
def my_func():
    ...
```

тобто, все одно доводиться писати дужки. Чи можна зробити так, щоб не потрібно було писати дужки, коли немає параметра. Звісно, відповідь позитивна, давай код

```python
def decorator(*args):
    func = None
    without_args = False
    if args:
        func, *decor_args = args
    if callable(func):
        without_args = True
    else:
        decor_args = args
    # Now you can use all arguments passed to decorator as decor_args
    def outer_wrapper(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            print('Before function %s call' % method.__name__)
            result = method(*args, **kwargs)
            print('After %s was called' % method.__name__)
            return result
        return wrapper
    if without_args:
        return outer_wrapper(func)
    return outer_wrapper
```

Просто додаємо ще одну перевірку, чи декоратор викликаний з аргументами, чи без і на основі цього передаємо потрібну *обгортку*. В результаті цей декоратор можна застосовувати будь-яким способом: `@decorator`, `@decorator()`, `@decorator(1, 2, 3)`.

Отож, є мільярд варіантів як можна написати декоратор. Тут мав би бути ще якийсь логічний висновок стосовно вищесказаного, але не склалося.

### Ресурси

* [Патерни та рецепти для Пайтона](http://python-3-patterns-idioms-test.readthedocs.org/en/latest/PythonDecorators.html)
* [12 кроків до розуміння декораторів](http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/)
