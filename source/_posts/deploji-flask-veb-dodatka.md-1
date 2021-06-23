---
title: Деплой Flask веб-додатка
date: 2015-02-13 16:40:18
tags: [flask, nginx, uwsgi, deploy]
author: Misha Behersky
language: ua
---

### Розгортаємо на Freebsd+nginx+uwsgi+Flask

У virtual environment виконуємо команду

```bash
$ pip install uwsgi
```

Створюємо файл конфігурації для _uwsgi_, `uwsgi_projectname.ini`

```ini
[uwsgi]
chdir=/path/to/project
wsgi-file=run.py
callable=app
env=/path/to/project/venv
socket=127.0.0.1:6783
processes=4
threads=2
master=True
chmod-socket=666
```

Конфігурація для _nginx_, `nginx_projectname.conf` - сервер має співпадати з параметром сокет вище

```nginx
upstream projectname {
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
```

Активуємо конфігурацію

```bash
$ ln -s /path/to/your/project/nginx_projectname.conf /etc/nginx/sites-enabled/
$ nginx -t
$ nginx -s reload
```

Запускаємо сервер

```bash
$ uwsgi --ini uwsgi_projectname.ini
```

### +Supervisor

Конфіг файл, `supervisor_projectname.conf`

```ini
[program:projectname]
command=/path/to/project/venv/bin/uwsgi --ini uwsgi_projectname.ini
directory=/path/to/project
user=username
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/projectname.supervisor.stdout
stopsignal=QUIT
```

Щоб файл зберігався в поточній папці, робимо на нього посилання

```bash
$ ln -s /path/to/project/supervisor_projectname.conf /usr/local/etc/supervisor/
$ supervisorctl
> reread
> update
```

### Ресурси

* [uWSGI документація для Flask](http://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html#deploying-flask)
* [Flask документація для uWSGI](http://flask.pocoo.org/docs/0.10/deploying/uwsgi/)
