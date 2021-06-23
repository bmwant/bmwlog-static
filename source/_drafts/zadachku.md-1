---
title: Задачки #1
date: 2015-04-29 13:25:58
tags: [python, логіка]
author: Misha Behersky
language: ua
---

<h3>Знайти помилку в коді</h3>

<p>Є реалізація функції, яка приймає непорожній&nbsp;масив <strong>arr</strong> з <strong>n</strong>&nbsp;цілочисельних значень у неспадному порядку і число <strong>k</strong>&nbsp;та перевіряє, чи містить даний масив значення 1, 2, ..., k (кожне число від 1 до k щонайменше один раз). Всі інші числові значення заборонені.</p>

<p><em>Обмеження:&nbsp;</em></p>

<ul>
	<li>n, k - числа на відрізку [1; 300 000]</li>
	<li>arr містить цілі числа з діапазону [0; 1 000 000 000]</li>
	<li>arr відсортований у неспадному порядку</li>
</ul>

<p><em>Приклади вхідних даних:</em></p>

<ul>
	<li>([1, 1, 2, 3, 3], 3) -&gt; True</li>
	<li>([1, 1, 3], 2) -&gt; False</li>
</ul>

<p><em>Код:&nbsp;</em></p>

<pre>
<code class="language-python">def solution(arr, k):
    n = len(arr)
    for i in xrange(n-1):
        if arr[i]+1 &lt; arr[i+1]:
            return False
    if arr[0] != 1 and arr[n-1] != k:
        return False
    else:
        return True</code></pre>

<p><em>Рішення:</em></p>

<p>В циклі ми перевіряємо, щоб кожен елемент + 1 був більший або рівний наступного. Цим забезпечується перевірка на неспадний порядок. Але серед вхідних даних може бути і нуль, тому такий контрприклад валиться:&nbsp;<strong>([1, 0, 0, 1, 2], 2)</strong>. потрібно додати перевірку на нуль. Підводний камінь: <strong>обмеження на вхідні дані</strong>.</p>

<pre>
<code class="language-python">if arr[i]+1 &lt; arr[i+1] or arr[i] == 0:
    return False</code></pre>

<p>Друга помилка: <strong>логічні оператори</strong>. Наступна перевірка здається логічною: перший елемент - це одиниця, останній елемент - це k, а оскільки всі елементи між ними йдуть з кроком нуль або один, то всі необхідні умови виконані.</p>

<p>and перевіряє виконання одразу обох умов, тому якщо перший елемент не одиниця, але останній k або останній не k, проте перший одиниця - повернеться результат True. Контрприклади:&nbsp;<strong>([1, 2, 2, 3, 3], 8)</strong>,&nbsp;<strong>([3, 4, 4, 5, 5], 5)</strong></p>

<pre>
<code class="language-python">if arr[0] != 1 or arr[n-1] != k:
    return False</code></pre>

<p><em>Правильний код:</em></p>

<pre>
<code class="language-python">def solution(arr, k):
    n = len(arr)
    for i in xrange(n-1):
        if arr[i]+1 &lt; arr[i+1] or arr[i] == 0:
            return False
    if arr[0] != 1 or arr[n-1] != k:
        return False
    else:
        return True</code></pre>

<h3>Сортування масиву</h3>

<p>Є непорожній масив <strong>arr</strong>, що містить <strong>n</strong> цілих чисел. Ви можете здійснити одну операцію обміну. Вона приймає два індекси <strong>i</strong>, <strong>j</strong> такі, що <strong>0 &lt;= i &lt;= j &lt; n</strong> та міняє місцями значення <strong>arr[i]</strong> та <strong>arr[j]</strong>. Написати функцію, яка на основі вхідного масиву буде перевіряти, чи можна здійснити сортування за неспаданням цього масиву, викоставши щонайбліьше одну операцію обміну.</p>

<p><em>Обмеження:&nbsp;</em></p>

<ul>
	<li>n&nbsp;- число&nbsp;на відрізку [1; 100]</li>
	<li>arr містить цілі числа з діапазону [1; 1 000 000 000]</li>
</ul>

<p><em>Приклади вхідних даних:</em></p>

<ul>
	<li>([1, 3, 5, 3, 7]) -&gt; True</li>
	<li>([1, 3, 5, 3, 4]) -&gt; False</li>
