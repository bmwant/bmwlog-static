---
title: Beware when using dict.keys() and dict.values()
date: 2018-12-05 13:28:53
tags: [python, dict, ordered, bug]
author: Misha Behersky
---

Starting with Python3.7 `dict.keys()` and `dict.values()` preserves an insertion order [[1](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)] [[2](https://mail.python.org/pipermail/python-dev/2017-December/151283.html)] [[3](https://docs.python.org/3/library/stdtypes.html#typesmapping)]. 

That's not true for older versions, so the code below
```
data = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
}

keys = ['one', 'two', 'three', 'four']
values = [1, 2, 3, 4]

data_keys = list(data.keys())
data_values = list(data.values())
k_equals = data_keys == keys
v_equals = data_values == values
if not k_equals:
    print('wrong keys', data_keys)
if not v_equals:
    print('wrong values', data_values)
```
might show you an output notifying about unexpected order of items. The tricky part is that it _might_ give you correct result in some cases (on your dev environment) and definitely will give you wrong result in other cases (production env).

Consider the following example

```
process_data = lambda x: x**2

key_index = 1 # I want a second element
key = data_keys[key_index]
# pass value to another function
print(process_data(data[key]))
```
It will give you inconsistent results between run making your code unreliable.

> Note that you can rely matching between `keys` and `values`

For example the code below will work

```
def get_index_of(number):
    return data_keys.index(number)

process_data = lambda x: x**2

key_index = get_index_of('two') # I want a second element
key = data_keys[key_index]
# pass value to another function
print(process_data(data[key]))
```

That means you still can safely use any index to value conversions keeping in mind only the fact you cannot be sure about the order of elements in these containers. But when in doubt make sure to use [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict).

Happy coding!