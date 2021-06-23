---
title: FreeBSD фікси помилок
date: 2014-12-20 15:27:12
tags: [freebsd, bugs]
author: Misha Behersky
---

<h3>
 pkg_add: unable to fetch / unable to get
</h3>
<p>
 Причиною помилки є неправильна змінна
 <em>
  PACKAGESITE
 </em>
 .
 <a href="ftp://ftp.freebsd.org/pub/FreeBSD/ports/">
  Тут
 </a>
 можна знайти правильний лінк для вашої системи.
</p>
<p>
 Для
 <em>
  FreeBSD 9.0
 </em>
 з
 <em>
  bash
 </em>
 команда виглядає таким чином:
</p>
<pre>
<code class="language-bash">export PACKAGESITE=ftp://ftp.freebsd.org/pub/FreeBSD/ports/i386/packages-9-stable/Latest/
</code></pre>
<p>
 Дізнатися версію ОС можна командою:
 <strong>
  uname -a
 </strong>
 .
</p>
<p>
 Виводимо нову змінну і перевіряємо коректну роботу:
</p>
<pre>
<code class="language-bash">echo $PACKAGESITE
pkg_add -r nginx</code></pre>
<h3>
 urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
</h3>
<p>
 Причиною є те, що у нових версіях Python за замовчування CA сертифікат шукається в папці
 <strong>
  /etc/ssl/cert.pem
 </strong>
</p>
<p>
 Фіксимо командою
</p>
<pre>
<code class="language-bash">ln -s /usr/local/etc/ssl/cert.pem /etc/ssl/cert.pem </code></pre>
<p>
</p>