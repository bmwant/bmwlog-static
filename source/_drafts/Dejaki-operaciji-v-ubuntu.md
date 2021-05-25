---
title: Деякі операції в Ubuntu
date: 2015-02-21 17:57:54
tags: [ubuntu, postgresql]
author: Misha Behersky
---

<h3>
 Виділити swap-пам'ять
</h3>
<p>
 На віртуальних машинах часто буває недостатньо оперативної пам'яті, а своп стандартно не виділяється. Щоб створити його самостійно (на 1 ГБ в прикладі) виконуємо команди від рута
</p>
<pre>
<code class="language-bash">dd if=/dev/zero of=/swapfile bs=1M count=1024
mkswap /swapfile
swapon  /swapfile</code></pre>
<p>
 В файлі
</p>
<pre>
<code class="language-bash">nano /etc/fstab</code></pre>
<p>
 додаємо рядок
 <strong>
  /swapfile none swap defaults 0 0
 </strong>
 і перезавантажуємо.
</p>
<h3>
 Виконати довготривалий процес у фоні
</h3>
<p>
 Часто потрібно підключитися по ssh, запустити якусь програму і закрити клієнт, щоб вона продовжувала працювати. Наприклад, тимчасово запустити сервер, щоб можна було протестувати якийсь функціонал. Для цього є команда
 <strong>
  nohup
 </strong>
</p>
<pre>
<code class="language-bash">nohup python server.py &amp;</code></pre>
<p>
 Після цього можна закривати термінал, а процес продовжить працювати. В кінці обов'язковий знак амперсанда.
</p>
<pre>
<code class="language-bash">nohup longproccess &amp;
exit</code></pre>
<h3>
 Перезавантажити машину
</h3>
<pre>
<code class="language-bash">reboot</code></pre>
<h3>
 Операції в PostgreSQL
</h3>
<p>
 Перейти в режим користувача-postgres для роботи з базами даних
</p>
<pre>
<code class="language-bash">su postgres</code></pre>
<p>
 Видалити базу даних. Переконайтеся, що до неї немає активних підключень
</p>
<pre>
<code class="language-bash">dropdb database_name</code></pre>
<p>
 Створити нового користувача і встановити для нього пароль
</p>
<pre>
<code class="language-bash">createuser -P username</code></pre>
<p>
 Створити нову базу даних і надати користувачу доступ до неї
</p>
<pre>
<code class="language-bash">createdb database_name --owner owner_name</code></pre>
<p>
</p>