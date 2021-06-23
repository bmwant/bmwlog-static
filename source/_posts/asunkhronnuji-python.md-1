---
title: Асинхронний Python
date: 2015-05-13 14:02:48
tags: [python, asyncio, aiohttp, requests]
author: Misha Behersky
---

В цій статті перейдемо до практики асинхронного програмування, а також порівняння синхронного та асинхронного коду. Розробляти будемо програму, яка здійснює сотню запитів до різних веб-адрес. Для синхронного коду використаємо класну бібліотеку для запитів - [Requests](http://docs.python-requests.org/en/latest/).

```python
def jumbotron():
    url = 'http://www.kinopoisk.ru/picture/'
    start_id = 1980223
    for i in range(100):
        next_id = start_id + i
        r = requests.get('{url}{id}'.format(url=url, id=next_id))
        assert r.status_code == 200
```

Скрипт почергово проходить по 100 url-ам і завантажує відповідну сторінку. Асинхронний код виглядає не набагато складніше, але дозволяє значно прискорити цей процес. Для запитів використовуємо бібліотеку [aiohttp](http://aiohttp.readthedocs.org/en/latest/client.html).

```python
@asyncio.coroutine
def get_url(url):
    r = yield from aiohttp.request('get', url)
    assert r.status == 200
    r.close()


@asyncio.coroutine
def jumbotron():
    url = 'http://www.kinopoisk.ru/picture/'
    start_id = 1980223
    coroutines = []
    for i in range(100):
        next_id = start_id + i
        url = '{url}{id}'.format(url=url, id=next_id)
        coroutines.append(get_url(url))
    res = yield from asyncio.gather(*coroutines)
```

Тепер заміряємо час виконання для обох варіантів:

```python
start = time.time()
jumbotron()
end = time.time()
print('Executed in %s seconds' % (end-start))
```

для синхронного і

```python
start = time.time()
asyncio.get_event_loop().run_until_complete(jumbotron())
end = time.time()
print('Executed in %s seconds' % (end-start))
```

відповідно для асинхронного. На моєму комп'ютері результати були **15 секунд** проти **0.3 секунди**. Тобто швидкість зросла в _мільярд*_ разів. Також цей код можна переписати в якості грабера (можна завантажувати і зберігати картинки/музику/файли).

_* - мільярд_: абстрактне число, що використовується для підкреслення значущості деякої величини та її безперечної переваги над інишими

### Ресурси

* [Непогана стаття з гарними прикладами для asyncio](http://sahandsaba.com/understanding-asyncio-node-js-python-3-4.html)
* [Ще одна стаття, також англійською](http://geekgirl.io/concurrent-http-requests-with-python3-and-asyncio/)
