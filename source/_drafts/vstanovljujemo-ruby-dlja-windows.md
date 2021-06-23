---
title: Встановлюємо Ruby для Windows
date: 2015-05-14 17:02:14
tags: [ruby, windows, mongo]
author: Misha Behersky
---

<p>Встановити Ruby для Windows дуже просто, оскільки є спеціальний сайт <a href="http://rubyinstaller.org/" target="_blank">RubyInstaller</a> з готовими&nbsp;інсталяторами. Завантажуємо <a href="http://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-2.2.2.exe" target="_blank">інсталятор</a>, а також <a href="http://dl.bintray.com/oneclick/rubyinstaller/DevKit-mingw64-32-4.7.2-20130224-1151-sfx.exe" target="_blank">набір для розробки</a> (може знадобитися для встановлення додаткових розширень). Після встановлення основного файлу і розпаковки іншого, переходимо в його директорію і виконуємо команди</p>

<pre>
<code class="language-bash">ruby dk.rb init
ruby dk.rb review
ruby dk.rb install</code></pre>

<p>Все, Рубі готовий до використання. Перевіряємо його запуск і версію</p>

<pre>
<code class="language-bash">ruby --version</code></pre>

<h3>Genghis</h3>

<p>Я встановлював Рубі, щоб мати змогу запустити веб-додаток для адміністрування MongoDB: <a href="http://genghisapp.com/" target="_blank">Genghis</a>. Щоб встановити його потрібно виконати такі команди</p>

<pre>
<code class="language-bash">gem install bson_ext -v 1.9.2
gem install genghisapp
</code></pre>

<p>Далі запускаємо його командою</p>

<pre>
<code class="language-bash">genghisapp</code></pre>

<p>принаймні, так написано в документації. В мене запускатися таким чином відмовилося, тому запасний варіант: заходимо в папку <strong>gem</strong>-ів (приблизно десь тут&nbsp;<em>C:\Ruby22\lib\ruby\gems\2.2.0\gems</em>), і переходимо до genghisapp. Звідти викликаємо консоль і вводимо</p>

<pre>
<code class="language-bash">ruby genghis.rb</code></pre>

<p>Тепер можна заходити на&nbsp;<a href="http://localhost:4567/" target="_blank">localhost:4567</a>&nbsp;і використовувати адмінку для Mongo.</p>

<h3>Ресурси</h3>

<p><a href="https://www.ruby-lang.org/en/" target="_blank">Офіційний сайт мови програмування Ruby</a></p>