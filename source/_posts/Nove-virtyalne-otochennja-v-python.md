---
title: Нове віртуальне оточення в Python 3
date: 2015-05-05 12:45:29
tags: [virtualenv, windows]
author: Misha Behersky
---

<p>Починаючи з версії 3.3 підтримка віртуальних оточень була додана до стандартної бібліотеки. Створити віртуальне оточення тепер можна просто командою</p>

<pre>
<code class="language-bash">pyenv venv</code></pre>

<p>замість встановлення virtualenv і виконання команди</p>

<pre>
<code class="language-bash">virtualenv venv</code></pre>

<p>Але у Windows не захотіли додавати скрипт pyenv в папку&nbsp;<em>C:\Python34\Scripts</em>, а натомість він лежить в папці&nbsp;<em>C:\Python34\Tools\Scripts&nbsp;</em>у вигляді пайтон-скрипта. Тому існують такі альтернативні варіанти:</p>

<p>1.&nbsp;Прописати повним шляхом</p>

<pre>
<code class="language-bash">C:\Python34\python C:\Python34\Tools\Scripts\pyvenv.py venv
</code></pre>

<p>або якщо <em>python.exe </em>доданий у вас до змінної&nbsp;<em>PATH</em></p>

<pre>
<code class="language-bash">python C:\Python34\Tools\Scripts\pyvenv.py venv</code></pre>

<p>&nbsp;2. За допомогою запуска модуля бібліотеки як скрипта (ключ <em>-m</em>)</p>

<pre>
<code class="language-bash">python -m venv venv</code></pre>

<p>Перший venv - це назва модуля, другий - назва папки з вашим віртуальним оточенням.</p>

<p>3. Створити власний скрипт pyenv</p>

<p>В папці&nbsp;<em>C:\Python34\Scripts&nbsp;</em>&nbsp;створюємо файл <strong>pyenv.bat&nbsp;</strong>з таким вмістом</p>

<pre>
<code class="language-bash">python C:\Python34\Tools\Scripts\pyvenv.py %*</code></pre>

<p><strong>%* </strong>&nbsp;вказує передати всі введені в консоль аргументи відповідному скриптові. Тепер можна виконувати найпершу згори команду, що буде давати аналогічний результат.</p>

<p>Активувати і вийти з віртуального оточення можна звичними командами</p>

<pre>
<code class="language-bash">venv\scripts\activate</code></pre>

<p>та</p>

<pre>
<code class="language-bash">deactivate</code></pre>

<p>&nbsp;</p>