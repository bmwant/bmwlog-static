---
title: Розділити словник на частини
date: 2015-12-30 00:48:10
tags: [python, hints, dict]
author: Misha Behersky
language: ua
archived: true
---

Сьогодні виникла потреба поділити словник (dict) на дві частини. Задача зводиться до перетворення у список, який потім ділиться на дві частини, і створення з цих частин знову словників. Словник перетворюється у список парами (tuple) *ключ-значення*.

```python
big_dict = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
}


big_dict_list = list(big_dict.items())

left_list_dict = big_dict_list[:len(big_dict_list)//2]
right_list_dict = big_dict_list[len(big_dict_list)//2:]

part_one = dict(left_list_dict)
part_two = dict(right_list_dict)
```

Порядок елементів в словнику не визначений, тому якщо потрібні частини, поділені за певними критеріями, необхідно здійснити додаткове сортування списку. Якщо кількість елементів непарна - перший словник буде на один елемент менший (слайс не включає праву межу). В результаті отримаємо два словники

```python
{1: 'one', 2: 'two', 3: 'three'}
{4: 'four', 5: 'five', 6: 'six'}
```

Потім я вирішив узагальнити даний код для поділу на довільну кількість частин. Можна користуватися цією узагальненою функцією:

```python
import math


def split_dict(big_dict: dict, parts: int):
    big_dict_list = list(big_dict.items())
    total_elems = len(big_dict_list)
    if parts > total_elems:
        raise ValueError('You cannot divide into parts more than elements you have')

    elems_in_part = math.ceil(total_elems/parts)
    for i in range(parts):
        yield dict(big_dict_list[i*elems_in_part:(i+1)*elems_in_part])
```

Оскільки не завжди буде виконуватися ділення націло (в кожній частині однакова кількість елементів), можна зробити щоб всі частини були однакові і одна містила залишок

```python
def split_dict(big_dict: dict, parts: int):
    big_dict_list = list(big_dict.items())
    total_elems = len(big_dict_list)
    if parts > total_elems:
        raise ValueError('You cannot divide into parts more than elements you have')

    elems_in_part = total_elems // parts
    for i in range(parts-1):
        left = i*elems_in_part
        right = (i+1)*elems_in_part
        yield dict(big_dict_list[left:right])

    # Return the rest of the dict anyway
    yield dict(big_dict_list[(parts-1)*elems_in_part:])
```

Для другого (я зараз про версію Пайтона) потрібно позабирати анотації типів і немає потреби явно приводити елементи словника до списку, а в першому варіанті привести до цілого числа `int` результат `math.ceil`.
