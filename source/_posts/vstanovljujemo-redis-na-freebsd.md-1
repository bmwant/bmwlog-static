---
title: Встановлюємо Redis на FreeBSD
date: 2015-02-01 14:27:06
tags: [redis, freebsd]
author: Misha Behersky
language: ua
---

### Встановлюємо Redis з портів

```bash
$ cd /usr/ports/databases/redis/
$ make install clean
```

### Додаємо в автозавантаження

В файлі `/etc/rc.conf` додаємо рядок

```
redis_enable="YES"
```

Щоб запустити Redis, виконуємо команду

```bash
$ service redis start
```

Клієнт для робити з Redis також встановлений. Для його запуску вводимо `redis-cli`

Конфігурація зберігається в файлі `/usr/local/etc/redis.conf`

### Ресурси

* [Документація по командах на redis.io](http://redis.io/commands)
