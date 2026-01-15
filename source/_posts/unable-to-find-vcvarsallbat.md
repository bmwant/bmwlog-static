---
title: Unable to find vcvarsall.bat
date: 2015-05-13 11:28:27
tags: [python, windows]
author: Misha Behersky
language: ua
archived: true
---

Така помилка виникає, коли ви намагаєтесь встановити додатковий модуль для Python, який написаний на C/C++. Але його спочатку треба скомпілювати для вашої системи. Для цього потрібно встановити компілятор від Microsoft, який іде в комплекті з Microsoft Visual C++ 2010 Express (можна завантажити безкоштовно [звідси](https://www.visualstudio.com/en-us/products/visual-studio-express-vs.aspx), посилання внизу сторінки). Метод працює для Python 3, 32-bit. Для Python 2, можливо буде потрібна 2008 версія.

Якщо немає часу встановлювати компілятор або з якихось причин дане рішення не допомагає, можна завантажити попередньо скомпільовані пакети для різних версій пайтона/операційної системи. Повний список [тут](http://www.lfd.uci.edu/~gohlke/pythonlibs/). Завантажуєте файл `*.whl` і у віртуальному оточенні виконуєте команду

```bash
$ pip install module_name_and_version.whl
```

**UPD.** Microsoft Visual C++ 9.0 для Python 2.7 можна [завантажити звідси](http://aka.ms/vcpython27).
