---
title: MySQL. Основні команди
date: 2015-02-10 21:41:24
tags: [mysql, db, cheatsheet]
author: Misha Behersky
language: ua
---

### Створюємо базу даних та користувача для неї

<p>Виконуємо вхід та створюємо базу даних</p>

<pre>
<code class="language-sql">mysql -u root -p[your-root-password]
CREATE DATABASE [databasename];</code></pre>

<p>Створюємо користувача і надаємо йому повний доступ до бази</p>

<pre>
<code class="language-sql">CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON databasename.* TO newuser@localhost;</code></pre>

<p>Оновлюємо права доступу і виходимо</p>

<pre>
<code class="language-sql">FLUSH PRIVILEGES;

quit;</code></pre>

<p>Тепер можемо ввійти під нашим новим користувачем</p>

<pre>
<code class="language-bash">mysql -u newuser -p</code></pre>

<p>Вводимо пароль і працюємо з нашою базою даних.</p>

### Перезапустити MySQL-сервер на FreeBSD

<pre>
<code class="language-bash">service mysql-server restart</code></pre>

### Дозволити доступ до бази даних з віддалених хостів

<pre>
<code class="language-sql">USE mysql;
SELECT host, user FROM user;
UPDATE user SET host='%' WHERE user='[username]' AND host='localhost';
FLUSH PRIVILEGES;
</code></pre>

<p>Замість хоста можна вказати хост або символи підстановки (<strong>% </strong>для всіх). Також можна дозволити доступ одразу при створенні користувача:&nbsp;<strong>CREATE USER &#39;newuser&#39;@&#39;%&#39;</strong></p>

### Вивести список всіх баз даних

<pre>
<code class="language-sql">SHOW databases;</code></pre>
