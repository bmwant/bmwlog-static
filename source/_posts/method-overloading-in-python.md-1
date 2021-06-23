---
title: Method overloading in Python
date: 2018-07-18 11:42:29
tags: [python, dispatch, overloading, patterns, decorator]
author: Misha Behersky
language: en
---

Python does not support method/functions overloading as other languages do. For example in C++ we can define three different methods that will support different types of arguments

```cpp
class printData {
   public:
      void print(int i) {
        cout << "Printing int: " << i << endl;
      }
      void print(double  f) {
        cout << "Printing float: " << f << endl;
      }
      void print(char* c) {
        cout << "Printing character: " << c << endl;
      }
};
```

But in Python only the last declared method will be used.

```python
class PrintData:
    def print(self, i: int):
        print(i)  # just get ignored
    def print(self, i: float):
        print(i)  # will have no effect
    def print(self, i: str):
        print(i)  # type of argument does not matter, only last declaration will be used
```

As usually in Python world there is a workaround or some way to implement any concept or idea. First approach is a straightforward simple implementation of writing logical conditions within method/function itself. Thanks to [keywords-only arguments](https://www.python.org/dev/peps/pep-3102/) we can force to explicitly provide parameters names for our arguments therefore emulating calls to functions with different signatures. You can also do the same manually checking `**kwargs` for the presence of desired arguments ([in case you use Python 2](https://github.com/pasztorpisti/kwonly-args)).

```python
class ResolverManual(object):
    def multiply(self, *, a=None, b=None):
        if a is None and b is None:
            print('Method called without arguments')
            return

        if a is None and b is not None:
            print('b is provided')
            return b

        if a is not None and b is None:
            print('a is provided')
            return a

        print('Both values are present. Product is')
        return a*b
```

Now we just need to invoke `multiply` method with desired set of arguments

```python
r1 = ResolverManual()
multiply1 = r1.multiply
print(multiply1())
print(multiply1(a=1))
print(multiply1(b=2))
print(multiply1(a=1, b=2))
```

In each branch of our logical if conditions we can provide a call to any internal method we want but essentially we will get something like this at the end

```
Method called without arguments
None
a is provided
1
b is provided
2
Both values are present. Product is
2
```

With a help of `functools` built-in module we can achieve almost the same behaviour. It contains [singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch) decorator allowing to call appropriate function based on the type of the first argument (therefore single) . You can define one generic function and register as many other function as you want with different types of the first argument and it will automatically dispatch a call to matched one.

```python
from functools import singledispatch


@singledispatch
def multiply2(a, b):
    print('Generic function for {a}, {b}'.format(a=a, b=b))


def multiply_float(a: float, b: float):
    print('Multiplying two floats: {a}x{b}'.format(a=a, b=b))
    return a*b


def multiply_lists(a: list, b: list):
    print('Cartesian product of {a} and {b}'.format(a=a, b=b))
    return sum([val_a*val_b for val_a in a for val_b in b])


multiply2.register(float, multiply_float)
multiply2.register(list, multiply_lists)
```

Optionally you can decorate each of your functions with _function.register(type)_ decorator (`@multiply2.register(complex)`) inplace instead of registering them later. To fully emulate overloading with dispatching based on types we can use [multipledispatch](https://github.com/mrocklin/multipledispatch) library which does the same but generalizes for any number of parameters (note, it's not the part of standard library).

```python
print(multiply2(3, 4))
print(multiply2(4.1, 5.2))
print(multiply2([1, 2, 3], [4, 5, 6]))
```

Invocation above will give us following output

```
Generic function for 3, 4
None
Multiplying two floats: 4.1x5.2
21.32
Cartesian product of [1, 2, 3] and [4, 5, 6]
90
```

In case you want to use single dispatch behaviour on the methods of your class you need to slightly modify the decorator. The problem is that it decides which registered function to call based on the type of a first argument and in case of a method our first argument will be always `self` instance.

```python
from functools import singledispatch, update_wrapper


def methdispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper
```

So our new `methdispatch` will substitute a call with actual first argument instead of a self and then just elevate the rest of the function. We can use this decorator as showed below

```python
class ResolverMethDispatch(object):
    @methdispatch
    def multiply(self, a, b):
        print('Generic method for {a}, {b}'.format(a=a, b=b))
        return '{a}x{b}'.format(a=a, b=b)

    @multiply.register(int)
    def multiply_int(self, a, b):
        print('Multiplying two ints: {a}x{b}'.format(a=a, b=b))
        return a*b

    @multiply.register(str)
    def multiply_str(self, a, b):
        print('Making string "{a}" {b} characters long'.format(a=a, b=b))
        return a*b
```

The next step is to instantiate our class and use the method as usually

```python
r3 = ResolverMethDispatch()
multiply3 = r3.multiply
print(multiply3([3], [4]))
print(multiply3(3, 4))
print(multiply3('a', 4))
```

You will not be surprised at this point because an output satisfies our expectations

```
Generic method for [3], [4]
[3]x[4]
Multiplying two ints: 3x4
12
Making string "a" 4 characters long
aaaa
```

There are two other very similar options based on classes that I like the most when trying to implement function overloading. The idea is to pass all the logic to either `__call__` or `__new__` magic method and implement all the logic within them. And the best thing about it is using as a regular function call. Lets see an example

```python
class _multiply4(object):
    def __call__(self, *args, **kwargs):
        if len(args) == 2:
            a, b = args
            if isinstance(a, int) and isinstance(b, int):
                return self._multiply_int(a, b)
            elif isinstance(a, float) and isinstance(b, float):
                return self._multiply_float(a, b)
            elif isinstance(a, str) and isinstance(b, int):
                return self._multiply_str(a, b)
        return self._multiply_generic(*args)

    def _multiply_generic(self, *args):
        print('Generic method for arguments: {}'.format(args))

    def _multiply_float(self, a: float, b: float):
        print('Multiplying two floats: {a}x{b}'.format(a=a, b=b))
        return a*b

    def _multiply_int(self, a: int, b: int):
        print('Multiplying two ints: {a}x{b}'.format(a=a, b=b))
        return a*b

    def _multiply_str(self, a: str, b: int):
        print('Making string "{a}" {b} characters long'.format(a=a, b=b))
        return a*b
multiply4 = _multiply4()
```

We define 4 different functions (1 default generic and 3 type specific) and make our decision in a `__call___` method. Then we instantiate our class to get a target callable that we can use in our code

```python
print(multiply4())
print(multiply4(5, 6))
print(multiply4(8.0, 9.1))
print(multiply4('d', 4))
```

As expected different functions will be called for different arguments based on our conditions

```
Generic method for arguments: ()
None
Multiplying two ints: 5x6
30
Multiplying two floats: 8.0x9.1
72.8
Making string "d" 4 characters long
dddd
```

The same concept but with a `__new__` will look like this

```python
class multiply5(object):
    def __new__(cls, *args, **kwargs):
        if len(args) == 2:
            a, b = args
            if isinstance(a, int) and isinstance(b, int):
                return cls._multiply_int(a, b)
            elif isinstance(a, float) and isinstance(b, float):
                return cls._multiply_float(a, b)
            elif isinstance(a, str) and isinstance(b, int):
                return cls._multiply_str(a, b)
        return cls._multiply_generic(*args)

    @classmethod
    def _multiply_generic(cls, *args):
        print('Generic method for arguments: {}'.format(args))

    @classmethod
    def _multiply_float(cls, a: float, b: float):
        print('Multiplying two floats: {a}x{b}'.format(a=a, b=b))
        return a*b

    @classmethod
    def _multiply_int(cls, a: int, b: int):
        print('Multiplying two ints: {a}x{b}'.format(a=a, b=b))
        return a*b

    @classmethod
    def _multiply_str(cls, a: str, b: int):
        print('Making string "{a}" {b} characters long'.format(a=a, b=b))
        return a*b
```

This way we don't need to instantiate a class and the usage remain the same

```python
print(multiply5(7, 10))
print(multiply5(8.0, 9.0))
print(multiply5('b', 4))
print(multiply5(3, 4, 5))
```

will give us predictable result

```
Multiplying two ints: 7x10
70
Multiplying two floats: 8.0x9.0
72.0
Making string "b" 4 characters long
bbbb
Generic method for arguments: (3, 4, 5)
None
```

### Final thoughts
I do not encourage to use this examples in a real code (besides singledispatch one). This demonstrates great flexibility of a language and can be a guide to some interesting concepts within it but as[ Zen of Python](https://www.python.org/dev/peps/pep-0020/) states

> There should be one - and preferably only one - obvious way to do it.

Basically it means that in case you need to implement anything "hacky" there is something missing in the design of your program/algorithm and it should be revised. Tools (as well as algorithms/data structures) matters so choose them wisely but do not stop to obtain new knowledge implementing such a tricky things.

### Resources
* [Multiple dispatch article](http://matthewrocklin.com/blog/work/2014/02/25/Multiple-Dispatch)
* [PEP on overloading](https://legacy.python.org/dev/peps/pep-3124/)
