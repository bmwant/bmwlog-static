---
title: MySQL. Основні команди
date: 2015-02-10 21:41:24
tags: [mysql, db, cheatsheet]
author: Misha Behersky
language: ua
---

### Створюємо базу даних та користувача для неї

Виконуємо вхід та створюємо базу даних

```bash
$ mysql -u root -p[your-root-password]
mysql> CREATE DATABASE [databasename];
```

Створюємо користувача і надаємо йому повний доступ до бази

```sql
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON databasename.* TO newuser@localhost;
```

Оновлюємо права доступу і виходимо

```sql
mysql> FLUSH PRIVILEGES;
mysql> quit;
```

Тепер можемо ввійти під нашим новим користувачем

```bash
$ mysql -u newuser -p
```

Вводимо пароль і працюємо з нашою базою даних.

### Перезапустити MySQL-сервер на FreeBSD

```bash
$ service mysql-server restart
```

### Дозволити доступ до бази даних з віддалених хостів

```sql
mysql> USE mysql;
mysql> SELECT host, user FROM user;
mysql> UPDATE user SET host='%' WHERE user='[username]' AND host='localhost';
mysql> FLUSH PRIVILEGES;
```

Замість хоста можна вказати хост або символи підстановки (`%` для всіх). Також можна дозволити доступ одразу при створенні користувача: `CREATE USER 'newuser'@&'%';`

### Вивести список всіх баз даних

```sql
mysql> SHOW databases;
```
