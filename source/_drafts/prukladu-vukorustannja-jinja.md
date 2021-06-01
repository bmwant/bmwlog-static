---
title: Приклади використання Jinja2
date: 2014-10-26 22:51:17
tags: [jinja2, python, filters]
author: Misha Behersky
language: ua
---

### Пишемо власний фільтр

<p>Шаблонізатор Jinja2 має багато вбудованих фільтрів, серед яких:</p>

<p><strong>capitalize(s).&nbsp;</strong>Переводить першу літеру рядка в верхній регістр, всі інші будуть в нижньому.</p>

<p><strong>dictsort(value,&nbsp;case_sensitive=False,&nbsp;by=&#39;key&#39;).&nbsp;</strong>Дозволяє сортувати словник за ключами або значеннями.</p>

<p><strong>filesizeformat(value,&nbsp;binary=False).&nbsp;</strong>Форматує вивід розміру файлу у зрозумілий вигляд (13 kB, 4.1 MB, 102 Bytes).</p>

<p><strong>first.</strong> Повертає перший елемент послідовності.</p>

<p><strong>round(value,&nbsp;precision=0,&nbsp;method=&#39;common&#39;).&nbsp;</strong>Округляє значення з заданою точністю звичайний способом округлення (<em>common</em>), завжди до більшого значення (<em>ceil</em>) або до меншого (<em>floor</em>).</p>

<p>Повний список можна знайти в офіційній документації <a href="http://jinja.pocoo.org/docs/dev/templates/#list-of-builtin-filters" target="_blank">тут</a>.</p>

<p>Фільтр - це звичайна функція, яка приймає ліву сторону як перший аргумент і всі інші параметри як додаткові аргументи. Наприклад, нам потрібно, щоб фільтр додавав до значення знак&nbsp;<em>$</em>, якщо це число, в іншому випадку дописував слово <em>dollars</em>. Так буде виглядати наш фільтр:</p>

<pre>
<code class="language-python">def dollars(value):
    try:
        new_value = str(int(value)) + '$'
    except ValueError:
        new_value = value + ' dollars'
    return new_value</code></pre>

<p>Тепер потрібно додати фільтр до нашого середовища - і можна його використовувати:</p>

<pre>
<code class="language-python">from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('yourapplication', 'templates'))
env.filters['dollars'] = dollars</code></pre>

<p>В шаблоні сторінки просто пишемо&nbsp;<strong>{{ value | dollars }}</strong>.&nbsp;</p>

<pre>
<code class="language-python">template = env.get_template('test.html')
print(template.render(value='one hundred'))
print(template.render(value='100'))</code></pre>

<p>поверне відповідно<strong>&nbsp;one hundred dollars</strong> і <strong>100$</strong>.</p>

<h3>Ресурси</h3>

<p><a href="http://jinja.pocoo.org/docs/dev/api/" target="_blank">Офіційна документації Jinja2</a></p>
