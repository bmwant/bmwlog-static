---
title: Python. Подорожі в часі
date: 2015-08-28 14:54:44
tags: [python, time, datetime, calendar]
author: Misha Behersky
---

<p>В цій статті я хочу розказати про основні операції з датами/часом, які дозволяє здійснювати Пайтон за допомогою модулів стандартної бібліотеки. Мова бути йти про функції з використанням модулів <a href="https://docs.python.org/3.4/library/datetime.html" target="_blank">datetime</a>, <a href="https://docs.python.org/3.4/library/calendar.html" target="_blank">calendar</a>&nbsp;та <a href="https://docs.python.org/3.4/library/time.html" target="_blank">time</a>.</p>

<p><img alt="" src="/img/article/83fa02bc24fd39908afbea54f501e061.jpg" style="height:430px; width:800px" /></p>

<p>Почнемо з перетворень між датами та їх представленнями у вигляді рядків.</p>

<p>Надалі будемо говорити про дату як про об&#39;єкт типу <strong>datetime.datetime,</strong> який містить такі атрибути: рік, місяць, день, година, хвилина, секунда, мікросекунда та інформація про часовий пояс.</p>

<h3>Перетворити рядок заданого формату в дату</h3>

<pre>
<code class="language-python">import datetime
date_str = '23/10/2016 15:32'
date_format = '%d/%m/%Y %H:%M'
result = datetime.datetime.strptime(date_str, date_format)</code></pre>

<p>Щоб отримати інформацію стосовно специфікаторів формату дати можна звернутися до <a href="https://docs.python.org/3.4/library/datetime.html#strftime-strptime-behavior" target="_blank">офіційної документації</a> або до <a href="http://strftime.org" target="_blank">цієї класної шпаргалки</a>.</p>

<h3>Перетворити дату в рядок заданого формату</h3>

<pre>
<code class="language-python">date = datetime.datetime.now()
date_format = '%x %X'
result = date.strftime(date_format)</code></pre>

<p>Даний код перетворить поточний <em>даточас </em>в представлення дати та часу відповідно до вашої поточної локалізації.</p>

<h3>Отримати початок дня для дати</h3>

<pre>
<code class="language-python">result = date.replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)</code></pre>

<h3>Отримати дату без інформації про часовий пояс</h3>

<pre>
<code class="language-python">result = date.replace(tzinfo=None)</code></pre>

<p>Це може знадобитися, щоб порівнювати дати з датами, що не мають інформації про часовий пояс, додавати чи віднімати їх. Але будьте уважні, бо таким способом можна втратити кілька годин).</p>

<h3>Отримати перше число попереднього місяця</h3>

<pre>
<code class="language-python">date = datetime.date.today()  # or any another date you want
first_day = datetime.date(day=1, month=date.month, year=date.year)
prev_month = first_day - datetime.timedelta(days=1)
result = datetime.datetime(year=prev_month.year, month=prev_month.month, day=1)</code></pre>

<p>Спочатку отримуємо перший день для місяця нашої дати. Потім віднімаємо від нього один день - так ми перейдемо на попередній місяць. І наостанок, сформуємо об&#39;єкт дати для першого числа отриманого місяця. Такі маніпуляції потрібні, щоб не робити додаткових перевірок на кількість днів у місяці, перший/останній місяць року.</p>

<h3>Перетворити time_struct/timestamp&nbsp;в datetime</h3>

<pre>
<code class="language-python">time_struct = time.strptime(date_str, date_format)
date = datetime.datetime.fromtimestamp(time.mktime(time_struct))</code></pre>

<p>mktime спочатку перетворить <em>часоструктуру</em> в кількість секунд, що пройшли з початку <a href="https://en.wikipedia.org/wiki/Unix_time" target="_blank">Епохи</a> (1 січня 1970 року), а потім створить новий об&#39;єкт дати.</p>

<h3>Порівняти date та datetime дати</h3>

<p>Якщо у вас є об&#39;єкт , отриманий, наприклад, як <em>datetime.date.today() </em>і його потрібно порівняти з екземпляром класу <em>datetime.datetime</em>, то приведемо останній з використанням методу <em>date()</em></p>

<pre>
<code class="language-python">the_date = datetime.datetime.now()
the_date = the_date.replace(day=the_date.day+1)
today = datetime.date.today()
the_date &gt; today  # TypeError: can't compare datetime.datetime to datetime.date
the_date.date() &gt; today  # True</code></pre>

<h3>Перетворити дату в кількість секунд/мілісекунд</h3>

<pre>
<code class="language-python">date_seconds = time.mktime(date.timetuple())
mls = date_seconds * 1000
result = int(mls)
</code></pre>

<h3>Порівняти дві дати за форматом</h3>

<p>Таке може знадобитися, якщо потрібно перевірити, чи співпадає рік і день в дат з різними місяцями і часом (не обов&#39;язково цей приклад, порівнювати можна за будь-яким форматом)</p>

<pre>
<code class="language-python">date_one  # 2015-08-28 15:57:29.615660
date_two  # 2015-07-28 11:32:57.294810
date_format = '%Y %d'
formatted_one = date_one.strftime(date_format)
formatted_two = date_two.strftime(date_format)
result = formatted_one == formatted_two</code></pre>

<h3>Інформація про дату</h3>

<p>Отримати інформацію про дату: день, місяць, рік, номер дня у році, номер дня тижня, номер тижня у році, чи високосний рік.</p>

<pre>
<code class="language-python">print('Day number: %s' % date.day)
print('Month number: %s' % date.month)
print('Current year: %s' % date.year)
print('Day of the year: %s' % date.timetuple().tm_yday)
print('Day of week number: %s' % date.isoweekday())
print('Week of year number: %s' % date.isocalendar()[1])
print('Is leap year: %s' % calendar.isleap(date.year))</code></pre>

<h3>І наостанок</h3>

<p>Надрукувати календар для обраного року в консоль</p>

<pre>
<code class="language-python">import calendar
calendar.prcal(2015)</code></pre>

<p>Сніпет коду до всіх прикладів можна знайти <a href="https://bitbucket.org/snippets/MostWanted/98LMK" target="_blank">тут на бітбакеті</a>.</p>

<h3>Ресурси</h3>

<p>Додаткові модулі, які полегшать роботу з датами</p>

<p><a href="http://labix.org/python-dateutil" target="_blank">dateutil - конвертації, парсинг, арифметика над датами</a></p>

<p><a href="http://pytz.sourceforge.net" target="_blank">pytz - модуль для роботи з часовими поясами</a></p>

<p><a href="http://delorean.readthedocs.org/en/latest/" target="_blank">delorean - спрощена робота з датами плюс генерація дат</a></p>

<p><a href="https://pymotw.com/2/time/" target="_blank">Стаття про time в &quot;модулі тижня&quot; (PyMOTW)</a></p>