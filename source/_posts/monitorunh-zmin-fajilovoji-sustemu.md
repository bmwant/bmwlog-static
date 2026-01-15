---
title: Моніторинг змін файлової системи
date: 2015-05-14 14:31:30
tags: [python, windows, filesystem]
author: Misha Behersky
language: ua
archived: true
---

Щоб виконувати зміни, відповідно до подій файлової системи для Пайтона існує бібліотека [Watchdog](http://pythonhosted.org/watchdog/). Взагалі аналогів існує багато, а принцип роботи полягає в тому, що скрипт з певним інтервалом часу перевіряє всі файли у списку моніторингу, і якщо дата модифікації файлу змінилася, виконуються необхідні дії. Я також писав схожу штуку, код можна подивитися [на гітхабі](https://github.com/bmwant/Reloader). Для Linux-систем існує трохи інший підхід, коли ядро операційної системи само сповіщує про зміни у файловій системі. Так відпадає необхідність постійно в циклі опитувати мільярд файлів. На основі цього побудована бібліотека [pyinotify](https://github.com/seb-m/pyinotify).

Отож, завдання полягає в тому, щоб скрипт повідомляв про редагування файлів певного типу (python-скрипти) в поточній папці. Створюємо новий клас обробника, де вказуємо необхідні патерни для файлів.

```python
class ScriptModifiedHandler(PatternMatchingEventHandler):
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
        pass
```

Чотири методи: `on_modified`, `on_moved`, `on_deleted`, `on_created` дозволяють зробити окремий обробник для кожної події. Ми будемо просто виводити текст в консоль і лише на модифікацію файлу. Далі потрібно додати спостерігача, який буде використовувати даний обробник.

```python
observer = Observer()
path = '.'
event_handler = ScriptModifiedHandler()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

Створюємо екземпляр _Спостерігача_ і _Обробника_ і вказуємо для спостерігача папку, за якою наглядати (`recursive=True` вказує, що за підпапками також треба слідкувати, `path` - шлях до потрібної папки. Крапка відповідає директорії, з якої запущений скрипт). Повний код скрипта [gist](https://gist.github.com/bmwant21/b5042ad3896c73261cc1). Запустити так

```bash
$ python watch.py
```

Спробуйте відредагувати ще якийсь _*.py_-файл і отримайте нотифікацію про це в консоль. Зупинити виконання можна комбінаціює `Ctrl`+`C`.
