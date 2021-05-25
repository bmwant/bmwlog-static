---
title: Парсинг html-документу
date: 2015-03-15 19:26:27
tags: [parsing]
author: Misha Behersky
---

<h3>
 Чудовий суп
</h3>
<p>
 Для початку встановимо бібліотеку
 <a href="http://www.crummy.com/software/BeautifulSoup/" target="_blank">
  Beautiful Soup
 </a>
</p>
<pre>
<code class="language-bash">pip install beautifulsoup4</code></pre>
<p>
 Вона дозволяє здійснювати навігацію, пошук та зміну html-дерева. З її допомогою можна з легкістю розпарсити потрібний документ.
</p>
<p>
 Отож, завдання: потрібно знайти весь код всередині
 <strong>
  pre-code
 </strong>
 блоку, який має клас
 <strong>
  language-html
 </strong>
 і екранувати всі символи. Це потрібно для того, щоб у тексті статті блок html-коду відображався як текст, а не як дійсний елемент. Зробити це дуже просто (використовуємо css-селектор)
</p>
<pre>
<code class="language-python">import cgi
from bs4 import BeautifulSoup
soup = BeautifulSoup(html)
for elem in soup.select('pre &gt; code.language-html'):
    new_content = cgi.escape(elem.renderContents())
    elem.string = new_content

print(soup)</code></pre>
<p>
 І далі кожен знайдений елемент замінюємо на його екранований вміст за допомогою модуля
 <strong>
  cgi
 </strong>
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="http://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank">
  Документація Beautiful Soup
 </a>
</p>
<p>
 <a href="https://docs.python.org/2/library/cgi.html#cgi.escape" target="_blank">
  Екранування в cgi
 </a>
</p>