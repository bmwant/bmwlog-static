---
title: Recursion in Python
tags: [python, recursion, functional]
author: Misha Behersky
language: en
---

One of the main selling points of any functional programming language is recursion or rather an elegant way you can implement recursive function using one's syntax. In this article I want to show that Python code style can be easily adapted to be written in a functional way proving it's trully multi-paradigm language.
Everyone knows classical example of recursion using [Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number), so let's take a look at the corresponding Python code for it.

```python
def fib(n: int) -> int:
    if n == 0 or n == 1:  # base case
        return n

    return fib(n-2) + fib(n-1)
```

We have a function accepting a number and returning an element of the Fibonacci sequence corresponding to that number. Each recursive function should also have a **base case** (also known as **edge case**) and essentially it's a branch of code which halts or returns something immediatelly without making any subsequent recursive calls. Then we have two recursive function calls calculating two previous numbers of the sequence and basically that corresponds to the definition where each number is just a sum of two prior ones in a sequence.
Most of the functional languages are also known to be [statically typed](https://en.wikipedia.org/wiki/Type_system#STATIC), so we are also using type annotations within our code examples to make them look more *functional-ish*.

###

Now let's implement a couple of frequently used common functions to illustrate that ... can be implemented concisely in a recursive fashion.

Our first subject is `maximum` / `minimum` function returning target element from the list.

```python
def maximum(arr):
    if not arr:
        raise ValueError('Cannot find maximum in an empty list')

    if len(arr) == 1:
        return arr[0]

    x, *tail = arr
    max_tail = maximum(tail)
    return x if x > max_tail else max_tail
```

As usually we start from a base case knowing that maximum element of the list containing only one element is the element itself.
The biggest element of the whole list is either current one or the biggest element from the rest of the sequence. Here we use
[list destructuring](https://www.python.org/dev/peps/pep-3132/) to seamlessly extract first element from the list and its tail.


https://docs.python.org/3/library/functions.html#slice

```python
arr = [1, 2, 3, 4]
x, tail = arr.pop(0), arr
# (1, [2, 3, 4])
```

Same logic applies to the `minimum` function, but here instead of comparison we invoke [min](https://docs.python.org/3/library/functions.html#min)
built-in function.

```python
def minimum(arr: List[int]) -> int:  # type annotations for clarity
    x, *tail = arr  # list unpacking
    if not tail:  # base case
        return x

    return min(x, minimum(tail))  # recursive call
```

### Rewrite everything with recursion

Below you can find couple of extra functions just to demonstrate how similar their structure is and how fluently any structure can be translated into recursive calls.

* `replicate` takes a number `n` and a value `val` and returns a list containing `n` copies of the same `val` value

```python
def replicate(n, val):
    if n <= 0:
        return []

    return [val, *replicate(n-1, val)]
```

Example invocation:

```python
>>> replicate(3, 42)
[42, 42, 42]
```

* `take` - given a number `n` and a list `arr` it returns first `n` elements from that list

```python
def take(n, arr):
    if n <= 0 or not arr:
        return []

    x, *tail = arr
    return [x, *take(n-1, tail)]
```

Example invocation:

```python
>>> take(3, [0, 1, 2, 3, 4])
[0, 1, 2]
>>> take(5, [])
[]
```

* `elem` for the value `val` provided and a list `arr` it returns whether a list contains that element

```python
def elem(val, arr) -> bool:
    if not arr:
        return False

    x, *tail = arr
    if val == x:
        return True
    return elem(val, tail)
```

Example invocation:

```python
>>> arr1 = [1, 2, 3]
>>> arr2 = ['a', 'b', 'c', 'd']
>>> elem(0, arr1)
False
>>> elem('d', arr2))
True
```

* `reverse` simply reverses a list

```python
def reverse(arr):
    if not arr:
        return []

    x, *tail = arr
    return [*reverse(tail), x]
```

Example invocation:

```python
>>> reverse([1, 2, 3, 4, 5])
[5, 4, 3, 2, 1]
>>> reverse([])
[]
```

* `zip` takes two lists and *zips* them together. It returns one list each element being a pair of matching elements from input lists. In case one list is shorter the resulting list would not contain items from the longer list that do not match with anything in the end.

```python
def zip(xs, ys):
    if not xs or not ys:
        return []

    x, *x_tail = xs
    y, *y_tail = ys
    return [(x, y), *zip(x_tail, y_tail)]
```

Example invocation (resulting list does not contain `d` element as it doesn't match with anything from the first list):

```python
>>> arr1 = [1, 2, 3]
>>> arr2 = ['a', 'b', 'c', 'd']
>>> zip(arr1, arr2)
[(1, 'a'), (2, 'b'), (3, 'c')]
```

> itertools examples

### Quick, sort!

```python
def quicksort(arr):
    if not arr:
        return []
    x, *tail = arr
    smaller_sorted = quicksort([t for t in tail if t <= x])
    bigger_sorted = quicksort([t for t in tail if t > x])
    return [*smaller_sorted, x, *bigger_sorted]
```

### Resources

* [RealPython article on recursion](https://realpython.com/python-recursion/)
* [Recursion schemes (advanced)](http://comonad.com/reader/2009/recursion-schemes/)
