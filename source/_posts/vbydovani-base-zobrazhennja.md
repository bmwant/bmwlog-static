---
title: Вбудовані base64 зображення
date: 2016-07-08 16:44:14
tags: [python, js, html, web]
author: Misha Behersky
language: ua
---

[HTML дозволяє](http://caniuse.com/#feat=datauri) задавати зображення прямо в тегові за допомогою `dataURI` (зображення у вигляді base64-кодованого тексту). Виглядає це так

```html
<img alt="Embedded Image" src="data:image/png;base64,iVBORw0KGgoA...">
```

Якщо потрібно відрендерити шаблон, який буде використовувати такі зображення на бекенді, можна використати [base64](https://docs.python.org/3/library/base64.html) зі стандартної бібліотеки. Приклад для [Flask-у](http://flask.pocoo.org/) (можна використати аналогічний підхід будь-де).

```python
import base64

from flask import Flask, render_template


app = Flask(__name__, template_folder='.')


@app.route('/')
def hello():
    with open('image.png', 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return render_template('template.html', image=encoded_image)


if __name__ == '__main__':
    app.run()
```

І сам файл шаблону `template.html`

```html
<!DOCTYPE html>
<html>

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>Test embedded</title>
</head>

<body>
  <p>Image below</p>
  <img src="data:image/png;base64,{{image}}">
</body>
</html>
```

В результаті отримаємо сторінку з тегом зображення, яке вже вбудоване і не потребує виконання ще одного запиту до серверу.

![moo](/old/article/28f73ca4dbf238649ee84949766e1d65.png)

### Ресурси

* [Переваги використання вбудованих зображень](https://varvy.com/pagespeed/base64-images.html)
* [RFC на стандарт](https://tools.ietf.org/html/rfc2397)
