---
title: Встановлюємо PostgreSQL на FreeBSD
date: 2015-02-21 17:57:54
tags: [postgresql, pgadmin, freebsd]
author: Misha Behersky
---

<p>
 Стандартно встановлюємо з портів
</p>
<pre>
<code class="language-bash">cd /usr/ports/databases/postgresql94-server
make config
make install clean</code></pre>
<p>
 Додаємо в автозапуск при завантаженні
</p>
<pre>
<code class="language-bash">echo 'postgresql_enable="YES"' &gt;&gt; /etc/rc.conf</code></pre>
<p>
 Перша ініціалізація
</p>
<pre>
<code class="language-bash">/usr/local/etc/rc.d/postgresql initdb</code></pre>
<p>
 В файлі
 <strong>
  /usr/local/pgsql/data/postgresql.conf
 </strong>
 розкоментовуємо/змінюємо рядки. Вказуємо слухати з'єднання зі всіх адрес на порту
 <em>
  5432
 </em>
</p>
<pre>
<code class="language-ini">listen_addresses = '*'
port = 5432</code></pre>
<p>
 Додаємо такі рядки у файл
 <strong>
  /usr/local/pgsql/data/pg_hba.conf
 </strong>
</p>
<pre>
<code class="language-ini">host    all    all    0.0.0.0/0    md5
host    all    all         ::/0    md5</code></pre>
<p>
 Для всіх зовнішніх підключень вимагати аутентифікацію
</p>
<h3>
 Створюємо нового користувача з усіма привілеями
</h3>
<pre>
<code class="language-bash">su pgsql
createuser -sdrP username</code></pre>
<p>
 <strong>
  -s
 </strong>
 - користувач буде суперюзером
</p>
<p>
 <strong>
  -d
 </strong>
 - користувач зможе створювати бази даних
</p>
<p>
 <strong>
  -r
 </strong>
 - користувач зможе створювати нові ролі
</p>
<p>
 <strong>
  -P
 </strong>
 - запитати пароль для нового користувача
</p>
<h3>
 Створюємо нову базу даних
</h3>
<pre>
<code class="language-bash">createdb test</code></pre>
<p>
 Підключаємося до неї за допомогою клієнта
 <strong>
  psql
 </strong>
</p>
<pre>
<code class="language-bash">psql test</code></pre>
<p>
 В запрошенні вводу команди можна ввести:
</p>
<p>
 <strong>
  \dt
 </strong>
 - показати всі таблиці в базі
</p>
<p>
 <strong>
  \dt tablename
 </strong>
 - описати конкретну таблицю
</p>
<p>
 <strong>
  \l
 </strong>
 - (L в нижньому регістрі), список всіх баз даних
</p>
<p>
 <strong>
  \q
 </strong>
 - вихід
</p>
<p>
 Щоб використовувати PostgreSQL віддалено можна скористатися клієнтом
 <a href="http://www.pgadmin.org" target="_blank">
  pgAdmin
 </a>
 .
</p>
<p>
 Після внесення змін в файли конфігурації пишемо
</p>
<pre>
<code class="language-bash">service postgresql restart</code></pre>
<h3>
 Ресурси
</h3>
<p>
 <a href="http://www.pgadmin.org/download/windows.php" target="_blank">
  Завантажити pgAdmin для Windows
 </a>
</p>