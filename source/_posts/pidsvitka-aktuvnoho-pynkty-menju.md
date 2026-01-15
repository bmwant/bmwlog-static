---
title: Підсвітка активного пункту меню
date: 2015-10-18 21:33:02
tags: [js, jquery, css]
author: Misha Behersky
language: ua
archived: true
---

Простий сніпет, щоб додати клас `active` до елементу лінк вашого навбару.

```javascript
function setActiveLink() {
  var currentPath = document.location.pathname;
  var selector = "a[href='" + currentPath + "']";
  var elem = document.querySelector(selector);
  if(elem !== null) {
    elem.setAttribute("class", "active");
  }
}
```

Те ж саме з використання jQuery (плюс скидання всіх попередньо встановлених активних лінків)

```javascript
function setActiveLink() {
  var currentPath = document.location.pathname;
  var selector = "a[href='" + currentPath + "']";
  $("nav a").removeClass("active");
  $(selector).addClass("active");
}
```
