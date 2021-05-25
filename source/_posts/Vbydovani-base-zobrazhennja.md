---
title: Вбудовані base64 зображення
date: 2016-07-08 16:44:14
tags: [python, js, html, web]
author: Misha Behersky
---

<p><a href="http://caniuse.com/#feat=datauri" target="_blank">HTML дозволяє</a> задавати зображення прямо в тегові за допомогою dataURI (зображення у вигляді base64-кодованого тексту). Виглядає це так</p>

<pre>
<code class="language-html">&lt;img alt="Embedded Image" src="data:image/png;base64,iVBORw0KGgoA..."&gt;</code></pre>

<p>Якщо потрібно відрендерити шаблон, який буде використовувати такі зображення на бекенді, можна використати <a href="https://docs.python.org/3/library/base64.html" target="_blank">base64</a> зі стандартної бібліотеки. Приклад для <a href="http://flask.pocoo.org/" target="_blank">Flask-у</a> (можна використати аналогічний підхід будь-де).</p>

<pre>
<code class="language-python">import base64

from flask import Flask, render_template


app = Flask(__name__, template_folder='.')


@app.route('/')
def hello():
    with open('image.png', 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return render_template('template.html', image=encoded_image)


if __name__ == '__main__':
    app.run()</code></pre>

<p>І сам файл шаблону <em>template.html</em></p>

<pre>
<code class="language-html">&lt;!DOCTYPE html&gt;
&lt;html&gt;

&lt;head&gt;
  &lt;meta http-equiv="Content-Type" content="text/html; charset=utf-8"/&gt;
  &lt;title&gt;Test embedded&lt;/title&gt;
&lt;/head&gt;

&lt;body&gt;
  &lt;p&gt;Image below&lt;/p&gt;
  &lt;img src="data:image/png;base64,{{image}}"&gt;
&lt;/body&gt;  
&lt;/html&gt;</code></pre>

<p>В результаті отримаємо сторінку з тегом зображення, яке вже вбудоване і не потребує виконання ще одного запиту до серверу.</p>

<p><img alt="" src="/img/article/28f73ca4dbf238649ee84949766e1d65.png" style="height:458px; width:428px" /></p>

<p>Ресурси</p>

<p><a href="https://varvy.com/pagespeed/base64-images.html" target="_blank">Переваги використання вбудованих зображень</a></p>

<p><a href="https://tools.ietf.org/html/rfc2397" target="_blank">RFC на стандарт</a></p>