---
title: Працюємо з MongoDB в Python
date: 2015-04-12 21:42:14
tags: [python, mongo]
author: Misha Behersky
---

<p>MongoDB - це не реляційна, документно-орієнтована база даних. Якщо проводити паралелі зі звичайними базами даних (MySQL і т.д.), то маємо таку термінологію:</p>

<p><strong>База даних</strong> (теж база даних) - структорований, впорядкований набір даних, які ви хочете зберігати</p>

<p><strong>Колекція</strong> (таблиця) - набір пов&#39;язаних між собою за певним критерієм даних. База даних складається з колекцій.</p>

<p><strong>Документ</strong> (рядок/запис в таблиці) - структурна одиниця даних; документи об&#39;єднуються в колекції. Документи зберігаються у JSON-подібному вигляді (а саме <a href="http://docs.mongodb.org/meta-driver/latest/legacy/bson/" target="_blank">BSON</a>, якщо говорити про використання зі стандартними структурами пайтона). Структура: набір полів і відповідних значень для них.</p>

<p><img alt="" src="/img/article/5c2577a023b539caaf679a0b9e898725.png" style="height:170px; width:570px" /></p>

<p>Перевагами монго є: відновлення після збоїв, автоматичне масштабування, підтримка динамічної структури документів (немає жорсткої прив&#39;язки до наперед визначеної схеми), вбудовані документи і масиви як альтернатива складним join-ам, і <em>документи</em>, які є аналогами стандартних структур даних в багатьох мовах програмування (dict в пайтоні). Досить теорії - працюємо з монго за допомогою клієнта PyMongo.</p>

<p>Для початку завантажуємо/встановлюємо/запускаємо&nbsp;<a href="https://www.mongodb.org/downloads" target="_blank">монго</a>&nbsp;або використовуємо <s>отримані незаконним шляхом</s> реквізити доступу до віддаленого серверу. Піп-піп</p>

<pre>
<code class="language-bash">pip install pymongo</code></pre>

<h3>Підключаємось</h3>

<pre>
<code class="language-python">from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)</code></pre>

<p>Один клієнт може працювати одразу з декількома (всіма) базами даних. Щоб вибрати потрібно базу можна використовувати доступ по атрибуту через крапку або словник-подібну нотацію</p>

<pre>
<code class="language-python">db = client.posts_db
db = client['posts_db']</code></pre>

<h3>Працюємо з документами</h3>

<pre>
<code class="language-python">db = client.posts_db  # database
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
print(posts.find_one(post_id))</code></pre>

<p>Можна додавати один або одразу декільки елементів масивом. При додаванні кожного елемента документу присвоюється спеціальне поле &#39;_id&#39;, унікальне для колекції. Якщо у вас є це поле у текстовому вигляді, то знайти відповідний документ можна так:</p>

<pre>
<code class="language-python">from bson.objectid import ObjectId
post_id_str = '552ab4dd6d54671af8c1ca0e'
the_post = posts.find_one({'_id': ObjectId(post_id_str)})</code></pre>

<p>Оновлюємо необхідний документ&nbsp;і рахуємо кількість всіх записів в колекції</p>

<pre>
<code class="language-python">posts.update({'_id': post_id}, {'$set': {'text': 'Updated text'}}, upsert=False)
print(posts.find({'author': 'Mike').count())
print(posts.count())</code></pre>

<p>Додати унікальний запис до масиву, наприклад оновити теги до запису, щоб не було повторів</p>

<pre>
<code class="language-python">posts.update({'_id': post_id}, {'$addToSet': {'tags': 'mongo'}})
posts.update({'_id': post_id}, {'$addToSet': {'tags': 'newpag'}})
the_post = posts.find_one(post_id)
print(the_post['tags'])</code></pre>

<p>Буде доданий лише другий тег.</p>

<p>І наостанок: вибрати випадковий документ з колекції. Для цієї достатньо необхідної задачі існує багато рішень, ось одне з не дуже складних</p>

<pre>
<code class="language-python">import random

number = random.randint(1, posts.count())
pp = posts.find().limit(-1).skip(number).next()
print(pp['text'])</code></pre>

<p><strong>Увага! </strong>Остання версія PyMongo на момент написання статті - 3.0, використана тут - 2.6. Назви деяких методів чи їх поведінка могла змінитися, тому при виникненні помилок звертайтесь до документації. Встановити конкретну версію можна явно вказавши це в pip</p>

<pre>
<code class="language-bash">pip install pymongo==2.6.3</code></pre>

<h3>Ресурси</h3>

<p><a href="http://docs.mongodb.org/manual/tutorial/getting-started/" target="_blank">Документація Монго</a></p>

<p><a href="https://api.mongodb.org/python/current/" target="_blank">Документація PyMongo (спочатку читати це)</a></p>

<p><a href="http://www.mongodbmanager.com" target="_blank">Графічний клієнт для Windows (щоб подивитися на створену базу)</a></p>