---
title: Деплой Flask веб-додатка
date: 2015-02-13 16:40:18
tags: [flask, nginx, uwsgi, deploy]
author: Misha Behersky
---

<h3>
 Розгортаємо на Freebsd+nginx+uwsgi+Flask
</h3>
<p>
 У virtual environment виконуємо команду
</p>
<pre>
<code class="language-bash">pip install uwsgi</code></pre>
<p>
 Створюємо файл конфігурації для
 <strong>
  uwsgi
 </strong>
 ,
 <em>
  uwsgi_projectname.ini
 </em>
</p>
<pre>
<code class="language-ini">[uwsgi]
chdir=/path/to/project
wsgi-file=run.py
callable=app
env=/path/to/project/venv
socket=127.0.0.1:6783
processes=4
threads=2
master=True
chmod-socket=666
</code></pre>
<p>
 Конфігурація для
 <strong>
  nginx
 </strong>
 , сервер має співпадати з параметром сокет вище
</p>
<pre>
<code class="language-nginx">upstream projectname {
    server 127.0.0.1:6783;
}

server {
    listen 80;
    server_name _;
    charset utf-8;

    root /path/to/project;
    
    location / {
      try_files $uri @proxy_to_app;
    }
    
    location @proxy_to_app {
      uwsgi_pass projectname;
      include /usr/local/etc/nginx/uwsgi_params;
    }
}
</code></pre>
<pre>
<code class="language-bash">ln -s /path/to/your/project/nginx_projectname.conf /etc/nginx/sites-enabled/
nginx -t
nginx -s reload</code></pre>
<p>
 Запускаємо
</p>
<pre>
<code class="language-bash">uwsgi --ini uwsgi_projectname.ini</code></pre>
<h3>
 +Supervisor
</h3>
<p>
 Конфіг файл,
 <em>
  supervisor_projectname.conf
 </em>
</p>
<pre>
<code class="language-ini">[program:projectname]
command=/path/to/project/venv/bin/uwsgi --ini uwsgi_projectname.ini
directory=/path/to/project
user=username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/projectname.supervisor.stdout
stopsignal=QUIT </code></pre>
<p>
 Щоб файл зберігався в поточній папці, робимо на нього посилання
</p>
<pre>
<code class="language-bash">ln -s /path/to/project/supervisor_projectname.conf /usr/local/etc/supervisor/
supervisorctl
reread
update</code></pre>
<h3>
 Ресурси
</h3>
<p>
 <a href="http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html#deploying-flask" target="_blank">
  uWSGI документація для Flask
 </a>
</p>
<p>
 <a href="http://flask.pocoo.org/docs/0.10/deploying/uwsgi/" target="_blank">
  Flask документація для uWSGI)
 </a>
</p>