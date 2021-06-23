---
title: Python-нагадувалки #1
date: 2014-12-09 21:23:52
tags: [python, path, cheatsheet]
author: Misha Behersky
---

<h3>
 Робота з файлами
</h3>
<p>
 Наприклад, маємо такий файл:
 <em>
  "D:\files\doc.txt"
 </em>
</p>
<p>
</p>
<p>
 Отримати лише ім'я файлу (без повного шляху)
</p>
<pre>
<code class="language-python">file_path = r'D:\files\doc.txt'
file_name = os.path.basename(file_path)</code></pre>
<p>
 Аналогічно можна зробити, якщо вам потрібно дізнатися ім'я папки.
</p>
<p>
 Результат:
 <strong>
  'doc.txt'
 </strong>
</p>
<p>
</p>
<p>
 Розділити ім'я і розширення файлу
</p>
<pre>
<code class="language-python">file_only_name, file_extension = os.path.splitext(file_name)</code></pre>
<p>
 Результат:
 <strong>
  ('doc', '.txt')
 </strong>
</p>
<p>
</p>
<p>
 Отримати шлях до папки, в якій міститься файл
</p>
<pre>
<code class="language-python">dir_name = os.path.dirname(r'D:\files\doc.txt')</code></pre>
<p>
 Результат:
 <strong>
  'D:\\files'
 </strong>
</p>
<p>
</p>
<p>
 Перевірити, чи існує файл/папка
</p>
<pre>
<code class="language-python">os.path.exists(file_path)</code></pre>
<p>
</p>
<p>
 Створити дерево папок (створюються також всі проміжні папки, якщо потрібно)
</p>
<pre>
<code class="language-python">os.makedirs('D:/files/one/two/three')</code></pre>
<p>
</p>
<p>
 Створити порожній файл
</p>
<pre>
<code class="language-python">with open('D:/files/new_file.txt', 'a'):
    pass</code></pre>
<p>
 Відкривати потрібно саме з параметром
 <em>
  'a'
 </em>
 , тоді якщо файл існує - він не буде стертий. Відпадає додаткова перевірка на наявність файлу.
</p>
<p>
</p>
<p>
 Весь код перевірений на
 <strong>
  Python 3.4
 </strong>
 , але повинен також працювати і в
 <strong>
  2.6.x+
 </strong>
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="https://docs.python.org/3.4/library/os.path.html" target="_blank">
  Документація по os.path
 </a>
</p>