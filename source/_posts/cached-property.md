---
title: Cached property
date: 2016-04-13 18:19:01
tags: [python, tips, snippets]
author: Misha Behersky
language: ua
---

Інколи поле об'єкта, до якого потрібно отримувати доступ, дуже довго обраховується і щоб кожного разу не викликати дорогу операцію, можна його закешувати. Наприклад

```python
class Car(object):
    @property
    def speed(self):
        """
        To retrieve speed property we need to look under the hood and
        carefully examine all the stuff, so it could take too much time
        """
        time.sleep(10)
        return 450


very_fast_car = Car()
print(very_fast_car.speed)

# Oh, I forget what was the speed of that car
print(very_fast_car.speed)
```

Щоб отримати деяку властивість інколи потрібно багато рахувати або здійснювати запит до стороннього сервісу. Якщо вважати, що після цього дана властивість не буде змінюватися, можна скористатися простим декоратором:

```python
from functools import wraps


def cached_property(func):
    @wraps(func)
    def get(self):
        if not hasattr(self, '_cached'):
            self._cached = func(self)
        return self._cached
    return property(get)
```

Він збереже результат викликаної функції в атрибут об'єкта і таким чином наступні рази доступ буде відбуватися до уже порахованих даних.

Щоб отримати більший контроль, можна скористатися готовою бібліотекою [cached-property](https://pypi.python.org/pypi/cached-property). Вона дозволяє кожного разу не копіювати даний код собі у проект, дає змогу інвалідувати кеш, працює з тредами, можна навіть встановлювати таймаути.

### Ресурси

* [Рецепти від ActiveState](http://code.activestate.com/recipes/576563-cached-property/)
* [Кешування для викликів функцій](https://docs.python.org/3/library/functools.html#functools.lru_cache)