</ul>

<p><em>Рішення:</em></p>

<p>Наївне рішення перебором: беремо пари всіх можливих індексів і робимо для них операцію обміну. Якщо після цього масив стає відсортованим, повертаємо True.</p>

<pre>
<code class="language-python">def solution(arr):
    n = len(arr)
    arr_sorted = sorted(arr)
    for j in xrange(0, n):
        for i in xrange(0, j):
        arr_copy = arr[:]
        arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
        if arr_copy == arr_sorted:
            return True
    return False</code></pre>

<h3>Мінімальна відстань</h3>

<p>Є непорожній масив&nbsp;<strong>arr</strong>, що містить&nbsp;<strong>n</strong>&nbsp;невід&#39;ємних чисел. Для різних елементів <strong>arr[p]</strong> та <strong>arr[q]</strong> (тобто <strong>p != q</strong>) вводиться поняття відстанні:</p>

<ul>
	<li>arr[p] - arr[q], якщо arr[p] - arr[q] &gt;= 0</li>
	<li>arr[q] - arr[p], якщо&nbsp;arr[p] - arr[q] &lt; 0</li>
</ul>

<p>Напишіть функцію, яка буде визначати мінімальну відстань між двома різними елементами для даного масиву.&nbsp;</p>

<p><em>Обмеження:</em></p>

<ul>
	<li>n&nbsp;- число&nbsp;на відрізку [2; 100 000]</li>
	<li>arr містить цілі числа з діапазону [0; 1 000 000]</li>
</ul>

<p><em>Приклади вхідних даних:</em></p>

<ul>
	<li>([8, 24, 3, 20, 1, 17]) -&gt; 2</li>
	<li>([7, 21, 3, 42, 3, 7]) -&gt; 0</li>
</ul>

<p><em>Рішення:</em></p>

<p>Сортуємо масив і послідовно для пар шукаємо їхню відстань. Найменшу записуємо в результуючу змінну.</p>

<pre>
<code class="language-python">def solution(arr):
    min_dist = 1000000
    arr.sort()
    for i in in xrange(len(arr)-1):
        dist = abs(a[i]-a[i+1])
        if dist &lt; min_dist:
            min_dist = dist
    return min_dist</code></pre>

<h3>Підрахунок п&#39;ятірок</h3>

<p>Напишіть програму, яка буде отримувати на вхід два цілих числа <strong>i</strong>, <strong>j</strong>&nbsp;і повертати скільки елементів на даному проміжку діляться на 5 без остачі.</p>

<p><em>Обмеження:&nbsp;</em></p>

<ul>
	<li>i, j&nbsp;- числа на відрізку [1; 100 000], i &lt; j</li>
</ul>

<p><em>Приклади вхідних даних:</em></p>

<ul>
	<li>(14, 25) -&gt; 3</li>
	<li>(13, 17) -&gt; 1</li>
	<li>(35, 55) -&gt; 5</li>
	<li>(88, 89) -&gt; 0</li>
</ul>

<p><em>Рішення:</em></p>

<p>Перший спосіб - просто використати цикл і лічильник:</p>

<pre>
<code class="language-python">def solution(i, j):
    counter = 0
    for k in range(i, j+1):
        if k%5 == 0:
            counter += 1
    return counter</code></pre>

<p>Другий спосіб - скористатись математичними операціями для прискорення обчислень. Знаходимо ліву та праву поправки (відстань вліво та вправо до найближчих чисел, що кратні п&#39;яти) та ділимо довжину цього проміжку на 5, враховуючи значення поправок.</p>

<pre>
<code class="language-python">def solution(i, j):
    l_adj = i%5
    r_adj = 5 - j%5
    length = j - i + l_adj + r_adj
    result = length / 5
    if l_adj == 0:
        result += 1
    if r_adj != 0:
        result -= 1
    return result</code></pre>

<p>Або включаємо ліву межу, або не забуваємо виключити зайвий елемент правої межі.</p>

<p>Другий спосіб дає значний приріст швидкодії: <strong>0.0029&nbsp;</strong>с проти <strong>56&nbsp;</strong>с (час на 10 000 повторів для проміжку [1; 100 000])</p>
