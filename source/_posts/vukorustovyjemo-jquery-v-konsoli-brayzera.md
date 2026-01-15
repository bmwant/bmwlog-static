---
title: Використовуємо jQuery в консолі браузера
date: 2015-06-15 22:02:32
tags: [jquery, cdn, javascript]
author: Misha Behersky
language: ua
archived: true
---

Інколи необхідно використати в консолі можливості [jQuery](https://jquery.com), але на сайті бібліотека не підключена. Відкриваємо консоль `Ctrl`+`Shift`+`C` і вводимо код

```javascript
var jq = document.createElement('script');
jq.src = "http://code.jquery.com/jquery-2.1.4.js";
document.getElementsByTagName('head')[0].appendChild(jq);
jQuery.noConflict();
```

Це створить в сторінці новий елемент для jQuery. Адресу можна взяти будь-яку (той же [Google CDN](https://developers.google.com/speed/libraries/#jquery)), але врахуйте, якщо з'єднання з сайтом встановлене через `https`, то і шлях до jQuery має бути по захищеному з'єднанні (`https://code.jquery.com/jquery-2.1.4.js`).

Останній рядок `jQuery.noConflict()` звільняє змінну `$`, якщо вона використовується якимось іншими бібліотеками. Якщо ви хочете використовувати її разом з jQuery, то цей рядок необхідно прибрати.

Щоб дізнатися, чи підключений на сторінці jQuery і якщо так, то якої версії, потрібно ввести одну з команд:

```javascript
$.fn.jquery;
jQuery.fn.jquery;
```

Якщо не підключено - отримаєте помилку, в іншому разі - поточну версію.
