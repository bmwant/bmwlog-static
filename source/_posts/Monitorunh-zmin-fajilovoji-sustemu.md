---
title: Моніторинг змін файлової системи
date: 2015-05-14 14:31:30
tags: [python, windows, filesystem]
author: Misha Behersky
---

<p>Щоб виконувати зміни, відповідно до подій файлової системи для Пайтона існує бібліотека <a href="http://pythonhosted.org/watchdog/" target="_blank">Watchdog</a>. Взагалі аналогів існує багато, а принцип роботи полягає в тому, що скрипт з певним інтервалом часу перевіряє всі файли у списку моніторингу, і якщо дата модифікації файлу змінилася, виконуються необхідні дії. Я також писав схожу штуку, код можна подивитися <a href="https://github.com/bmwant21/Reloader" target="_blank">на гітхабі</a>. Для Linux-систем існує трохи інший підхід, коли ядро операційної системи само сповіщує про зміни у файловій системі. Так відпадає необхідність постійно в циклі опитувати мільярд файлів. На основі цього побудована бібліотека <a href="https://github.com/seb-m/pyinotify" target="_blank">pyinotify</a>.</p>

<p>Отож, завдання полягає в тому, щоб скрипт повідомляв про редагування файлів певного типу (python-скрипти) в поточній папці. Створюємо новий клас обробника, де вказуємо необхідні патерни для файлів.</p>

<pre>
<code class="language-python">class ScriptModifiedHandler(PatternMatchingEventHandler):
    patterns = ['*.py']

    def __init__(self):
        super(ScriptModifiedHandler, self).__init__()
        # you can add some init code here

    def process(self, event):
        print(event.src_path, event.event_type)

    def on_modified(self, event):
        self.process(event)
		
    def on_moved(self, event):
        pass
		
    def on_deleted(self, event):
        pass
		
    def on_created(self, event):
        pass</code></pre>

<p>Чотири методи: <em>on_modified</em>, <em>on_moved</em>, <em>on_deleted</em>, <em>on_created&nbsp;</em>дозволяють зробити окремий обробник для кожної події. Ми будемо просто виводити текст в консоль і лише на модифікацію файлу. Далі потрібно додати спостерігача, який буде використовувати даний обробник.</p>

<pre>
<code class="language-python">observer = Observer()
path = '.'
event_handler = ScriptModifiedHandler()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()</code></pre>

<p>Створюємо екземпляр <em>Спостерігача</em> і <em>Обробника</em> і вказуємо для спостерігача папку, за якою наглядати) (r<em>ecursive=True</em> вказує, що за підпапками також треба слідкувати, <em>path</em> - шлях до потрібної папки. Крапка відповідає директорії, з якої запущений скрипт).&nbsp;Повний код скрипта <a href="https://gist.github.com/bmwant21/b5042ad3896c73261cc1" target="_blank">gist</a>. Запустити так</p>

<pre>
<code class="language-bash">python watch.py</code></pre>

<p>Спробуйте відредагувати ще якийсь *.py-файл і отримайте нотифікацію про це в консоль. Зупинити виконання можна комбінаціює <kbd>Ctrl</kbd>+<kbd>C.</kbd></p>