---
title: Кольоровий текст в консолі
date: 2016-07-24 16:29:49
tags: [python, utils, console]
author: Misha Behersky
language: ua
---

Коли потрібно виводити багато тексту в консоль, хочеться мати можливість зробити акцент на деяких більш важливих рядках (змінити колір, додати фон, зробити [жирним](http://pikabu.ru/story/shutki_pro_tvoyu_zhirnuyu_mamu_1834442)). Для цього я дуже зручна бібліотека [py-term](https://github.com/gravmatt/py-term)

```bash
$ pip install py-term
```

сумісна з другим і третім Пайтоном.

Простий приклад використання

```python
import term

term.write('Will be in ')
term.write('one line\n', term.bold)

term.writeLine('Custom color', term.green)

text = term.format('And custom background', term.white, term.bgblue)
term.writeLine(text)

# Clear text from color escape sequences
formatted = text.encode()
clear = term.strip(text)
print(formatted)
print(clear)
```

![example](/old/article/06e9f736ceae3a0b9858c8098afeacc7.png)

Також серед доступних можливостей: позиціонування курсору, вирівнювання тексту, очищення екрану, очищення певного рядка, встановлення довільного заголовку вікна.

### Список доступних кольорів для тексту

![text colors](/old/article/6f90e79a88e8365e96c9ec2bd64ee166.png)

### Список доступних кольорів для фону

![background colors](/old/article/51c9a8560ecf3dfbbba630f606b92d27.png)
