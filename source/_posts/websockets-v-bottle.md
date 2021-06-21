---
title: websockets в Bottle
date: 2015-03-24 13:53:59
tags: [websocket, bottle, gunicorn, nginx]
author: Misha Behersky
language: ua
---

### Як подружити мікрофреймворк Bottle з веб-сокетами?

Будемо розглядати зв'язку **nginx+gunicorn+bottle**.

Підтримка [перемикання протоколу](http://tools.ietf.org/html/rfc2616#section-14.42), який необхідний для встановлення веб-сокет з'єднання, реалізована в nginx, починаючи з версії `1.3.13`. Тому перевірте свою версію nginx і за необхідності оновіть його

```bash
$ nginx -v
nginx version: nginx/1.6.2
```

Далі дещо змінюємо nginx-конфігурацію для вашого додатку

```nginx
location /websocket {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

Тепер встановлюємо gevent-websocket - воркер, що буде використовуватися gunicorn-ом для забезпечення підтримки веб-сокетів в bottle

```bash
$ pip install gevent-websocket
```

В файлі налаштувань gunicorn додаємо рядок (повний файл налаштувань [в цій статті](https://bmwlog.pp.ua/deploji-bottle-veb-dodatka/))


```python
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
```

Додаємо функцію-обробник в bottle-коді

```python
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            wsock.send('Your message %s' % message)
        except WebSocketError:
            break
```

І вбудовуємо в сторінку код, який буде спілкуватися з даним обробником

```javascript
var ws = new WebSocket("ws://localhost:8080/websocket");
ws.onopen = function() {
    ws.send("Hello, world");
};
ws.onmessage = function (evt) {
    alert(evt.data);
};
```

Перезапускаємо все

```bash
$ supervisorctl projectname restart
$ supervisorctl projectname status
$ nginx -t
$ nginx -s reload
```

Заходимо на сторінку і бачимо інформаційне віконце з вашим текстом!

### Ресурси

* [Асинхронний bottle](http://bottlepy.org/docs/dev/async.html#finally-websockets)
* [Gevent-websocket на PyPi](https://pypi.python.org/pypi/gevent-websocket/)
* [Стаття в блозі nginx про веб-сокети](http://nginx.com/blog/websocket-nginx/)
