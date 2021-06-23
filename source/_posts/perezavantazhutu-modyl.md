---
title: Перезавантажити модуль
date: 2016-02-02 20:21:04
tags: [python, console, module]
author: Misha Behersky
language: ua
---

Часто виникає ситуація, коли потрібно протестити функцію з деякого модуля. Найпростіше досягти цього, відкривши інтерпретатор і в [REPL-режимі](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) зробити необхідний виклик

```bash
$ python
>>> import module_name
>>> module_name.test_function(5)
10
```

Але якщо функція модифікована (був оновлений код), ще один виклик все одно поверне той же результат, що очевидно є небажаною для нас (хоча і правильною, очікуваною) поведінкою. Найпростіший варіант - це перезапустити інтерпретатор

```bash
>>> quit()
$ python
>>> ...
```

і виконати ті ж самі команди, що є не дуже зручно. Тому рішення для **Python 2**:

```python
>>> import module_name
>>> module_name.test_function(5)
10
>>> reload(module_name)
>>> module_name.test_function(5)
25
```

для **Python 3**:

```python
>>> import imp
>>> import module_name
>>> module_name.test_function(5)
10
>>> imp.reload(module_name)
>>> module_name.test_function(5)
25
```

дозволить зекономити час і прискорити тестування коду, що модифікується.

### Ресурси

* [Модуль imp для третьої версії](https://docs.python.org/3/library/imp.html#imp.reload)
