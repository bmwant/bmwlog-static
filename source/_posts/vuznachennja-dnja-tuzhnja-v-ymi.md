---
title: Визначення дня тижня в умі
date: 2015-04-30 13:59:21
tags: [мнемоніка, обчислення]
author: Misha Behersky
language: ua
---

За допомогою даної методики можна визначити день тижня, знаючи дату від 1900 року до 2099. Для цього необхідно запам'ятати три зображення.

![year shift](/old/article/77867c6ad3023d0386086bfd8755114a.png)

**Зміщення року**

![month shift](/old/article/5c896ae58ef03c10b29ce64585d21d3a.png)

**Зміщення місяця**

### Алгоритм (на прикладі дати 25 серпня 2001)

* Визначаємо зміщення року. Для цього беремо найближчий менший високосний рік з таблиці (2000). Його зміщення - 0. Це число додаємо до різниці між роками (2001 - 2000 = 1), тобто 0 + 1 = **1**.
* Визначаємо зміщення місяця. Серпень відповідає цифрі **8** в сусідній таблиці.
* Додаємо до двох попередніх цифр число необхідної дати. 1 + 8 + 25 = **34**.
* Беремо остачу від ділення на 7. 34 % 7 = **6**. Це і буде шуканим днем тижня, тобто субота. Понеділок - 1, вівторок - 2, середа - 3, четвер - 4, п'ятниця - 5, субота - 6, неділя - 0.

> **УВАГА!** Якщо рік високосний, то для січня і лютого потрібно додатково відняти 1.

### Приклади

**5 лютого 1948 (високосний рік)**

* Зміщення 5. 5 + 0 = **5**.
* Лютий - **9**.
* 5 + 9 + 5 = 19. Не забуваємо відняти одницю для високосного року. 19 - 1 = **18**.
* 18 % 7 = 4. Четвер.

**10 вересня 2087 (трохи в майбутнє)**

0+3 +4 +10 %7 = 3. Середа!

Щоб простіше було запам'ятати таблички слід знати, що у першій числа ідуть з кроком 4 по стовпцях і з кроком 28 по рядках. Таблиця розміром 7х7. Друга відповідає порам року по рядкам, починаючи з весни, а по стовпцям ідуть числа від 2 до 9 у неспадному порядку згори вниз.

### Ресурси

* [Оригінал статті на Хабрі](http://habrahabr.ru/post/217389/)