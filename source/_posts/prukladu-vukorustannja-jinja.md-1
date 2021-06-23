---
title: Приклади використання Jinja2
date: 2014-10-26 22:51:17
tags: [jinja2, python, filters]
author: Misha Behersky
language: ua
---

### Пишемо власний фільтр

Шаблонізатор Jinja2 має багато вбудованих фільтрів, серед яких:

* `capitalize(s)` Переводить першу літеру рядка в верхній регістр, всі інші будуть в нижньому.

* `dictsort(value, case_sensitive=False, by='key')` Дозволяє сортувати словник за ключами або значеннями.

* `filesizeformat(value, binary=False)` Форматує вивід розміру файлу у зрозумілий вигляд (13 kB, 4.1 MB, 102 Bytes).

* `first(seq)` Повертає перший елемент послідовності.

* `round(value, precision=0, method='common')` Округляє значення з заданою точністю звичайний способом округлення (*common*), завжди до більшого значення (*ceil*) або до меншого (*floor*).

Повний список можна знайти в офіційній документації [тут](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters).

Фільтр - це звичайна функція, яка приймає ліву сторону як перший аргумент і всі інші параметри як додаткові аргументи. Наприклад, нам потрібно, щоб фільтр додавав до значення знак **$**, якщо це число, в іншому випадку дописував слово **dollars**. Так буде виглядати наш фільтр:

```python
def dollars(value):
    try:
        new_value = str(int(value)) + '$'
    except ValueError:
        new_value = value + ' dollars'
    return new_value
```

Тепер потрібно додати фільтр до нашого середовища - і можна його використовувати:

```python
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('yourapplication', 'templates'))
env.filters['dollars'] = dollars
```

В шаблоні сторінки просто пишемо `{{ value | dollars }}`

```python
template = env.get_template('test.html')
print(template.render(value='one hundred'))
print(template.render(value='100'))
```

поверне відповідно `one hundred dollars` і `100$`.

### Ресурси

* [Офіційна документації Jinja2](http://jinja.pocoo.org/docs/dev/api/)
