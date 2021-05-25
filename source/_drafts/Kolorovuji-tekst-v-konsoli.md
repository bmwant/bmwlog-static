---
title: Кольоровий текст в консолі
date: 2016-07-24 16:29:49
tags: [python, utils, console]
author: Misha Behersky
---

<p>Коли потрібно виводити багато тексту в консоль, хочеться мати можливість зробити акцент на деяких більш важливих рядках (змінити колір, додати фон, зробити <a href="http://pikabu.ru/story/shutki_pro_tvoyu_zhirnuyu_mamu_1834442" target="_blank">жирним</a>). Для цього я дуже зручна бібліотека <a href="https://github.com/gravmatt/py-term" target="_blank">py-term</a></p>

<pre>
<code>pip install py-term</code></pre>

<p>сумісна з другим і третім Пайтоном.</p>

<p>Простий приклад використання</p>

<pre>
<code class="language-python">import term

term.write('Will be in ')
term.write('one line\n', term.bold)

term.writeLine('Custom color', term.green)

text = term.format('And custom background', term.white, term.bgblue)
term.writeLine(text)

# Clear text from color escape sequences
formatted = text.encode()
clear = term.strip(text)
print(formatted)
print(clear)</code></pre>

<p><img alt="" src="/img/article/06e9f736ceae3a0b9858c8098afeacc7.png" style="height:124px; width:600px" /></p>

<p>Також серед доступних можливостей: позиціонування курсору, вирівнювання тексту, очищення екрану, очищення певного рядка, встановлення довільного заголовку вікна.</p>

<h3>Список доступних кольорів для тексту</h3>

<p><img alt="" src="/img/article/6f90e79a88e8365e96c9ec2bd64ee166.png" style="height:402px; width:280px" /></p>

<h3>Список доступних кольорів для фону</h3>

<p><img alt="" src="/img/article/51c9a8560ecf3dfbbba630f606b92d27.png" style="height:371px; width:280px" /></p>