---
title: LOCи, або Наскільки велика кодова база вашого проекту
date: 2016-07-21 15:08:31
tags: [python, kpidata, utils]
author: Misha Behersky
---

<p>В нас у KPIdata всі сервіси розділені на компоненти, кожному з яких відповідає окремий репозиторій</p>

<p><img alt="" src="/img/article/d35f448e63ea3dbf9a9c9fb3fbed944a.png" style="height:924px; width:632px" /></p>

<p>Коли кодова база розрослася - стало цікаво, як багато коду було написано, а саме: стандартний показник <a href="https://en.wikipedia.org/wiki/Source_lines_of_code" target="_blank">loc</a>&nbsp;(кількість рядків коду). Для цього є готовий зручний інструмент &nbsp;<a href="https://github.com/AlDanial/cloc" target="_blank">CLOC</a>. Встановити на Mac можна так</p>

<pre>
<code class="language-bash">brew install cloc</code></pre>

<p>&nbsp;Наявні&nbsp;також релізи&nbsp;і для багатьох інших ОС/пакетних менеджерів. Підтримується близько 200 мов. Подивитися повний список:</p>

<pre>
<code>clock --show-lang</code></pre>

<p>Оскільки нашою основною мовою є Python, було цікаво подивитися статистику саме для нього. Заходимо в папку з проектами і запускаємо</p>

<pre>
<code class="language-bash">cloc --exclude-dir=venv --include-lang=Python .</code></pre>

<p><img alt="" src="/img/article/842ba6e6ba823265b87a969d0bda757c.png" /></p>

<p>За допомогою -<strong>-exclude-dir</strong> можна задати папки, які не потрібно враховувати (в даному випадку, щоб бачити статистику лише по своєму коду, без сторонніх бібліотек). Аналогічно для <em>Javascript</em> можна заігнорувати <em>node_modules</em> чи <em>vendor</em>-папки</p>

<p><strong>--include-lang</strong> - список мов, які потрібно опрацювати, в даному випадку лише одна. Останнім параметром йде шлях до папки, дерево якої потрібно просканувати (крапка означає поточну директорію).</p>

<p>Майже, <em>19К</em> рядків власного коду, не враховуючи коментарі. Досить непогано! В наступному пості про <em>KPIdata</em>, покажу який в нас code coverage, що буде не дуже вражаючим, але тим не менш, розгляну, які інструменти ми для цього використовуємо.</p>

### Ресурси

* `http://kpidata.org` - Сайт KPIdata
* [Наші репозиторії на github](https://github.com/kpidata/)
