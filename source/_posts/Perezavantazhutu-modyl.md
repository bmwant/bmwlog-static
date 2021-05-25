---
title: Перезавантажити модуль
date: 2016-02-02 20:21:04
tags: [python, console, module]
author: Misha Behersky
---

<p>Часто виникає ситуація, коли потрібно протестити функцію з деякого модуля. Найпростіше досягти цього, відкривши інтерпретатор і в <a href="https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop" target="_blank">REPL-режимі</a>&nbsp;зробити необхідний виклик</p>

<pre>
<code class="language-bash">python
&gt;&gt;&gt; import module_name
&gt;&gt;&gt; module_name.test_function(5)
&gt;&gt;&gt; 10</code></pre>

<p>Але якщо функція модифікована (був оновлений код), ще один виклик все одно поверне той же результат, що очевидно є небажаною для нас (хоча і правильною, очікуваною) поведінкою. Найпростіший варіант - це перезапустити інтерпретатор&nbsp;</p>

<pre>
<code class="language-bash">&gt;&gt;&gt; quit()
python
&gt;&gt;&gt; ...</code></pre>

<p>і виконати ті ж самі команди, що є не дуже зручно. Тому рішення, <strong>Python 2</strong></p>

<pre>
<code class="language-bash">&gt;&gt;&gt; import module_name
&gt;&gt;&gt; module_name.test_function(5)
&gt;&gt;&gt; 10
&gt;&gt;&gt; reload(module_name)
&gt;&gt;&gt; module_name.test_function(5)
&gt;&gt;&gt; 25</code></pre>

<p><strong>Python 3</strong></p>

<pre>
<code class="language-bash">&gt;&gt;&gt; import imp
&gt;&gt;&gt; import module_name
&gt;&gt;&gt; module_name.test_function(5)
&gt;&gt;&gt; 10
&gt;&gt;&gt; imp.reload(module_name)
&gt;&gt;&gt; module_name.test_function(5)
&gt;&gt;&gt; 25</code></pre>

<p>дозволить зекономити час і прискорити тестування коду, що модифікується.</p>

<h3>Ресурси</h3>

<p><a href="https://docs.python.org/3/library/imp.html#imp.reload" target="_blank">Модуль imp для третьої версії</a></p>