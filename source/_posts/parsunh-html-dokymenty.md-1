---
title: Парсинг html-документу
date: 2015-03-15 19:26:27
tags: [parsing]
author: Misha Behersky
language: ua
---

### Чудовий суп

Для початку встановимо бібліотеку [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)

```bash
$ pip install beautifulsoup4
```

Вона дозволяє здійснювати навігацію, пошук та зміну html-дерева. З її допомогою можна з легкістю розпарсити потрібний документ.

Отож, завдання: потрібно знайти весь код всередині `pre-code` блоку, який має клас `language-html` і екранувати всі символи. Це потрібно для того, щоб у тексті статті блок html-коду відображався як текст, а не як дійсний елемент. Зробити це дуже просто (використовуємо css-селектор)

```python
import cgi
from bs4 import BeautifulSoup

soup = BeautifulSoup(html)

for elem in soup.select('pre > code.language-html'):
    new_content = cgi.escape(elem.renderContents())
    elem.string = new_content

print(soup)
```

І далі кожен знайдений елемент замінюємо на його екранований вміст за допомогою модуля `cgi`

### Ресурси

* [Документація Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Екранування в cgi](https://docs.python.org/2/library/cgi.html#cgi.escape)
