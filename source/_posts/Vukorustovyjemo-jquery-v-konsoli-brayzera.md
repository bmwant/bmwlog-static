---
title: Використовуємо jQuery в консолі браузера
date: 2015-06-15 22:02:32
tags: [jquery, cdn, javascript]
author: Misha Behersky
---

<p>Інколи необхідно використати в консолі можливості <a href="https://jquery.com" target="_blank">jQuery</a>, але на сайті бібліотека не підключена. Відкриваємо консоль <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd> і вводимо код&nbsp;</p>

<pre>
<code class="language-javascript">var jq = document.createElement('script');
jq.src = "http://code.jquery.com/jquery-2.1.4.js";
document.getElementsByTagName('head')[0].appendChild(jq);
jQuery.noConflict();</code></pre>

<p>Це створить в сторінці новий елемент &nbsp;для jQuery. Адресу можна взяти будь-яку (той же <a href="https://developers.google.com/speed/libraries/#jquery" target="_blank">Google CDN</a>), але врахуйте, якщо з&#39;єднання з сайтом встановлене через <strong>https</strong>, то і шлях до jQuery має бути по захищеному з&#39;єднанні (<em>https://code.jquery.com/jquery-2.1.4.js</em>).</p>

<p>Останній рядок <em>(jQuery.noConflict()</em>) звільняє змінну <strong>$</strong>, якщо вона використовується якимось іншими бібліотеками. Якщо ви хочете використовувати її разом&nbsp;з jQuery, то цей рядок необхідно прибрати.</p>

<p>Щоб дізнатися, чи підключений на сторінці jQuery і якщо так, то якої версії, потрібно ввести одну&nbsp;з команд:</p>

<pre>

<code class="language-javascript">$.fn.jquery;
jQuery.fn.jquery;</code></pre>

<p>Якщо не підключено - отримаєте помилку, в іншому разі - поточну версію.</p>

<p>&nbsp;</p>