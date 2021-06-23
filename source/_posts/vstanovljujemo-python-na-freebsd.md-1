---
title: Встановлюємо Python на FreeBSD
date: 2014-10-20 21:19:14
tags: [freebsd, python]
author: Misha Behersky
language: ua
---

Спочатку виконуємо команду `wget` для завантаження архіву. Замість `2.7.8` можна вказати останню версію, доступну на даний момент.

```bash
$ wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz --no-check-certificate
$ tar -xzvf Python-2.7.8.tgz
$ cd Python-2.7.8
$ ./configure
$ make
$ make install
```

Далі вводимо команду `python` і в консолі повинні отримати повідомлення від інтерпретатора з номером щойно встановленої версії Python-а.

Потім встановлюємо *pip* та *virtual environment*

```bash
$ cd /usr/ports/devel/py-pip/ && make install clean
$ pip install virtualenv
```

Щоб почати роботу з проектом виконуємо команди

```bash
$ cd /path/to/your/project
$ virtualenv venv
$ source venv/bin/activate
```

По закінченню вводимо команду `deactivate`

### Ресурси

* [Перевірити останню версію Python](https://www.python.org/downloads/)
