---
title: Асинхронний Python #2
date: 2015-05-13 14:02:48
tags: [python, asyncio, aiohttp, requests]
author: Misha Behersky
---

<p>В цій статті перейдемо до практики асинхронного програмування, а також порівняння синхронного та асинхронного коду. Розробляти будемо програму, яка здійснює сотню запитів до різних веб-адрес. Для синхронного коду використаємо класну бібліотеку для запитів - <a href="http://docs.python-requests.org/en/latest/" target="_blank">Requests</a>.</p>

<pre>
<code class="language-python">def jumbotron():
    url = 'http://www.kinopoisk.ru/picture/'
    start_id = 1980223
    for i in range(100):
        next_id = start_id + i
        r = requests.get('{url}{id}'.format(url=url, id=next_id))
        assert r.status_code == 200</code></pre>

<p>Скрипт почергово проходить по 100 url-ам і завантажує відповідну сторінку. Асинхронний код виглядає не набагато складніше, але дозволяє значно прискорити цей процес. Для запитів використовуємо бібліотеку <a href="http://aiohttp.readthedocs.org/en/latest/client.html" target="_blank">aiohttp</a>.</p>

<pre>
<code class="language-python">@asyncio.coroutine
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
    res = yield from asyncio.gather(*coroutines)</code></pre>

<p>Тепер заміряємо час виконання для обох варіантів:</p>

<pre>
<code class="language-python">start = time.time()
jumbotron()
end = time.time()
print('Executed in %s seconds' % (end-start))</code></pre>

<p>для синхронного і</p>

<pre>
<code class="language-python">start = time.time()
asyncio.get_event_loop().run_until_complete(jumbotron())
end = time.time()
print('Executed in %s seconds' % (end-start))</code></pre>

<p>відповідно для асинхронного. На моєму комп&#39;ютері результати були <strong>15 секунд</strong> проти <strong>0.3 секунди</strong>. Тобто швидкість зросла в мільярд*&nbsp;разів. Також цей код можна переписати в якості грабера (можна завантажувати і зберігати картинки/музику/файли).</p>

<p><small>* - мільярд: абстрактне число, що використовується для підкреслення значущості деякої величини та її безперечної переваги над інишими</small></p>

<h3>Ресурси</h3>

<p><a href="http://sahandsaba.com/understanding-asyncio-node-js-python-3-4.html" target="_blank">Непогана стаття з гарними прикладами для asyncio</a></p>

<p><a href="http://geekgirl.io/concurrent-http-requests-with-python3-and-asyncio/" target="_blank">Ще одна стаття, також англійською</a></p>