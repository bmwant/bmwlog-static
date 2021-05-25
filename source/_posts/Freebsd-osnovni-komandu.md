---
title: FreeBSD. Основні команди
date: 2015-01-27 09:40:34
tags: [freebsd, cheatsheet]
author: Misha Behersky
---

<h3>
 Змінити свій пароль
</h3>
<pre>
<code class="language-bash">passwd</code></pre>
<h3>
 Створити папку
</h3>
<pre>
<code class="language-bash">mkdir dirname</code></pre>
<p>
 Створити кінцеву папку разом з проміжними, якщо вони не існують
</p>
<pre>
<code class="language-bash">mkdir -p path/to/directory</code></pre>
<h3>
 Видалити файл
</h3>
<pre>
<code class="language-bash">rm filename</code></pre>
<h3>
 Перейменувати файл чи перемістити файл
</h3>
<pre>
<code class="language-bash">mv old-file-name new-file-name
mv file1 file2
mv source target</code></pre>
<h3>
 Перейти в режим суперюзера
</h3>
<pre>
<code class="language-bash">su -</code></pre>
<p>
 і ввести пароль. Для виходу натиснути Ctrl+D або ввести exit
</p>
<h3>
 Надати права на папку і всі вкладені файли/папки для користувача
</h3>
<pre>
<code class="language-bash">chown -R username dirname</code></pre>
<h3>
 Встановити bash як стандартний шелл для користувача
</h3>
<pre>
<code class="language-bash">cd /usr/ports/shells/bash
make install clean
chsh -s /usr/local/bin/bash username</code></pre>
<h3>
 Подивитися інформацію про користувача (шелл, домашня директорія)
</h3>
<pre>
<code class="language-bash">finger username</code></pre>
<h3>
 Встановити wget
</h3>
<pre>
<code class="language-bash">cd /usr/ports/ftp/wget
make install clean</code></pre>
<h3>
 Встановити pip для python
</h3>
<pre>
<code class="language-bash">cd /usr/ports/devel/py-pip/ &amp;&amp; make install clean

pip install virtualenv</code></pre>
<p>
 <strong>
  Обов'язково встановлюйте віртуальне оточення і для кожного проекту створюйте своє!
 </strong>
</p>
<h3>
 Вивести вміст текстового файлу
</h3>
<pre>
<code class="language-bash">cat filename.txt</code></pre>
<h3>
 Редагувати файл за допомогою Easy Editor-а
</h3>
<pre>
<code class="language-bash">ee filename.txt</code></pre>
<h3>
 Оновити дерево портів
</h3>
<pre>
<code class="language-bash">portsnap fetch update</code></pre>
<h3>
 Знайти і завершити процес, запущений деякою програмою
</h3>
<p>
 Напрклад, подивитися, що позапускав Python
</p>
<pre>
<code class="language-bash">ps -fA | grep python</code></pre>
<p>
 <strong>
  570  -  Ss     0:32.89 /usr/local/bin/python2.7 /usr/local/bin/supervisord
 </strong>
</p>
<p>
 Першим числом в рядку буде
 <em>
  pid
 </em>
 , його і потрібно ввести в:
</p>
<pre>
<code class="language-bash">kill 570</code></pre>
<h3>
 Переглянути всіх користувачів/групи
</h3>
<pre>
<code class="language-bash">awk -F":" '{print $1}' /etc/passwd
awk -F":" '{print $1}' /etc/group</code></pre>
<p>
 або
</p>
<pre>
<code class="language-bash">cat /etc/passwd | cut -d: -f1 | grep -v \#
cat /etc/group | cut -d: -f1 | grep -v \#</code></pre>
<h3>
 Розпакувати .tar.gz архів
</h3>
<pre>
<code class="language-bash">tar -zxvf arhive_name.tar.gz</code></pre>
<p>
 <strong>
  -z
 </strong>
 автоматична підтримка gzip стиснення
</p>
<p>
 <strong>
  -x
 </strong>
 розпакувати архів
</p>
<p>
 <strong>
  -v
 </strong>
 вивести на екран файли, які розпаковані
</p>
<p>
 <strong>
  -f
 </strong>
 файл архіву
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="https://www.freebsd.org/doc/en/books/handbook/editors.html" target="_blank">
  Декілька слів про ee (easy editor)
 </a>
</p>
<p>
 <a href="https://www.gnu.org/software/wget/" target="_blank">
  Сторінка wget
 </a>
</p>