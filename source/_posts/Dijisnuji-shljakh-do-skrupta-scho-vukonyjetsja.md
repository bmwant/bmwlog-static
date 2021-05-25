---
title: Дійсний шлях до скрипта, що виконується
date: 2015-12-08 12:12:51
tags: [python, inspect]
author: Misha Behersky
---

<p>Досі щоб дізнатися ім&#39;я файлу, що зараз виконується чи шлях до нього, я використовував такі конструкції</p>

<pre>
<code class="language-python">import os

print(__file__)
print(os.path.abspath(__file__))
</code></pre>

<p>Та виявляється, що цей код буде виконуватися як очікується, не у всіх випадках. Наприклад, якщо ми маємо два модуля <strong>one.py</strong> (з вмістом, наведеним вище)&nbsp;і <strong>two.py</strong>, то під час запуску останнього з кодом</p>

<pre>
<code class="language-python">execfile('one.py')</code></pre>

<p>отримаємо насправді назву і шлях для файлу <strong>two.py</strong>.</p>

<p>Такі кейси трапляються досить рідко, але для вирішення цієї проблеми можна скористатися модулем <em>inspect</em></p>

<pre>
<code class="language-python">import inspect

print(inspect.getfile(inspect.currentframe()))</code></pre>

<p>Цей фрагмент коду <em>завжди</em> буде повертати ім&rsquo;я файлу&nbsp;модуля, з якого виконується код.</p>

<h3>Ресурси</h3>

<p><a href="https://pymotw.com/2/inspect/" target="_blank">Використання модуля inspect</a></p>