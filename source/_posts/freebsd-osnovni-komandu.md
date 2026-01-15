---
title: FreeBSD. Основні команди
date: 2015-01-27 09:40:34
tags: [freebsd, cheatsheet]
author: Misha Behersky
language: ua
archived: true
---

### Змінити свій пароль

```bash
$ passwd
```

### Створити папку

```bash
$ mkdir dirname
```

Створити кінцеву папку разом з проміжними, якщо вони не існують

```bash
$ mkdir -p path/to/directory
```

### Видалити файл

```bash
$ rm filename
```

### Перейменувати файл чи перемістити файл

```bash
$ mv old-file-name new-file-name
$ mv file1 file2
$ mv source target
```

### Перейти в режим суперюзера

```bash
$ su -
```

і ввести пароль. Для виходу натиснути `Ctrl`+`D` або ввести exit

### Надати права на папку і всі вкладені файли/папки для користувача

```bash
$ chown -R username dirname
```

### Встановити bash як стандартний шелл для користувача

```bash
$ cd /usr/ports/shells/bash
$ make install clean
$ chsh -s /usr/local/bin/bash username
```

### Подивитися інформацію про користувача (шелл, домашня директорія)

```bash
$ finger username
```

### Встановити wget

```bash
$ cd /usr/ports/ftp/wget
$ make install clean
```

### Встановити pip для python

```bash
$ cd /usr/ports/devel/py-pip/ && make install clean
$ pip install virtualenv
```

Обов'язково встановлюйте віртуальне оточення і для кожного проекту створюйте своє!

### Вивести вміст текстового файлу

```bash
$ cat filename.txt
```

### Редагувати файл за допомогою Easy Editor-а

```bash
$ ee filename.txt
```

### Оновити дерево портів

```bash
$ portsnap fetch update
```

### Знайти і завершити процес, запущений деякою програмою

Напрклад, подивитися, що позапускав Python

```bash
$ ps -fA | grep python
```

```
570  -  Ss     0:32.89 /usr/local/bin/python2.7 /usr/local/bin/supervisord
```

Першим числом в рядку буде `pid`, його і потрібно ввести в:

```bash
$ kill 570
```

### Переглянути всіх користувачів/групи

```bash
awk -F":" '{print $1}' /etc/passwd
awk -F":" '{print $1}' /etc/group
```

або

```bash
$ cat /etc/passwd | cut -d: -f1 | grep -v \#
$ cat /etc/group | cut -d: -f1 | grep -v \#
```

### Розпакувати .tar.gz архів

```bash
$ tar -zxvf arhive_name.tar.gz
```

`-z` - автоматична підтримка gzip стиснення
`-x` - розпакувати архів
`-v` - вивести на екран файли, які розпаковані
`-f` - файл архіву

### Ресурси

* [Декілька слів про ee (easy editor)](https://www.freebsd.org/doc/en/books/handbook/editors.html)
* [Сторінка wget](https://www.gnu.org/software/wget/)
