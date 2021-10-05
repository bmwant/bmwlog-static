---
title: Python. Подорожі в часі
date: 2015-08-28 14:54:44
tags: [python, time, datetime, calendar]
author: Misha Behersky
language: ua
---

В цій статті я хочу розказати про основні операції з датами/часом, які дозволяє здійснювати Пайтон за допомогою модулів стандартної бібліотеки. Мова бути йти про функції з використанням модулів [datetime](https://docs.python.org/3.4/library/datetime.html), [calendar](https://docs.python.org/3.4/library/calendar.html) та [time](https://docs.python.org/3.4/library/time.html).

![marty](/old/article/83fa02bc24fd39908afbea54f501e061.jpg)

Почнемо з перетворень між датами та їх представленнями у вигляді рядків.

Надалі будемо говорити про дату як про обєкт типу `datetime.datetime`, який містить такі атрибути: рік, місяць, день, година, хвилина, секунда, мікросекунда та інформація про часовий пояс.

### Перетворити рядок заданого формату в дату

```python
import datetime
date_str = '23/10/2016 15:32'
date_format = '%d/%m/%Y %H:%M'
result = datetime.datetime.strptime(date_str, date_format)
```

Щоб отримати інформацію стосовно специфікаторів формату дати можна звернутися до [офіційної документації](https://docs.python.org/3.4/library/datetime.html#strftime-strptime-behavior) або до [цієї класної шпаргалки](http://strftime.org).

### Перетворити дату в рядок заданого формату

```python
date = datetime.datetime.now()
date_format = '%x %X'
result = date.strftime(date_format)
```

Даний код перетворить поточний *даточас* в представлення дати та часу відповідно до вашої поточної локалізації.

### Отримати початок дня для дати

```python
result = date.replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
```

### Отримати дату без інформації про часовий пояс

```python
result = date.replace(tzinfo=None)
```

Це може знадобитися, щоб порівнювати дати з датами, що не мають інформації про часовий пояс, додавати чи віднімати їх. Але будьте уважні, бо таким способом можна втратити кілька годин).

### Отримати перше число попереднього місяця

```python
date = datetime.date.today()  # or any another date you want
first_day = datetime.date(day=1, month=date.month, year=date.year)
prev_month = first_day - datetime.timedelta(days=1)
result = datetime.datetime(year=prev_month.year, month=prev_month.month, day=1)
```

Спочатку отримуємо перший день для місяця нашої дати. Потім віднімаємо від нього один день - так ми перейдемо на попередній місяць. І наостанок, сформуємо об'єкт дати для першого числа отриманого місяця. Такі маніпуляції потрібні, щоб не робити додаткових перевірок на кількість днів у місяці, перший/останній місяць року.

### Перетворити time_struct/timestamp в datetime

```python
time_struct = time.strptime(date_str, date_format)
date = datetime.datetime.fromtimestamp(time.mktime(time_struct))
```

mktime спочатку перетворить *часоструктуру* в кількість секунд, що пройшли з початку [Епохи](https://en.wikipedia.org/wiki/Unix_time) (1 січня 1970 року), а потім створить новий об'єкт дати.

### Порівняти date та datetime дати

Якщо у вас є об'єкт, отриманий, наприклад, як `datetime.date.today()` і його потрібно порівняти з екземпляром класу `datetime.datetime`, то приведемо останній з використанням методу `date()`

```python
the_date = datetime.datetime.now()
the_date = the_date.replace(day=the_date.day+1)
today = datetime.date.today()
the_date > today  # TypeError: can't compare datetime.datetime to datetime.date
the_date.date() > today  # True
```

### Перетворити дату в кількість секунд/мілісекунд

```python
date_seconds = time.mktime(date.timetuple())
mls = date_seconds * 1000
result = int(mls)
```

### Порівняти дві дати за форматом

Таке може знадобитися, якщо потрібно перевірити, чи співпадає рік і день в дат з різними місяцями і часом (не обов'язково цей приклад, порівнювати можна за будь-яким форматом)

```python
date_one  # 2015-08-28 15:57:29.615660
date_two  # 2015-07-28 11:32:57.294810
date_format = '%Y %d'
formatted_one = date_one.strftime(date_format)
formatted_two = date_two.strftime(date_format)
result = formatted_one == formatted_two
```

### Інформація про дату

Отримати інформацію про дату: день, місяць, рік, номер дня у році, номер дня тижня, номер тижня у році, чи високосний рік.

```python
print('Day number: %s' % date.day)
print('Month number: %s' % date.month)
print('Current year: %s' % date.year)
print('Day of the year: %s' % date.timetuple().tm_yday)
print('Day of week number: %s' % date.isoweekday())
print('Week of year number: %s' % date.isocalendar()[1])
print('Is leap year: %s' % calendar.isleap(date.year))
```

### І наостанок

Надрукувати календар для обраного року в консоль

```python
import calendar
calendar.prcal(2015)
```

Сніпет коду до всіх прикладів можна знайти [тут на бітбакеті](https://bitbucket.org/bmwant/workspace/snippets/98LMK/python-time-travelling).

### Ресурси

Додаткові модулі, які полегшать роботу з датами

* [dateutil - конвертації, парсинг, арифметика над датами](http://labix.org/python-dateutil)
* [pytz - модуль для роботи з часовими поясами](http://pytz.sourceforge.net)
* [delorean - спрощена робота з датами плюс генерація дат](http://delorean.readthedocs.org/en/latest/)
* [Стаття про time в "модулі тижня" (PyMOTW)](https://pymotw.com/2/time/)
