---
title: FreeBSD фікси помилок
date: 2014-12-20 15:27:12
tags: [freebsd, bugs]
author: Misha Behersky
language: ua
archived: true
---

> pkg_add: unable to fetch / unable to get

Причиною помилки є неправильна змінна **PACKAGESITE**. [Тут](ftp://ftp.freebsd.org/pub/FreeBSD/ports/) можна знайти правильний лінк для вашої системи. Для `FreeBSD 9.0` з `bash` команда виглядає таким чином:

```bash
$ export PACKAGESITE=ftp://ftp.freebsd.org/pub/FreeBSD/ports/i386/packages-9-stable/Latest/
```

Дізнатися версію ОС можна командою: `uname -a`.
Виводимо нову змінну і перевіряємо коректну роботу:

```bash
$ echo $PACKAGESITE
$ pkg_add -r nginx
```

> urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]

Причиною є те, що у нових версіях Python за замовчування CA сертифікат шукається в папці `/etc/ssl/cert.pem`.
Фіксимо командою

```bash
$ ln -s /usr/local/etc/ssl/cert.pem /etc/ssl/cert.pem
```
