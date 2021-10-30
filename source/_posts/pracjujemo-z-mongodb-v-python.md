---
title: Працюємо з MongoDB в Python
date: 2015-04-12 21:42:14
tags: [python, mongo]
author: Misha Behersky
language: ua
---

MongoDB - це нереляційна, документно-орієнтована база даних. Якщо проводити паралелі зі звичайними базами даних (MySQL і т.д.), то маємо таку термінологію:

**База даних** (теж база даних) - структорований, впорядкований набір даних, які ви хочете зберігати.

**Колекція** (таблиця) - набір пов'язаних між собою за певним критерієм даних. База даних складається з колекцій.

**Документ** (рядок/запис в таблиці) - структурна одиниця даних; документи об'єднуються в колекції. Документи зберігаються у JSON-подібному вигляді (а саме [BSON](http://docs.mongodb.org/meta-driver/latest/legacy/bson/), якщо говорити про використання зі стандартними структурами пайтона). Структура: набір полів і відповідних значень для них.

![mongodb logo](/images/mongomongo.png)

Перевагами монго є: відновлення після збоїв, автоматичне масштабування, підтримка динамічної структури документів (немає жорсткої прив'язки до наперед визначеної схеми), вбудовані документи і масиви як альтернатива складним join-ам, і _документи_, які є аналогами стандартних структур даних в багатьох мовах програмування (dict в пайтоні). Досить теорії - працюємо з монго за допомогою клієнта PyMongo.

Для початку завантажуємо/встановлюємо/запускаємо [монго](https://www.mongodb.org/downloads) або використовуємо ~отримані незаконним шляхом~ реквізити доступу до віддаленого серверу. Піп-піп


```bash
$ pip install pymongo
```

### Підключаємось

```python
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
```

Один клієнт може працювати одразу з декількома (всіма) базами даних. Щоб вибрати потрібно базу можна використовувати доступ по атрибуту через крапку або словник-подібну нотацію</p>

```python
db = client.posts_db
db = client['posts_db']
```

### Працюємо з документами

```python
db = client.posts_db  # database
posts = db.posts  # collection

post = {
    'author': 'Misha',
    'text': 'Blog post with Mongo',
    'tags': ['mongo', 'python', 'pymongo']
}  # document


post_id = posts.insert(post)
print(post_id)

new_posts = [
    {
        'author': 'Misha',
        'text': 'Another post',
        'tags': ['pag']
    },
    {
        'author': 'Mike',
        'text': 'The last post',
    }
]

posts.insert(new_posts)
print(posts.find_one(post_id))
```

Можна додавати один або одразу декільки елементів масивом. При додаванні кожного елемента документу присвоюється спеціальне поле `_id`, унікальне для колекції. Якщо у вас є це поле у текстовому вигляді, то знайти відповідний документ можна так:


```python
from bson.objectid import ObjectId
post_id_str = '552ab4dd6d54671af8c1ca0e'
the_post = posts.find_one({'_id': ObjectId(post_id_str)})
```

Оновлюємо необхідний документ і рахуємо кількість всіх записів в колекції

```python
posts.update({'_id': post_id}, {'$set': {'text': 'Updated text'}}, upsert=False)
print(posts.find({'author': 'Mike').count())
print(posts.count())
```

Додати унікальний запис до масиву, наприклад оновити теги до запису, щоб не було повторів

```python
posts.update({'_id': post_id}, {'$addToSet': {'tags': 'mongo'}})
posts.update({'_id': post_id}, {'$addToSet': {'tags': 'newpag'}})
the_post = posts.find_one(post_id)
print(the_post['tags'])
```

Буде доданий лише другий тег.

І наостанок: вибрати випадковий документ з колекції. Для цієї достатньо необхідної задачі існує багато рішень, ось одне з не дуже складних

```python
import random

number = random.randint(1, posts.count())
pp = posts.find().limit(-1).skip(number).next()
print(pp['text'])
```

> **Увага!** Остання версія PyMongo на момент написання статті - 3.0, використана тут - 2.6. Назви деяких методів чи їх поведінка могла змінитися, тому при виникненні помилок звертайтесь до документації. Встановити конкретну версію можна явно вказавши це в pip

```bash
$ pip install pymongo==2.6.3
```

### Ресурси

* [Документація Монго](http://docs.mongodb.org/manual/tutorial/getting-started/)
* [Документація PyMongo (спочатку читати це)](https://api.mongodb.org/python/current/)
* [Графічний клієнт для Windows (щоб подивитися на створену базу)](http://www.mongodbmanager.com)
