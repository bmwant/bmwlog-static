---
title: Ставимо Python 3.5 на Ubuntu
date: 2015-10-20 17:39:12
tags: [python, pip]
author: Misha Behersky
---

<p>На початку вересня <a href="https://www.python.org/downloads/release/python-350/" target="_blank">вийшов реліз</a> нового Пайтона (3.5) з купою крутих штук, особливо це корутини з <em>async/await </em>синтаксисом.</p>

<h3>Ставимо новий</h3>

<pre>
<code class="language-bash">apt-get install build-essential
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar -xvzf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
make install</code></pre>

<p>Щоб перевірити, просто вводимо в терміналі</p>

<pre>
<code class="language-bash">python3.5</code></pre>

<p>що має запустити інтерактивне середовище інтерпретатора. Можна додатково навідатися в папку <em>/usr/local/bin</em> і переконатися, що він там лежить плюс для впевненості&nbsp;</p>

<pre>
<code class="language-bash">which python3.5</code></pre>

<p>покаже, який саме виконуваний файл (звідки) викликається, коли ви вводите дану команду.</p>

<h3>Піп на місці?</h3>

<pre>
<code class="language-bash">pip3.5 -V</code></pre>

<p>повинен видати версію і місце, звідки він викликається. Якщо виникли проблеми з його встановленням, а саме фігурувала помилка&nbsp;</p>

<p><strong>Ignoring ensurepip failure: pip 7.1.2 requires SSL/TLS</strong></p>

<p>потрібно поставити бібліотеки для SSL</p>

<pre>
<code class="language-bash">apt-get install libssl-dev openssl</code></pre>

<p>і ще раз виконати команди&nbsp;<strong>make, make install</strong>.</p>

<p>Насолоджуємося Пайтоном!</p>

<p><img alt="" src="/img/article/f3bc846c15df350593a8543c35bfa643.jpg" style="height:514px; width:406px" /></p>

<h3>UPD.</h3>

<p>Якщо в інтерпретаторі під час натисннення кнопки вгору (має з&rsquo;явитися попередньо введена команда) відображаються незрозумілі символи типу&nbsp;<strong>^[[A&nbsp;</strong>- це означає, що інтерпретатор був зібраний без&nbsp;<em>якогось-там-дуже-важливого-прапорця</em>&nbsp;(flag). Щоб виправити цю проблему</p>

<pre>
<code class="language-bash">sudo apt-get install libreadline-dev
make
make install</code></pre>

<p>&nbsp;</p>