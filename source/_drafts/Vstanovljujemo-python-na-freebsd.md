---
title: Встановлюємо Python на FreeBSD
date: 2014-10-20 21:19:14
tags: [freebsd, python]
author: Misha Behersky
---

<p>
 Спочатку виконуємо команду
 <strong>
  wget
 </strong>
 для завантаження архіву. Замість
 <strong>
  2.7.8
 </strong>
 можна вказати останню версію, доступну на даний момент.
</p>
<pre>
<code class="language-bash">wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz --no-check-certificate

tar -xzvf Python-2.7.8.tgz

cd Python-2.7.8

./configure

make 

make install</code></pre>
<p>
 Далі вводимо команду
 <strong>
  python
 </strong>
 і в консолі повинні отримати повідомлення від інтерпретатора з номером щойно встановленої версії Python-а.
</p>
<p>
 Далі встановлюємо
 <strong>
  pip
 </strong>
 та
 <strong>
  virtual environment
 </strong>
</p>
<pre>
<code class="language-bash">cd /usr/ports/devel/py-pip/ &amp;&amp; make install clean

pip install virtualenv</code></pre>
<p>
 Щоб почати роботу з проектом виконуємо команди
</p>
<pre>
<code class="language-bash">cd /path/to/your/project
virtualenv venv
source venv/bin/activate
</code></pre>
<p>
 По закінченню вводимо команду
 <strong>
  deactivate
 </strong>
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="https://www.python.org/downloads/" target="_blank">
  Перевірити останню версію Python
 </a>
</p>