---
title: Деплой bottle веб-додатка
date: 2015-02-13 15:50:30
tags: [bottle, gunicorn, nginx, supervisor, freebsd]
author: Misha Behersky
---

<h3>Розгортаємо FreeBSD+nginx+Gunicorn+bottle+Supervisor</h3>

<p>Створюємо віртуальне оточення, активуємо його, встановлюємо всі залежності і виконуємо команду</p>

<pre>
<code class="language-bash">pip install gunicorn</code></pre>

<p><img alt="" src="/img/article/c2156d1bed9c3d569daf9304c82fe185.png" style="height:73px; width:227px" /></p>

<p>Далі створюємо файл конфігурації для <strong> nginx, </strong> <em> nginx_projectname.conf </em></p>

<pre>
<code class="language-nginx">upstream projectname {
    server 127.0.0.1:8031;
}

server {
    listen 80;
    server_name example.com *.example.com;
    charset utf-8;

    root /data/projects/projectname;
    
    location / {
      try_files $uri @proxy_to_app;
    }
    
    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass http://projectname;
    }
}</code></pre>

<p>Застосовуємо внесені зміни</p>

<pre>
<code class="language-bash">ln -s /path/to/your/project/nginx_projectname.conf /etc/nginx/sites-enabled/
nginx -s reload</code></pre>

<p>Створюємо файл з конфігурацією для <strong> Gunicorn, </strong> <em> g_settings.py </em></p>

<pre>
<code class="language-bash">bind = "127.0.0.1:8031"
workers = 4</code></pre>

<p>В <strong> bind </strong> прописуємо те ж, що і в налаштуваннях <strong> nginx </strong></p>

<p>Запускаємо за допомогою <strong> Gunicorn </strong> . Переконайтеся, що файл <em> run.py </em> містить таку конструкцію:</p>

<pre>
<code class="language-python">from bottle import run, default_app
from app import app, config as conf

if __name__ == '__main__':
    run(app=app, host=conf.RUN_HOST, port=conf.RUN_PORT)
else:
    app = default_app()</code></pre>

<pre>
<code class="language-bash">gunicorn --cofing g_config.py run:app</code></pre>

<h3>Автоматизуємо запуск</h3>

<p>Ну, Supervisor. Створюємо <em> supervisor_projectname.conf </em> файл в директорії <strong> /usr/local/etc/supervisor/ </strong> (або створюємо туди посилання):</p>

<pre>
<code class="language-ini">[program:projectname]
command=/path/to/project/venv/bin/gunicorn run:app --config g_settings.py
directory=/path/to/project/
user=nobody
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/projectname.supervisor.stdout
stopsignal=QUIT </code></pre>

<p>Все готово, перевіряємо.</p>

<pre>
<code class="language-bash">supervisorctl
reread
update
status</code></pre>

<p>projectname RUNNING pid654, uptime 6 days)</p>

<h3>Ресурси</h3>

<p><a href="http://bottlepy.org/docs/dev/deployment.html" target="_blank">Документація по деплою bottle </a></p>

<p><a href="http://gunicorn.org" target="_blank">Сайт Gunicorn </a></p>