---
title: Підсвітка активного пункту меню
date: 2015-10-18 21:33:02
tags: [js, jquery, css]
author: Misha Behersky
---

<p>Простий сніпет, щоб додати клас <em>active</em> до елементу лінк вашого навбару.</p>

<pre>
<code class="language-javascript">function setActiveLink() {
    var currentPath = document.location.pathname;
    var selector = "a[href='" + currentPath + "']";
    var elem = document.querySelector(selector);
    if(elem !== null) {
        elem.setAttribute("class", "active");
    }
}</code></pre>

<p>Те ж саме з використання jQuery&nbsp;(плюс скидання всіх попередньо встановлених активних лінків)</p>

<pre>
<code class="language-javascript">function setActiveLink() {
    var currentPath = document.location.pathname;
    var selector = "a[href='" + currentPath + "']";
    $("nav a").removeClass("active");
    $(selector).addClass("active");
}</code></pre>

<p>&nbsp;</p>