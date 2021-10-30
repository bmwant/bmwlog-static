---
title: Встановлюємо MongoDB на FreeBSD
date: 2015-02-01 14:19:03
tags: [mongodb, freebsd]
author: Misha Behersky
language: ua
---

Встановлюємо _Mongo_ з портів

```bash
$ cd /usr/ports/databases/mongodb/
$ make install clean
```

Додаємо параметри автозапуску в `/etc/rc.conf`

```ini
mongod_enable="YES"
mongod_config="/usr/local/etc/mongodb.conf"
mongod_dbpath="/var/db/mongodb"
```

Налаштовуємо файл конфігурації `/usr/local/etc/mongodb.conf`

```ini
master = true
nohttpinterface = true
fork = true
port = 27017
quiet = true
logpath = /var/log/mongodb/mongod.log
logappend = true
journal = true
```

Запускаємо монго-демона

```bash
$ service mongod start
```

Тепер можна  підключитися в mongo-shell і перевірити, чи все працює

```bash
$ mongo
> show dbs
> exit
```

Якщо ви отримуєте помилку

```
/usr/local/etc/rc.d/mongod: WARNING: failed to start mongod
```

виконайте команду

```bash
$ rm /var/db/mongodb/mongod.lock
$ service mongod restart
```

> **УВАГА!** Це тимчасове рішення, яке може призвести до втрати даних. В документації монго цього робити не рекомендується.

### Ресурси

* [Топік на форумі FreeBSD зі встановлення Mongo](http://freebsd.pro/topic/28/)
* [Конфігурація Mongo](http://docs.mongodb.org/manual/administration/configuration/)
