---
title: YAML та Python
date: 2015-04-12 19:58:00
tags: [yaml, python, serialization]
author: Misha Behersky
archived: true
---

YAML (*YAML Ain't Markup Language*) - це стандарт серіалізації даних для багатьох мов програмування. Також його можна використовувати і для зберігання файлів-конфігурацій. Працювати з ним в Python достатньо просто. Якщо ви використовували [pickle](https://docs.python.org/2/library/pickle.html) або [json](https://docs.python.org/2/library/json.html) модулі, то тут все досить схоже. Підтримка реалізована модулем PyYAML.

Для швидкого встановлення використовуємо pip

```bash
pip install pyyaml
```

Створюємо файл конфігурації на основі словника

```python
import yaml

config = {
    'param1': 500,
    'param2': 'value2'
}

with open('config.txt', 'w') as fout:
    fout.write(yaml.dump(config))
```

Використовуємо цей файл в подальшому або іншою програмою

```python
with open('config.txt') as fin:
    cfg = yaml.load(fin.read())
    print(cfg['param1'])
```

Перехоплюємо помилки, якщо файл некоректний

```python
import yaml

try:
    config = yaml.load(file('config.txt'))
except yaml.YAMLError as exc:
    print('Error in configuration file: %s' % exc)
```

### Ресурси

* [Офіційний сайт YAML](http://yaml.org)
* [Документація PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation)
