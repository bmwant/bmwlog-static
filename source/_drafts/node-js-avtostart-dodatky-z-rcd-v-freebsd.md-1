---
title: node js автостарт додатку з rc.d в FreeBSD
date: 2018-06-07 09:55:16
tags: [freebsd, nodejs, foreverjs, rcd]
author: Misha Behersky
---

<p>Нещодавно виникла необхідність запустити веб-додаток на <a href="http://expressjs.com" target="_blank">Express</a> (node js) автоматично при старті та перезапуску системи (FreeBSD 10.3). До цього все запускалося за допомогою чудового менеджера процесів для ноди - <a href="https://github.com/foreverjs/forever" target="_blank">foreverjs</a>. Він чудово працює з дочірніми процесами і виконує свої функції (старт, перезапуск, перегляд логів, рестарт при зміні коду), але не запускається автоматично з операційною системою. Рішенням став демон системи, що виконує скрипти автозапуску під час старту - <a href="https://www.freebsd.org/doc/en_US.ISO8859-1/articles/rc-scripting/" target="_blank">rc.d</a>.</p>

<p>Проста конфігурація додатку для forever</p>

<pre>
<code class="language-json">{
    "uid": "myapp",
    "append": true,
    "watch": true,
    "script": "app.js",
    "sourceDir": "/home/user/myapp"
}</code></pre>

<p>І rc-скрипт який буде відповідати за запуск</p>

<pre>
<code class="language-bash">#!/bin/sh

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

run_rc_command "$1"</code></pre>

<p>Два важливих момента: </p>

<ol>
	<li>За допомогою цього скрипта можна виконувати запуск від будь-якого користувача, не лише root-а. Для цього в функціях start/stop/restart перед командою додатково є префікс <span class="inline-code">su - user -c</span>.</li>
	<li>Щоб передати змінні оточення - задаємо їх перед командою. Наприклад, перевизначаю порт для запуску <span class="inline-code">PORT=3344</span></li>
</ol>

<p>Все інше залишаємо без змін, замінюючи назву додатку та шлях до робочої директорії. Копіюємо цей файл в <span class="inline-code">/usr/local/etc/rc.d</span> і не забуваємо додавати права на виконання файлу.</p>

<pre>
<code class="language-bash">sudo chmod +x /usr/local/etc/rc.d/myapp</code></pre>

<p>Тепер можна користуватися всіма плюшками сервісу </p>

<pre>
<code class="language-bash">sudo service myapp restart</code></pre>

<h3>Ресурси</h3>

<p><a href="https://bieker.ninja/2014/04/23/nodejs-startup-script-for-freebsd.html" target="_blank">NodeJs Startup Script for FreeBSD</a></p>

<p><a href="https://habrahabr.ru/post/137857/" target="_blank">Схожа стаття на Хабрі</a></p>