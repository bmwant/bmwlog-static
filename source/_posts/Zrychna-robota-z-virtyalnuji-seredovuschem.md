---
title: Зручна робота з віртуальний середовищем
date: 2016-02-07 16:12:21
tags: [python, virtualenv, venv, tools, bash]
author: Misha Behersky
---

<p>Коли працюєш над декількома проектами, в кожного з яких своє віртуальне середовище, стає незручно щоразу виконувати одні і ті ж команди для їх створення/активації/видалення. <a href="https://virtualenvwrapper.readthedocs.org/en/latest/" target="_blank">Vitrualenvwrapper</a> - класна утиліта, менеджер-обгортка для роботи з віртуальними середовищами. Вона має свою власну папку, де зберігають віртуальні середовища, тому відпадає необхідність додавати створену папку в ігнор системи контролю версій, вирішувати проблему, коли незрозуміло, чи середовище було створено з віртуальної чи хостової машини; і взагалі спрощує виконання повсякденних операцій з середовищами. Отож, встановлення і деякі основні команди і через пʼять хвилин ви вже будете працювати лише з цим інструментом.</p>

<p>Встановлюємо (працює з другою і третьою версіями). Є і <a href="https://pypi.python.org/pypi/virtualenvwrapper-win" target="_blank">версія для Вінди</a>, але її я не перевіряв.</p>

<pre>
<code class="language-bash">pip install virtualenvwrapper</code></pre>

<p>І додаємо команди для інтеграції з командним рядком (приклад для bash) у файл <strong>~/.bash_profile</strong></p>

<pre>
<code class="language-bash">export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/code
source /usr/local/bin/virtualenvwrapper.sh</code></pre>

<p>Перезавантажуємо консоль чи виконуємо <strong>source ~/.bash_profile</strong>.&nbsp;Готово, можна створювати віртуальні середовища</p>

<pre>
<code class="language-bash">mkvirtualenv test</code></pre>

<p>Середовище створиться і автоматично активується. Деактивувати можна тією ж командою <strong>deactivate</strong>.</p>

<h3>Список деяких команд</h3>

<p><strong>mkvirtualenv </strong> - створити віртуальне середовище</p>

<p><strong>mkvirtualenv &nbsp; --python /usr/bin/python</strong> - конкретно вказати інтерпретатор, для якого буде створено (наприклад, якщо працюєте з другою та третьою версіями на різних проектах)</p>

<p><strong>lsvirtualenv -b</strong> - показати список всіх середовищ&nbsp;(ключ для стислого виводу)</p>

<p><strong>rmvirtualenv test</strong> - видалити середовище</p>

<p><strong>workon </strong> - активувати середовище або відобразити список усіх, якщо назва не вказана</p>

<p><strong>cdvirtualenv</strong>&nbsp;- перейти в папку віртуального середовища</p>

<p><strong>cdsitepackages </strong>- перейти в папку зі встановленими пакетами. Це реально зручно, я б використовував лише задля цієї команди</p>

<p><strong>wipeenv</strong> - очистить середовище від усіх встановлених сторонніх бібліотек</p>

<p>Серед інших корисних штук: можна зробити автоматичну активацію при зміні папки, автоматичний запуск додаткових скриптів перед чи після активації і ще трохи іншого (див. документацію)</p>

<h3>Ресурси</h3>

<p><a href="https://virtualenvwrapper.readthedocs.org/en/latest/index.html" target="_blank">Офіційна документація (з повним списком команд)</a></p>