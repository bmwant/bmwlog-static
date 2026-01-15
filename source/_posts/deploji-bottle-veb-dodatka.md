---
title: Деплой bottle веб-додатка
date: 2015-02-13 15:50:30
tags: [bottle, gunicorn, nginx, supervisor, freebsd]
author: Misha Behersky
language: ua
archived: true
---

### Розгортаємо FreeBSD+nginx+Gunicorn+bottle+Supervisor

Створюємо віртуальне оточення, активуємо його, встановлюємо всі залежності і виконуємо команду

```bash
$ pip install gunicorn
```

![rel](/old/article/c2156d1bed9c3d569daf9304c82fe185.png)

Далі створюємо файл конфігурації для **nginx**, `nginx_projectname.conf`

```nginx
upstream projectname {
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
}
```

Застосовуємо внесені зміни

```bash
$ ln -s /path/to/your/project/nginx_projectname.conf /etc/nginx/sites-enabled/
$ nginx -s reload
```

Створюємо файл з конфігурацією для **Gunicorn**, `g_settings.py`

```python
bind = "127.0.0.1:8031"
workers = 4
```

В **bind** прописуємо те ж, що і в налаштуваннях **nginx**

Запускаємо за допомогою **Gunicorn**. Переконайтеся, що файл `run.py` містить таку конструкцію:

```python
from bottle import run, default_app
from app import app, config as conf

if __name__ == '__main__':
    run(app=app, host=conf.RUN_HOST, port=conf.RUN_PORT)
else:
    app = default_app()
```

```bash
$ gunicorn --cofing g_config.py run:app
```

### Автоматизуємо запуск

Ну, Supervisor. Створюємо `supervisor_projectname.conf` файл в директорії `/usr/local/etc/supervisor/` (або створюємо туди посилання):

```ini
[program:projectname]
command=/path/to/project/venv/bin/gunicorn run:app --config g_settings.py
directory=/path/to/project/
user=nobody
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/projectname.supervisor.stdout
stopsignal=QUIT
```

Все готово, перевіряємо.

```bash
$ supervisorctl
> reread
> update
> status
projectname RUNNING pid654, uptime 6 days
```

### Ресурси

* [Документація по деплою bottle](http://bottlepy.org/docs/dev/deployment.html)
* [Сайт Gunicorn](http://gunicorn.org)
