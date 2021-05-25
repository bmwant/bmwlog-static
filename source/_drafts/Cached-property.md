---
title: Cached property
date: 2016-04-13 18:19:01
tags: [python, tips, snippets]
author: Misha Behersky
---

<p>Інколи поле об&#39;єкта, до якого потрібно отримувати доступ, дуже довго обраховується і щоб кожного разу не викликати дорогу операцію, можна його закешувати. Наприклад</p>

<pre>
<code class="language-python">class Car(object):
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
</code></pre>

<p>Щоб отримати деяку властивість інколи потрібно багато рахувати або здійснювати запит до стороннього сервісу. Якщо вважати, що після цього дана властивість не буде змінюватися, можна скористатися простим декоратором:</p>

<pre>
<code class="language-python">from functools import wraps


def cached_property(func):
    @wraps(func)
    def get(self):
        if not hasattr(self, '_cached'):
            self._cached = func(self)
        return self._cached
    return property(get)</code></pre>

<p>Він збереже результат викликаної функції в атрибут обʼєкта і таким чином наступні рази доступ буде відбуватися до уже порахованих даних.</p>

<p>Щоб отримати більший контроль, можна скористатися готовою бібліотекою <a href="https://pypi.python.org/pypi/cached-property" target="_blank">cached-property</a>. Вона дозволяє кожного разу не копіювати даний код собі у проект, дає змогу&nbsp;інвалідувати кеш, працює з тредами, можна навіть встановлювати таймаути.</p>

<h3>Ресурси</h3>

<p><a href="http://code.activestate.com/recipes/576563-cached-property/" target="_blank">Рецепти від ActiveState</a></p>

<p><a href="https://docs.python.org/3/library/functools.html#functools.lru_cache" target="_blank">Кешування для викликів функцій</a></p>