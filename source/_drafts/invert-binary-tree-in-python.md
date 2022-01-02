---
title: Invert binary tree in Python
tags: [python, algorithms, snippets]
author: Misha Behersky
language: en
---

### Problem

Python `3.10` is used throughout the article.

### Data structures

First of all we need a data structure which represents a tree and two helper functions:
`generate_tree` to create a target tree we plan to work with and
`print_tree` to visualize the result and verify our solution works as intended.

To represent a tree we need to define only one class that corresponds to a *node*. Each node stores some value/identificator as well as pointers to its children or `None` in case of *leaf* nodes. An arbitrary variable assigned to the root node will state as a tree within our code.

```python
class Node(object):
    def __init__(self, value: int = None):
        self.value = value
        self.left: Node = None
        self.right: Node = None

    def __str__(self):
        return f'{self.value}'

    def __repr__(self) -> str:
        return self.__str__()
```

```python
from typing import Optional

counter = 0

def generate_tree(levels: int) -> Optional[Node]:
    global counter
    if levels == 0:
        return None

    counter += 1
    node = Node(counter)
    node.left = generate_tree(levels-1)
    node.right = generate_tree(levels-1)
    return node
```

### Recursive solution


### Non-recursive solution

### Resources

* [Article on educative.io](https://www.educative.io/edpresso/how-to-invert-a-binary-tree)
* [Recursive solution souce code](https://github.com/bmwant/jaaam/blob/main/invert_binary_tree.py)
* [Non-recursive solution souce code](https://github.com/bmwant/jaaam/blob/main/invert_binary_tree_queue.py)
* [Stack-based solution source code](https://github.com/bmwant/jaaam/blob/main/invert_binary_tree_stack.py)
