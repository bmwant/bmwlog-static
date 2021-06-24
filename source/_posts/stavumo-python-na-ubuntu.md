---
title: Ставимо Python 3.5 на Ubuntu
date: 2015-10-20 17:39:12
tags: [python, pip, ubuntu]
author: Misha Behersky
language: ua
---

На початку вересня [вийшов реліз](https://www.python.org/downloads/release/python-350/) нового Пайтона (3.5) з купою крутих штук, особливо це корутини з `async/await` синтаксисом.

### Ставимо новий

```bash
$ apt-get install build-essential
$ wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
$ tar -xvzf Python-3.5.0.tgz
$ cd Python-3.5.0
$ ./configure
$ make
$ make install
```

Щоб перевірити, просто вводимо в терміналі

```bash
$ python3.5
```

що має запустити інтерактивне середовище інтерпретатора. Можна додатково навідатися в папку `/usr/local/bin` і переконатися, що він там лежить. Плюс для впевненості

```bash
$ which python3.5
```

покаже, який саме виконуваний файл (звідки) викликається, коли ви вводите дану команду.

### Піп на місці?

```bash
$ pip3.5 -V
```

повинен видати версію і місце, звідки він викликається. Якщо виникли проблеми з його встановленням, а саме фігурувала помилка

```
Ignoring ensurepip failure: pip 7.1.2 requires SSL/TLS
```

потрібно поставити бібліотеки для SSL

```bash
$ sudo apt-get install libssl-dev openssl
```

і ще раз виконати команди `make`, `make install`.

Насолоджуємося Пайтоном!

![python pleasure](/old/article/f3bc846c15df350593a8543c35bfa643.jpg)

### UPD.

Якщо в інтерпретаторі під час натисннення кнопки вгору (має з'явитися попередньо введена команда) відображаються незрозумілі символи типу `^[[A` - це означає, що інтерпретатор був зібраний без *якогось-там-дуже-важливого-прапорця* (flag). Щоб виправити цю проблему

```bash
$ sudo apt-get install libreadline-dev
$ make
$ make install
```
