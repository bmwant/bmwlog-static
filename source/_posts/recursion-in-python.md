---
title: Recursion in Python
tags: []
language: en
author: Misha Behersky
date: 2021-09-07 21:00:24
---


![y-combinator](/images/y_combinator.png)
> **NOTE**: All the code below has been tested using Python **3.8.12** and some of the syntax might not be compatible with older versions.

One of the main selling points of any functional programming language is recursion or rather an elegant way you can implement recursive function using one's syntax. In this article I want to show that Python can be easily adapted to be written in a functional way proving it's a trully multi-paradigm language.
Everyone knows classical example of recursion using [Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number), so let's take a look at the corresponding Python code for it.

```python
def fib(n: int) -> int:
    if n == 0 or n == 1:  # base case
        return n

    return fib(n-2) + fib(n-1)
```

We have a function accepting a number and returning an element of the Fibonacci sequence corresponding to that number. Each recursive function should have a **base case** (also known as **edge case**) and essentially it's a branch of code which halts or returns something immediatelly without making any subsequent recursive calls. Then we have two recursive function calls calculating two previous numbers of the sequence and basically that corresponds to the definition where each number is just a sum of two prior ones in a sequence.
Most of the functional languages are also known to be [statically typed](https://en.wikipedia.org/wiki/Type_system#STATIC), so we are also using type annotations within our code examples to make them look more *functional-ish*.

### Minimum efforts

Now let's implement a couple of frequently used common functions to illustrate such things can be implemented concisely in a recursive fashion.

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
The biggest element of the whole list is either current one or the biggest element from the rest of the sequence. Here we use [list destructuring](https://www.python.org/dev/peps/pep-3132/) to seamlessly extract first element from the list as well as its tail into two different variables.
Same result can be accomplished using approach below (in case you are not comfortable with such a syntax):

```python
arr = [1, 2, 3, 4]
x, tail = arr.pop(0), arr
# (1, [2, 3, 4])
```

Another option is to use [slices](https://docs.python.org/3/library/functions.html#slice) on the list:

```python
arr = [1, 2, 3, 4]
x, tail = arr[0], arr[1:]
# (1, [2, 3, 4])
```

Same logic applies to the `minimum` function, but here instead of comparison we invoke [min](https://docs.python.org/3/library/functions.html#min) built-in function.

```python
from typing import List

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

* `elem` - for the value `val` provided and a list `arr` it returns whether a list contains that element

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

> As an extra exercise you can start by taking any function from [itertools](https://docs.python.org/3/library/itertools.html) module and trying to come up with equivalent recursive code. Most of the functions there have rough code implementation provided within the documentation page above, so it would be much easier to understand what kind of logic you are trying to achieve.

### Quick, sort!

There are a lot of [graph traversal](https://en.wikipedia.org/wiki/Graph_traversal) algorithms which are easier to implement using recursive functions as well as this example of [quicksort](https://en.wikipedia.org/wiki/Quicksort) algorithm because their own definitions are declared in recursive terms. To accomplish sorting we start with *pivot* element which in the simplest case is just a first element of our list and place it between two partitions: first one is an array of sorted elements which are less or equal to our *pivot* and the second one is an array of sorted elements greater than that.

```python
def quicksort(arr):
    if not arr:
        return []
    x, *tail = arr
    smaller_sorted = quicksort([t for t in tail if t <= x])
    bigger_sorted = quicksort([t for t in tail if t > x])
    return [*smaller_sorted, x, *bigger_sorted]
```

As you can see there is nothing complex about recursion and some implementations can be even simpler then their iterative counterparts. Sometimes recursive code might be a bit harder to debug, so when in doubt always stick with the solution that is easier for you to understand and maintain. Otherwise go ahead and implement your new feature using recursive functions. Happy coding!

### Resources

* [RealPython article on recursion](https://realpython.com/python-recursion/)
* [Same functions implemented in Haskell](http://learnyouahaskell.com/recursion)
* [Y-combinator (advanced)](https://en.wikipedia.org/wiki/Fixed-point_combinator)
* [Recursion schemes (advanced)](http://comonad.com/reader/2009/recursion-schemes/)
* [Great talk on lambda calculus from David Beazley](https://youtu.be/pkCLMl0e_0k)
