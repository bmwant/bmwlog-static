---
title: Публікація модуля на PyPI
date: 2015-05-27 10:40:43
tags: [pypi, pip, distutils]
author: Misha Behersky
language: ua
---

Отже, ви написали модуль, яким хочете поділитися з іншими, зробити свій вклад в розвиток Python-а, або просто хочете мати можливість встановлювати свій модуль чере pip. [PyPI (Python Packages Index)](https://pypi.python.org/pypi) - це офіційний репозиторій модулів для Python. Для початку необхідно зареєструватися там. Після цього потрібно підготувати модуль (для початку вважаємо, що у нас є модуль `mymodule.py`, де міститься весь потрібний функціонал): за допомогою [distutils](https://docs.python.org/3/library/distutils.html) створити скрипт встановлення. Створюємо файл `setup.py` з подібним вмістом

```python
from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='MyModule',
      version='1.0',
      py_modules=['mymodule'],
      author='Most Wanted',
      author_email='bmwant@gmail.com',
      url='http://bmwlog.pp.ua',
      description='Short module description',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
      ],
      long_description=long_description,
)
```

Вказуємо назву, версію, інформацію про автора та короткий опис. Якщо у вас файл детального опису у форматі [reStructuredText](http://docutils.sourceforge.net/rst.html) (такий часто використовують на Github, якщо потрібно звідкись взяти приклад) - в *long_description* записуємо текст з цього файлу або просто вводимо його вручну. Особливу увагу варто приділити *classifiers*: це дозволяє віднести ваш модуль до певної категорії, що допоможе знайти його іншим і вибрати серед аналогів. Список класифікаторів можна [подивитися тут](https://pypi.python.org/pypi?%3Aaction=list_classifiers). Якщо є проблеми з вибором ліцензії, можна не вказувати її взагалі або скористатися [помічником](http://choosealicense.com). В більшості випадків підійде [MIT License](http://en.wikipedia.org/wiki/MIT_License). Коли файл готовий можна приступити до створення архіву для встановлення.

```bash
$ python setup.py check
$ python setup.py sdist
```

Це створить в папці dist архів вашого модуля з усіма необхідними файлами.

Якщо все пройшло успішно - можна завантажити ваш модуль в репозиторій

```bash
$ python setup.py sdist upload
```

Потрібно буде ввести логін і пароль вашого зареєстрованого акаунта (вам запропонують зберегти ці параметри у файлі <em>.pypirc</em>, щоб не вводити їх кожного разу) - і все: ваш модуль тепер доступний всім.

```bash
$ pip install mymodule
```

Отак просто! Після оновлення модуля - змінюємо версію і статус розробки (якщо потрібно) і вводимо команду

```bash
$ python setup.py sdist upload
```

Тепер, коли є декілька версій програми, можна встановлювати конкретну або оновлюватися до останної за допомогою команд

```bash
$ pip install mymodule==1.2
$ pip install mymodule --upgrade
```

В наступній статті я хочу більш детально описати скрипт `setup.py`, ознайомити з форматом написання *README*-файлів та публікацією пакетів (більш складних модулів та додаткових файлів).

Вдалої розробки.
