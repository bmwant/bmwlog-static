---
title: Unable to find vcvarsall.bat
date: 2015-05-13 11:28:27
tags: [python, windows]
author: Misha Behersky
---

<p>Така помилка виникає, коли ви намагаєтесь встановити додатковий модуль для Python, який написаний на C/C++. Але його спочатку треба скомпілювати для вашої системи. Для цього потрібно встановити компілятор від Microsoft, який іде в комплекті з Microsoft Visual C++ 2010 Express (можна завантажити безкоштовно <a href="https://www.visualstudio.com/en-us/products/visual-studio-express-vs.aspx" target="_blank">звідси</a>, посилання внизу сторінки). Метод&nbsp;працює для Python 3, 32-bit. Для Python 2, можливо буде потрібна 2008 версія.</p>

<p>Якщо немає часу встановлювати компілятор або з якихось причин дане рішення не допомагає, можна завантажити попередньо скомпільовані пакети для різних версій пайтона/операційної системи. Повний список <a href="http://www.lfd.uci.edu/~gohlke/pythonlibs/" target="_blank">тут</a>. Завантажуєте файл *.whl і у віртуальному оточенні виконуєте команду</p>

<pre>
<code class="language-bash">pip install module_name_and_version.whl</code></pre>

<p><strong>UPD.</strong>&nbsp;&nbsp;Microsoft Visual C++ 9.0 для Python 2.7 можна <a href="http://aka.ms/vcpython27" target="_blank">завантажити звідси</a>.</p>