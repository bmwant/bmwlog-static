---
title: node js автостарт додатку з rc.d в FreeBSD
date: 2018-06-07 09:55:16
tags: [freebsd, nodejs, foreverjs, rcd]
author: Misha Behersky
language: ua
---

Нещодавно виникла необхідність запустити веб-додаток на [Express](http://expressjs.com) (node js) автоматично при старті та перезапуску системи (FreeBSD 10.3). До цього все запускалося за допомогою чудового менеджера процесів для ноди - [foreverjs](https://github.com/foreverjs/forever). Він чудово працює з дочірніми процесами і виконує свої функції (старт, перезапуск, перегляд логів, рестарт при зміні коду), але не запускається автоматично з операційною системою. Рішенням став демон системи, що виконує скрипти автозапуску під час старту - [rc.d](https://www.freebsd.org/doc/en_US.ISO8859-1/articles/rc-scripting/).

Проста конфігурація додатку для forever

```json
{
  "uid": "myapp",
  "append": true,
  "watch": true,
  "script": "app.js",
  "sourceDir": "/home/user/myapp"
}
```

І rc-скрипт який буде відповідати за запуск

```bash
#!/bin/sh

# $FreeBSD$
#
# PROVIDE: myapp
# REQUIRE: LOGIN
# KEYWORD: shutdown

. /etc/rc.subr

name="myapp"
forever="/usr/local/bin/node /usr/local/bin/forever"
workdir="/home/user/myapp"
script="app.js"

rcvar=`set_rcvar`

start_cmd="start"
stop_cmd="stop"
restart_cmd="restart"

load_rc_config $name
eval "${rcvar}=\${${rcvar}:-'NO'}"

start()
{
  su - user -c \
  "NODE_ENV=production \
  PORT=3344 \
  ${forever} start ${workdir}/forever_config.json"
}

stop()
{
  su - user -c "${forever} stop myapp"

}

restart()
{
  su - user -c "${forever} restart myapp"
}

run_rc_command "$1"
```

Два важливих моменти:

* За допомогою цього скрипта можна виконувати запуск від будь-якого користувача, не лише root-а. Для цього в функціях start/stop/restart перед командою додатково є префікс `su - user -c`.
* Щоб передати змінні оточення - задаємо їх перед командою. Наприклад, перевизначаю порт для запуску `PORT=3344`

Все інше залишаємо без змін, замінюючи назву додатку та шлях до робочої директорії. Копіюємо цей файл в `/usr/local/etc/rc.d` і не забуваємо додавати права на виконання файлу.

```bash
$ sudo chmod +x /usr/local/etc/rc.d/myapp
```

Тепер можна користуватися всіма плюшками сервісу

```bash
$ sudo service myapp restart
```

### Ресурси

* [NodeJs Startup Script for FreeBSD](https://bieker.ninja/2014/04/23/nodejs-startup-script-for-freebsd.html)
* [Схожа стаття на Хабрі](https://habrahabr.ru/post/137857/)
