---
title: websockets в Bottle
date: 2015-03-24 13:53:59
tags: [websocket, bottle, gunicorn, nginx]
author: Misha Behersky
---

<h3>Як подружити мікрофреймворк Bottle з веб-сокетами?</h3>

<p>Будемо розглядати зв&#39;язку <strong>nginx+gunicorn+bottle</strong>.</p>

<p>Підтримка <a href="http://tools.ietf.org/html/rfc2616#section-14.42" target="_blank">перемикання протоколу</a>, який необхідний для встановлення веб-сокет з&#39;єднання, реалізований в nginx, починаючи з версії <em>1.3.13</em>. Тому перевірте свою версію nginx і за необхідності оновіть його</p>

<pre>
<code class="language-bash">nginx -v
nginx version: nginx/1.6.2</code></pre>

<p>Далі дещо змінюємо nginx-конфігурацію для вашого додатку (про повне налаштування можна <a href="http://bmwlog.pp.ua/post/38" target="_blank">прочитати тут</a>).</p>

<pre>
<code class="language-nginx">location /websocket {                        
    proxy_pass http://backend;                
    proxy_http_version 1.1;                  
    proxy_set_header Upgrade $http_upgrade;  
    proxy_set_header Connection "upgrade";   
}                                            </code></pre>

<p>Тепер встановлюємо&nbsp;gevent-websocket, воркер, що буде використовуватися gunicorn-ом для забезпечення підтримки веб-сокетів в bottle</p>

<pre>
<code class="language-bash">pip install gevent-websocket</code></pre>

<p>В файлі налаштувань gunicorn додаємо рядок (повний файл налаштувань знову ж таки <a href="http://bmwlog.pp.ua/post/38" target="_blank">в цій статті</a>)</p>

<pre>
<code class="language-python">worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'</code></pre>

<p>Додаємо функцію-обробник в bottle-коді</p>

<pre>
<code>@app.route('/websocket')
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
</code></pre>

<p>І вбудовуємо в сторінку код, який буде спілкуватися з даним обробником</p>

<pre>
<code class="language-javascript">                                                  </code></pre>

<p>Перезапускаємо все</p>

<pre>
<code class="language-bash">supervisorctl projectname restart
supervisorctl projectname status
nginx -t
nginx -s reload</code></pre>

<p>Заходимо на сторінку і бачимо інформаційне віконце з вашим текстом!</p>

<p><img alt="" src="/img/article/e627bdfa9a173c729614a1004f3f6bd7.png" style="height:138px; width:450px" /></p>

<h3>Ресурси</h3>

<p><a href="http://bottlepy.org/docs/dev/async.html#finally-websockets" target="_blank">Асинхронний bottle</a></p>

<p><a href="https://pypi.python.org/pypi/gevent-websocket/" target="_blank">Gevent-websocket на PyPi</a></p>

<p><a href="http://nginx.com/blog/websocket-nginx/" target="_blank">Стаття в блозі nginx про веб-сокети</a></p>