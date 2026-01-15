---
title: Python-нагадувалки
date: 2014-12-09 21:23:52
tags: [python, path, cheatsheet]
author: Misha Behersky
language: ua
archived: true
---

### Робота з файлами

Наприклад, маємо такий файл: `D:\files\doc.txt`.

* Отримати лише ім'я файлу (без повного шляху)

```python
file_path = r'D:\files\doc.txt'
file_name = os.path.basename(file_path)
```

Аналогічно можна зробити, якщо вам потрібно дізнатися ім'я папки.
Результат: `doc.txt`

* Розділити ім'я і розширення файлу

```python
file_only_name, file_extension = os.path.splitext(file_name)
```

Результат: `('doc', '.txt')`

* Отримати шлях до папки, в якій міститься файл

```python
dir_name = os.path.dirname(r'D:\files\doc.txt')
```

Результат: `D:\\files`

* Перевірити, чи існує файл/папка

```python
os.path.exists(file_path)
```

* Створити дерево папок (створюються також всі проміжні папки, якщо потрібно)

```python
os.makedirs('D:/files/one/two/three')
```

* Створити порожній файл

```python
with open('D:/files/new_file.txt', 'a'):
    pass
```

Відкривати потрібно саме з параметром `'a'`, тоді якщо файл існує - він не буде стертий. Відпадає додаткова перевірка на наявність файлу.

Весь код перевірений на `Python 3.4`, але повинен також працювати і в `2.6.x+`.

### Ресурси

* [Документація по os.path](https://docs.python.org/3.4/library/os.path.html)
