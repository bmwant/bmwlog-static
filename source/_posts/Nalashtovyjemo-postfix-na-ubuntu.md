---
title: Налаштовуємо Postfix на Ubuntu
date: 2015-03-19 18:58:34
tags: [postfix, mail, ubuntu]
author: Misha Behersky
---

<p>Якщо потрібна лише можливість відправляти пошту з сервера, при цьому не налаштовувати і обслуговувати повноцінний поштовий сервер (що досить довго-незручно-важко), можна скористатись <a href="http://en.wikipedia.org/wiki/Message_transfer_agent" target="_blank"> MTA </a> <a href="http://www.postfix.org" target="_blank"> Postfix </a> . Його використовують близько 25% всіх публічних поштових серверів. Для початку встановлюємо його і вказуємо доменне ім&#39;я вашого серверу ( <em> example.com </em> )</p>

<pre>
<code class="language-bash">apt-get install postfix</code></pre>

<p>Далі змінюємо рядок конфігурації на те ж саме ім&#39;я</p>

<pre>
<code class="language-bash">nano /etc/postfix/main.cf</code></pre>

<p>Не забудьте вказати MX-запис у налаштуваннях реєстратора вашого доменного імені, який б теж вказував на ваш сервер ( <em> example.com </em> ). Перезапускаємо Postfix</p>

<pre>
<code class="language-bash">service postfix restart</code></pre>

<p>Щоб протестувати роботу достатньо відправити лист з будь-якої вашої поштової скриньки на адресу <strong> username@example.com. </strong> <em> username </em> - ім&#39;я деякого користувача в системі. Перевірити вхідні можна, переглянувши папку <strong> /var/mail/ </strong></p>