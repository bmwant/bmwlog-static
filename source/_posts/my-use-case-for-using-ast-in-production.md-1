---
title: My use case for using AST in production
date: 2017-08-08 15:21:55
tags: [python, ast, cli, click]
author: Misha Behersky
language: en
---

I am an advocate about not using metaclasses, inspect/ast modules and other cool features in production. In 99% cases it's a marker of some workaround/patch or just poor architecture. But recently I had a case which pushed me to use [AST](https://docs.python.org/2/library/ast.html) module. In short I have a huge list of environment variables which should be reused by other script within docker container. I write that file using bash script and then invoke a docker run command. The issue is that all the params is defined in ActiveRecord class (representing a model) and in CLI-file (which is used to create such an instance from envrionment variables). When creating envrironment file in need to define all the properties once again in the script (more that 30 items) and it&#39;s another place where errors can be hiding and which you need to edit while adding new attribute to you model. So to automatically discover which variables should I save from environment I created a helper python script. I cannot import the module where all the fields defined and I cannot use inspect module or any third-party dependency as all the requirements are only available within container. So the only option left is to parse target file in some way. For this we have built in feature presented as abstract syntax tree. It can parse your source code file and build a tree-like structure representing relations between your code units.

Building a tree requires almost nothing

```python
import ast

filename = 'main.py'
with open(filename) as f:
    tree = ast.parse(f.read())
```

Next step is to traverse that tree looking for nodes you want to do something with. We are looking for options like these

```python
import click

option_one = click.option(
    '--option_one',
    required=True,
    envvar='option_one',
    help='Some field'
)

option_two = click.option(
    '--option_two',
    required=True,
    envvar='option_two',
    help='Another field'
)
```

So, basically we search assignments followed by `option` calls. Then we check all the keywords for that call to find `envvar` ones.

```python
result = []
for stmt in ast.walk(tree):
    if isinstance(stmt, ast.Assign):
        if isinstance(stmt.value, ast.Call) and stmt.value.func.attr == 'option':
            option = stmt.targets[0].id
            for kwd in stmt.value.keywords:
                if kwd.arg == 'envvar':
                    result.append(kwd.value.s)
```

You may also want to check option to fulfill some criteria if you have some other code within that file.

Now you can inspect your main **CLI** file and save required envrionment variables in the same way.

```python
result = []
for stmt in ast.walk(tree):
    if isinstance(stmt, ast.Attribute):
        if isinstance(stmt.value, ast.Name) and stmt.value.id == 'click_options':
            result.append(stmt.attr)
```

And just to have the full picture here is the `cli.py` file that is the actual entrypoint.

```python
import click
import click_options


@click.command(help='Entrypoint')
@click_options.option_one
@click_options.option_two
def main(**kwargs):
    create_record(**kwargs)


if __name__ == '__main__':
    main()
```

You can adapt this code to work with more complex statements and to follow the structure that you have in your own code.

The downsides of this approach is that ast may change between python versions and therefore code might be not compatible between releases. Also refactor will require complete rewrite of the handling logic. I suggest this example more like hands on with ast, but not the solution for the issue described.

### Summary

Understanding how AST works may allow you to write some cool stuff like [code optimization/modification](http://faster-cpython.readthedocs.io/ast_optimizer.html) before compilation or static analysis code checker (e.g. [plugins for flake8](https://julien.danjou.info/blog/2015/python-ast-checking-method-declaration)). Try playing with this library but as always think twice before applying your knowledge to some production code because it's really one of those places that might create you additional headache in future. Take care.
