---
title: Встановлюємо PostgreSQL на FreeBSD
date: 2015-02-21 17:57:54
tags: [postgresql, pgadmin, freebsd]
author: Misha Behersky
language: ua
archived: true
---

Стандартно встановлюємо з портів

```bash
$ cd /usr/ports/databases/postgresql94-server
$ make config
$ make install clean
```

Додаємо в автозапуск при завантаженні

```bash
$ echo 'postgresql_enable="YES"' >> /etc/rc.conf
```

Перша ініціалізація

```bash
$ /usr/local/etc/rc.d/postgresql initdb
```

В файлі `/usr/local/pgsql/data/postgresql.conf` розкоментовуємо/змінюємо рядки. Вказуємо слухати з'єднання зі всіх адрес на порту `5432`

```ini
listen_addresses = '*'
port = 5432
```

Додаємо такі рядки у файл `/usr/local/pgsql/data/pg_hba.conf`

```
host    all    all    0.0.0.0/0    md5
host    all    all         ::/0    md5
```

Для всіх зовнішніх підключень вимагати аутентифікацію

### Створюємо нового користувача з усіма привілеями

```bash
$ su pgsql
$ createuser -sdrP username
```

`-s` - користувач буде суперюзером
`-d` - користувач зможе створювати бази даних
`-r` - користувач зможе створювати нові ролі
`-P` - запитати пароль для нового користувача

### Створюємо нову базу даних

```bash
$ createdb test
```

Підключаємося до неї за допомогою клієнта `psql`

```bash
$ psql test
```

В запрошенні вводу команди можна ввести:
`\dt` - показати всі таблиці в базі
`\dt tablename` - описати конкретну таблицю
`\l` - (L в нижньому регістрі), список всіх баз даних
`\q` - вихід

Щоб використовувати PostgreSQL віддалено можна скористатися клієнтом [pgAdmin](http://www.pgadmin.org).

Після внесення змін в файли конфігурації пишемо

```bash
$ service postgresql restart
```

### Ресурси

* [Завантажити pgAdmin для Windows](http://www.pgadmin.org/download/windows.php)
