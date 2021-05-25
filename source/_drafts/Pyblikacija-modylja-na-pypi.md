---
title: Публікація модуля на PyPI
date: 2015-05-27 10:40:43
tags: [pypi, pip, distutils]
author: Misha Behersky
---

<p>Отже, ви написали модуль, яким хочете поділитися з іншими, зробити свій вклад в розвиток Python-а, або просто хочете мати можливість встановлювати свій модуль чере pip. <a href="https://pypi.python.org/pypi" target="_blank">PyPI (Python Packages Index)</a> - це офіційний репозиторій модулів для Python. Для початку необхідно зареєструватися там. Після цього потрібно підготувати&nbsp;модуль (для початку вважаємо, що у нас є модуль <em>mymodule.py</em>, де міститься весь потрібний функціонал):&nbsp;за допомогою <a href="https://docs.python.org/3/library/distutils.html" target="_blank">distutils</a>&nbsp;створити скрипт встановлення. Створюємо файл <em>setup.py</em> з подібним вмістом</p>

<pre>
<code class="language-python">from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='MyModule',
      version='1.0',
      py_modules=['mymodule'],
      author='Most Wanted',
      author_email='bmwant@gmail.com',
      url='http://bmwlog.pp.ua',
      description='Short module description',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
      ],
      long_description=long_description,
)</code></pre>

<p>Вказуємо назву, версію, інформацію про автора та короткий опис. Якщо у вас файл детального опису у форматі <a href="http://docutils.sourceforge.net/rst.html" target="_blank">reStructuredText</a>&nbsp;(такий часто використовують на Github, якщо потрібно звідкись взяти приклад) - в <em>long_description </em>записуємо текст з цього файлу або просто вводимо його вручну. Особливу увагу варто приділити <em>classifiers</em>: це дозволяє віднести ваш модуль до певної категорії, що допоможе знайти його іншим і вибрати серед аналогів. Список класифікаторів можна <a href="https://pypi.python.org/pypi?%3Aaction=list_classifiers" target="_blank">подивитися тут</a>. Якщо є проблеми з вибором ліцензії, можна не вказувати її взагалі або скористатися <a href="http://choosealicense.com" target="_blank">помічником</a>. В більшості випадків підійде <a href="http://en.wikipedia.org/wiki/MIT_License" target="_blank">MIT License</a>. Коли файл готовий можна приступити до створення архіву для встановлення.</p>

<pre>
<code class="language-bash">python setup.py check
python setup.py sdist</code></pre>

<p>Це створить в папці dist архів вашого модуля з усіма необхідними файлами.</p>

<p>Якщо все пройшло успішно - можна завантажити ваш модуль в репозиторій</p>

<pre>
<code class="language-bash">python setup.py sdist upload</code></pre>

<p>Потрібно буде ввести логін і пароль вашого зареєстрованого акаунта (вам запропонують зберегти ці параметри у файлі <em>.pypirc</em>, щоб не вводити їх кожного разу) - і все: ваш модуль тепер доступний всім.</p>

<pre>
<code class="language-bash">pip install mymodule</code></pre>

<p>Отак просто! Після оновлення модуля - змінюємо&nbsp;версію і статус розробки (якщо потрібно) і вводимо команду</p>

<pre>
<code class="language-bash">python setup.py sdist upload</code></pre>

<p>Тепер, коли є декілька версій програми, можна встановлювати конкретну або оновлюватися до останної за допомогою команд</p>

<pre>
<code class="language-bash">pip install mymodule==1.2
pip install mymodule --upgrade</code></pre>

<p>В наступній статті я хочу більш детально описати скрипт <em>setup.py</em>, ознайомити з форматом написання <em>README</em>-файлів та публікацією пакетів (більш складних модулів та додаткових файлів).</p>

<p>Вдалої розробки.</p>