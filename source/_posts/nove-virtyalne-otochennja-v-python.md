---
title: Нове віртуальне оточення в Python 3
date: 2015-05-05 12:45:29
tags: [virtualenv, windows, python]
author: Misha Behersky
language: ua
archived: true
---

Починаючи з версії 3.3 підтримка віртуальних оточень була додана до стандартної бібліотеки. Створити віртуальне оточення тепер можна просто командою

```bash
$ pyenv venv
```

замість встановлення virtualenv і виконання команди

```bash
$ virtualenv venv
```

Але у Windows не захотіли додавати скрипт pyenv в папку `C:\Python34\Scripts`, а натомість він лежить в папці `C:\Python34\Tools\Scripts` у вигляді пайтон-скрипта. Тому існують такі альтернативні варіанти:

1. Прописати повним шляхом

```bash
$ C:\Python34\python C:\Python34\Tools\Scripts\pyvenv.py venv
```

або якщо `python.exe` доданий у вас до змінної `PATH`

```bash
$ python C:\Python34\Tools\Scripts\pyvenv.py venv
```

2. За допомогою запуска модуля бібліотеки як скрипта (ключ `-m`)

```bash
$ python -m venv venv
```

Перший _venv_ - це назва модуля, другий - назва папки з вашим віртуальним оточенням.

3. Створити власний скрипт pyenv

В папці `C:\Python34\Scripts` створюємо файл `pyenv.bat` з таким вмістом

```
python C:\Python34\Tools\Scripts\pyvenv.py %*
```

`%*` вказує передати всі введені в консоль аргументи відповідному скриптові. Тепер можна виконувати найпершу згори команду, що буде давати аналогічний результат.

Активувати і вийти з віртуального оточення можна звичними командами `venv\scripts\activate` та `deactivate`.
