---
title: Встановлюємо бібліотеку cryptography
date: 2014-12-19 16:56:14
tags: [python, cryptography, pip, windows, wheels]
author: Misha Behersky
language: ua
archived: true
---

### Встановлюємо Cryptography для Windows

[Cryptography](https://cryptography.io/en/latest/) - бібліотека для роботи з криптографічними функціями у Python. Але встановити її [по інструкції](https://cryptography.io/en/latest/installation/#on-windows) мені так і не вдалося.
Для [pip](https://pip.pypa.io/en/latest/index.html) є крута штука, яка називається [wheels](http://pythonwheels.com). Це вже скомпільовані бібліотеки під вашу платформу, які пришвидшують встановлення і не потребують наявності компілятора.
Отож, для `Python 2.7, win32` [завантажуємо](https://pypi.python.org/packages/cp27/c/cryptography/cryptography-0.7.1-cp27-none-win32.whl#md5=05ed516ca15f25d2169f7629ed1da1d912670ee329ff) *wheel*-файл і виконуємо команду:

```bash
$ pip install cryptography-0.7.1-cp27-none-win32.whl
```

Аналогічно можна зробити для інших платформ і версій Python. Можливо знадобиться додатково встановити [OpenSSL](http://slproweb.com/products/Win32OpenSSL.html) (лінк в ресурсах).

### Ресурси

* [Курс з криптографії (англ.)](https://www.crypto101.io)
* [Cryptography на PyPi](https://pypi.python.org/pypi/cryptography)
* [OpenSSL для win32](http://slproweb.com/download/Win32OpenSSL-1_0_1j.exe)
