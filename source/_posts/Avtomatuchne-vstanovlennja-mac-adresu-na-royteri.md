---
title: Автоматичне встановлення MAC-адреси на роутері
date: 2015-07-19 14:03:54
tags: [dd-wrt, mac, router]
author: Misha Behersky
---

<p>На роутері D-Link DIR-615 з прошивкою dd-wrt виникла проблема: після перезавантаження злітає MAC (просто змінюється на попереднє значення). Щоб цього не відбувалося, достатньо виконати такі дії:</p>

<ol>
	<li>Зайти у веб-інтерфейс та перейти<em> Administation-&gt;Commands</em></li>
	<li>Вставити команди:
	<pre>
<code class="language-bash">nvram set wan_hwaddr="11:22:33:AA:BB:FF"

stopservice wan
startservice wan</code></pre>
	</li>
	<li>Натиснути&nbsp;<em>Save startup</em>.</li>
</ol>

<p>Тепер після перезавантажень мак буде встановлюватися автоматично в потрібне вам значення (не забудьте змінити&nbsp;<strong>11:22:33:AA:BB:FF</strong>&nbsp;на вашу адресу). Якщо це не буде працювати, можна спробувати додати команду&nbsp;<strong>nvram commit</strong>&nbsp;перед <strong>stopservice wan</strong>. Тепер не потрібно щоразу заходити в розділ <em>MAC Address Clone</em>&nbsp;і застосовувати зміни.</p>