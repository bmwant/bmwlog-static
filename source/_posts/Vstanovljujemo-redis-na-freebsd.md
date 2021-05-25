---
title: Встановлюємо Redis на FreeBSD
date: 2015-02-01 14:27:06
tags: [redis, freebsd]
author: Misha Behersky
---

<h3>Встановлюємо Redis з портів</h3>

<pre>
<code class="language-bash">cd /usr/ports/databases/redis/ 
make install clean</code></pre>

<h3>Додаємо в автозавантаження</h3>

<p>В файлі /etc/rc.conf додаємо рядок</p>

<pre>
<code class="language-bash">redis_enable="YES"</code></pre>

<p>Щоб запустити Redis, виконуємо команду</p>

<pre>
<code class="language-bash">service redis start</code></pre>

<p>Клієнт для робити з Redis також встановлений. Для його запуску вводимо <strong>redis-cli</strong></p>

<p>Конфігурація зберігається в файлі<strong>&nbsp;/usr/local/etc/redis.conf</strong></p>

<h3>Ресурси</h3>

<p><a href="http://redis.io/commands" target="_blank">Документація по командах на redis.io</a></p>