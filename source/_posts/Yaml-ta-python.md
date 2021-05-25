---
title: YAML та Python
date: 2015-04-12 19:58:00
tags: [yaml, python, serialization]
author: Misha Behersky
---

<p>YAML (<em>YAML Ain&#39;t Markup Language</em>) - це стандарт серіалізації даних для багатьох мов програмування. Також його можна використовувати і для зберігання файлів-конфігурацій. Працювати з ним в Python достатньо просто. Якщо ви використовували <a href="https://docs.python.org/2/library/pickle.html" target="_blank">pickle</a>&nbsp;або <a href="https://docs.python.org/2/library/json.html" target="_blank">json</a>&nbsp;модулі, то тут все досить схоже. Підтримка реалізована модулем PyYAML.</p>

<p>Для швидкого встановлення&nbsp;використовуємо pip</p>

<pre>
<code class="language-python">pip install pyyaml</code></pre>

<p>Створюємо файл конфігурації на основі словника</p>

<pre>
<code class="language-python">import yaml

config = {
    'param1': 500,
    'param2': 'value2'
}

with open('config.txt', 'w') as fout:
    fout.write(yaml.dump(config))</code></pre>

<p>Використовуємо цей файл в подальшому або іншою програмою</p>

<pre>
<code class="language-python">with open('config.txt') as fin:
    cfg = yaml.load(fin.read())
    print(cfg['param1'])</code></pre>

<p>Перехоплюємо помилки, якщо файл некоректний</p>

<pre>
<code class="language-python">import yaml

try:
    config = yaml.load(file('config.txt'))
except yaml.YAMLError as exc:
    print('Error in configuration file: %s' % exc)</code></pre>

<h3>Ресурси</h3>

<p><a href="http://yaml.org" target="_blank">Офіційний сайт YAML</a></p>

<p><a href="http://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank">Документація PyYAML</a></p>