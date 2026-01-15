---
title: Знайомство з Pyramid
date: 2015-05-29 13:04:44
tags: [python, pyramid, web, framework]
author: Misha Behersky
language: ua
archived: true
---

[Pyramid](http://www.pylonsproject.org/) - один з популярних [WSGI](http://wsgi.readthedocs.org/en/latest/) веб-фреймворків для Пайтона, який містить багато вбудованих компонентів для швидкої розробки вашого проекту. Сумісний з Python 3.

### Hello world

Створюємо мінімальний для запуску проект. В активованому віртуальному середовищі вводимо

```bash
$ pip install pyramid
```

Далі створюємо файл `hello.py` з таким вмістом

```python
from wsgiref.simple_server import make_server
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
```

Зберігаємо і в консолі вводимо команду

```bash
$ python hello.py
```

Тепер переходимо в браузері за адресою [localhost:8080/hello/misha](http://localhost:8080/hello/misha) і отримуємо повідомлення `Hello misha` (або інше ім'я, яке ви введете).

### Генерація проекту

Pyramid дозволяє генерувати базову структуру проекту, щоб прискорити процес розробки додатку (аналогічно команді `startproject` в Django).

```bash
$ pcreate -s starter project_name
$ python setup.py develop
```

Все готово для розробки вашого проекту. Крім параметру `starter` можна вказати `zodb` або `alchemy`, якщо ви хочете мати можливість працювати з базою даних.

За допомогою тестів, перевіряємо, чи все працює належним чином

```bash
$ python setup.py test -q
```

і запускаємо сервер

```bash
$ pserve development.ini
```

Тепер можна перейти на [localhost:6543](http://localhost:6543) і побачити результат (без написання жодного рядка коду). Все, можна приступати до розробки. Для того, щоб сервер автоматично перезапускався після змін у вашому коді додаємо ключ `--reload`.

```bash
$ pserve development.ini --reload
```

Детальніше про роботу з автоматичним генератором можна [подивитися тут](http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/project.html).

### Ресурси

* [Official tutorial for Pyramid](http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/index.html#quick-tutorial)
