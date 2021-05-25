---
title: Знайомство з Pyramid
date: 2015-05-29 13:04:44
tags: [python, pyramid, web, framework]
author: Misha Behersky
---

<p><a href="http://www.pylonsproject.org/" target="_blank">Pyramid </a>- один з популярних <a href="http://wsgi.readthedocs.org/en/latest/" target="_blank">WSGI&nbsp;</a>веб-фреймворків для Пайтона, який містить багато вбудованих компонентів для швидкої розробки вашого проекту. Сумісний з Python 3.</p>

<h3>Hello world</h3>

<p>Створюємо мінімальний для запуску проект. В активованому віртуальному середовищі вводимо</p>

<pre>
<code class="language-bash">pip install pyramid</code></pre>

<p>Далі створюємо файл <em>hello.py</em> з таким вмістом</p>

<pre>
<code class="language-python">from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Hello %(name)s' % request.matchdict)

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()</code></pre>

<p>Зберігаємо і в консолі вводимо команду</p>

<pre>
<code class="language-bash">python hello.py</code></pre>

<p>Тепер переходимо в браузері за адресою <a href="http://localhost:8080/hello/misha" target="_blank">localhost:8080/hello/misha</a>&nbsp;і отримуємо повідомлення <strong>Hello misha </strong>(або інше ім&#39;я, яке ви введете).</p>

<h3>Генерація проекту</h3>

<p>Pyramid дозволяє генерувати базову структуру проекту, щоб прискорити процес розробки додатку (аналогічно команді <em>startproject</em> в Django).</p>

<pre>
<code class="language-bash">pcreate -s starter project_name
python setup.py develop</code></pre>

<p>Все готово для розробки вашого проекту. Крім параметру <em>starter</em> можна вказати <em>zodb </em>або <em>alchemy</em>, якщо ви хочете мати можливість працювати з базою даних.</p>

<p>За допомогою тестів, перевіряємо, чи все працює належним чином</p>

<pre>
<code class="language-bash">python setup.py test -q</code></pre>

<p>і запускаємо сервер</p>

<pre>
<code class="language-bash">pserve development.ini</code></pre>

<p>Тепер можна перейти на&nbsp;<a href="http://localhost:6543" target="_blank">localhost:6543</a>&nbsp;і побачити результат (без написання жодного рядка коду). Все,<span style="line-height:1.6">&nbsp;можна приступати до розробки. Для того, щоб сервер автоматично перезапускався після змін у вашому коді додаємо ключ </span><em style="line-height:1.6">--reload</em></p>

<pre>
<code class="language-bash">pserve development.ini --reload</code></pre>

<p>Детальніше про роботу з автоматичним генератором можна <a href="http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html" target="_blank">подивитися тут</a>.</p>

<h3>Ресурси</h3>

<p><a href="http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/index.html#quick-tutorial" target="_blank">Official tutorial for Pyramid</a></p>