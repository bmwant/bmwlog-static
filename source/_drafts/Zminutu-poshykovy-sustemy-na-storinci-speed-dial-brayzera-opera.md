---
title: Змінити пошукову систему на сторінці Speed Dial браузера Opera
date: 2015-07-05 21:24:14
tags: [opera, google]
author: Misha Behersky
language: ua
---

<p>Коли встановлюєш браузер Opera,&nbsp;за замовчуванням на панелі швидкого набору розміщений пошуковик Яндекс (стандартно для країн СНД).</p>

<p>Щоб змінити його на Google, потрібно:</p>

<ol>
	<li>Відкрити файл <strong>Local State</strong>&nbsp;у блокноті. Знайти його можна ввівши в адресному рядку&nbsp;<em>opera://about </em>(або просто вибрати в головному меню&nbsp;<em>About Opera</em>)&nbsp;і подивитися в категорію <em>Paths-&gt;Profile</em>.</li>
	<li>Закрити браузер.</li>
	<li>Змінити в цьому файлі значення на такі:&nbsp;&quot;country&quot;:&quot;<strong>us</strong>&quot;, &quot;country_from_server&quot;:&quot;<strong>US</strong>&quot;, &quot;timestamp&quot;:&quot;<strong>1485978822600000000</strong>&quot;.</li>
	<li>Відкрити Оперу і користуватися нормальним пошуковиком з Експрес-панелі.</li>
</ol>
