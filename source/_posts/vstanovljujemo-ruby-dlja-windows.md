---
title: Встановлюємо Ruby для Windows
date: 2015-05-14 17:02:14
tags: [ruby, windows, mongo]
author: Misha Behersky
language: ua
---

Встановити Ruby для Windows дуже просто, оскільки є спеціальний сайт [RubyInstaller](http://rubyinstaller.org/) з готовими інсталяторами. Завантажуємо [інсталятор](http://dl.bintray.com/oneclick/rubyinstaller/rubyinstaller-2.2.2.exe), а також [набір для розробки](http://dl.bintray.com/oneclick/rubyinstaller/DevKit-mingw64-32-4.7.2-20130224-1151-sfx.exe) (може знадобитися для встановлення додаткових розширень). Після встановлення основного файлу і розпаковки іншого, переходимо в його директорію і виконуємо команди

```shell
ruby dk.rb init
ruby dk.rb review
ruby dk.rb install
```

Все, Рубі готовий до використання. Перевіряємо його запуск і версію

```shell
ruby --version
```

### Genghis

Я встановлював Рубі, щоб мати змогу запустити веб-додаток для адміністрування MongoDB: [Genghis](http://genghisapp.com/). Щоб встановити його потрібно виконати такі команди

```shell
gem install bson_ext -v 1.9.2
gem install genghisapp
```

Далі запускаємо його командою

```shell
genghisapp
```

принаймні, так написано в документації. В мене запускатися таким чином відмовилося, тому запасний варіант: заходимо в папку _gem_-ів (приблизно десь тут `C:\Ruby22\lib\ruby\gems\2.2.0\gems`), і переходимо до genghisapp. Звідти викликаємо консоль і вводимо

```shell
ruby genghis.rb
```

Тепер можна заходити на [localhost:4567](http://localhost:4567/) і використовувати адмінку для Mongo.

### Ресурси

* [Офіційний сайт мови програмування Ruby](https://www.ruby-lang.org/en/)
