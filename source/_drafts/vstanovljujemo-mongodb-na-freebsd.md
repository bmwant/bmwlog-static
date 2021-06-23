---
title: Встановлюємо MongoDB на FreeBSD
date: 2015-02-01 14:19:03
tags: [mongodb, freebsd]
author: Misha Behersky
---

<p>
 Встановлюємо
 <strong>
  Mongo
 </strong>
 з портів
</p>
<pre>
<code class="language-bash">cd /usr/ports/databases/mongodb/
make install clean</code></pre>
<p>
 Додаємо параметри автозапуску в
 <em>
  /etc/rc.conf
 </em>
</p>
<pre>
<code class="language-ini">mongod_enable="YES"
mongod_config="/usr/local/etc/mongodb.conf"
mongod_dbpath="/var/db/mongodb"</code></pre>
<p>
 Налаштовуємо файл конфігурації
 <em>
  /usr/local/etc/mongodb.conf
 </em>
</p>
<pre>
<code class="language-ini">master = true
nohttpinterface = true
fork = true
port = 27017
quiet = true
logpath = /var/log/mongodb/mongod.log
logappend = true
journal = true</code></pre>
<p>
 Запускаємо монго-демона
</p>
<pre>
<code class="language-bash">service mongod start</code></pre>
<p>
 Тепер можна  підключитися в mongo-shell і перевірити, чи все працює
</p>
<pre>
<code class="language-bash">mongo
show dbs
exit</code></pre>
<p>
 Якщо ви отримуєте помилку
</p>
<p>
 <strong>
  /usr/local/etc/rc.d/mongod: WARNING: failed to start mongod
 </strong>
</p>
<p>
 виконайте команду
</p>
<pre>
<code class="language-bash">rm /var/db/mongodb/mongod.lock
service mongod restart</code></pre>
<p>
 <strong>
  УВАГА!
 </strong>
 Це тимчасове рішення, яке може призвести до втрати даних. В документації монго цього робити не рекомендується.
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="http://freebsd.pro/topic/28/" target="_blank">
  Топік на форумі FreeBSD зі встановлення Mongo
 </a>
</p>
<p>
 <a href="http://docs.mongodb.org/manual/administration/configuration/" target="_blank">
  Конфігурація Mongo
 </a>
</p>