---
title: Пишемо просту нейронну мережу з нуля у 100 рядків коду
date: 2018-11-20 21:09:15
tags: [ai, neural-network, numpy, machine-learning, python]
author: Misha Behersky
language: ua
---

Привіт, зараз дуже популярними є напрямки [штучного інтелекту](https://uk.wikipedia.org/wiki/%D0%A8%D1%82%D1%83%D1%87%D0%BD%D0%B8%D0%B9_%D1%96%D0%BD%D1%82%D0%B5%D0%BB%D0%B5%D0%BA%D1%82), [нейронних мереж](https://uk.wikipedia.org/wiki/%D0%A8%D1%82%D1%83%D1%87%D0%BD%D0%B0_%D0%BD%D0%B5%D0%B9%D1%80%D0%BE%D0%BD%D0%BD%D0%B0_%D0%BC%D0%B5%D1%80%D0%B5%D0%B6%D0%B0) та [машинного навчання](https://uk.wikipedia.org/wiki/%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%B5_%D0%BD%D0%B0%D0%B2%D1%87%D0%B0%D0%BD%D0%BD%D1%8F). Все це побудовано на досить нескладних концептах, які можна відтворити, знаючи трохи математики та програмування. Саме це ми і зробимо сьогодні, використовуючи Python 3.

Для початку потрібно розуміти, що собою буде являти нейронна мережа. Будемо думати про неї, як про функцію, що отримує деякий набір вхідних даних та видає для них результат. Ззовні це виглядає як _чорний ящик_, внутрішню будову якого ми будемо розглядати. Отож, наше завдання - використовуючи набір вхідних даних навчити нашу нейронну мережу, щоб вона максимально точно відображала зв'язок вхідних та вихідних даних. Потрібно знайти найкращу [апроксимацію](https://uk.wikipedia.org/wiki/%D0%90%D0%BF%D1%80%D0%BE%D0%BA%D1%81%D0%B8%D0%BC%D0%B0%D1%86%D1%96%D1%8F) [функції відображення](https://uk.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D1%96%D1%8F_(%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0)) вхідних даних у вихідні.

### Вхідні дані
Щоб перевірити коректність роботи нашої мережі, ми будемо використовувати деяку зазделегідь відому нам функцію, яку ми використаємо для генерації вхідних даних, а також поведінку якої ми будемо намагатися повторити в процесі навчання. Отже, функція буде приймати 4 вхідних параметри `x1`, `x2`, `x3`, `x4` та повертати результат `y`, що рівний [виразу](https://uk.wikipedia.org/wiki/%D0%91%D1%83%D0%BB%D0%B5%D0%B2%D0%B0_%D0%B0%D0%BB%D0%B3%D0%B5%D0%B1%D1%80%D0%B0) `(x1 and x2) or (x3 and x4)`. [Область визначення](https://uk.wikipedia.org/wiki/%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C_%D0%B2%D0%B8%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%BD%D1%8F) та [область значень](https://uk.wikipedia.org/wiki/%D0%9E%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C_%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D1%8C) функції - множина з двох елементів `{0, 1}`

```python
def f(X):
    x1, x2, x3, x4 = X
    return (x1 or x2) and (x3 or x4)
```

Залишилось перебрати всі можливі комбінації і порахувати результат, що ми будемо використовувати як еталонний.

```python
from itertools import product
import pandas as pd

def main():
    columns = ['x1', 'x2', 'x3', 'x4', 'y']
    data = []
    for elem in product([0, 1], repeat=4):
        row = [*elem, f(elem)]
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    df.to_csv('data.csv', header=True, index=False)
```

Тут і далі в коді використовується бібліотека для роботи з даними [pandas](http://pandas.pydata.org/pandas-docs/stable/) (взагалі, для конкретного прикладу можна обійтися і без неї, але вона є стандартом при обробці вхідних даних, тому буде корисно познайомитися зі зразком її використання). Також для операції з матрицями та векторами будемо використовувати бібліотеку [numpy](https://docs.scipy.org/doc/numpy/user/quickstart.html#the-basics). В результаті отримаємо файл з таким вмістом `head data.csv`

![dataset](/old/article/e283b3547b2f32729c1be66a69650435.png)

### Трохи теорії
Нейронні мережі складаються з таких основних компонентів: вхідні дані (`X(x1, x2, ..., xn)`), вихідні дані (`y`), один або декілька прихованих шарів, [набір коефіцієнтів](https://uk.wikipedia.org/wiki/%D0%A8%D1%82%D1%83%D1%87%D0%BD%D0%B0_%D0%BD%D0%B5%D0%B9%D1%80%D0%BE%D0%BD%D0%BD%D0%B0_%D0%BC%D0%B5%D1%80%D0%B5%D0%B6%D0%B0#%D0%97'%D1%94%D0%B4%D0%BD%D0%B0%D0%BD%D0%BD%D1%8F_%D1%82%D0%B0_%D0%B2%D0%B0%D0%B3%D0%B8) між кожним з шарів (`W(w1, w2, ..., wn)`) та [функцій активації](https://uk.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D0%B2%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0_%D1%84%D1%83%D0%BD%D0%BA%D1%86%D1%96%D1%8F_%D1%88%D1%82%D1%83%D1%87%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BD%D0%B5%D0%B9%D1%80%D0%BE%D0%BD%D0%B0) для кожного прихованого шару.
Для нашого випадку найпростіша мережа буде виглядати так

![network 1](/old/article/5e375cadf53c3b6e947b950e3f8b3cee.png)

Якщо з вхідними даними, шарами та коефіцієнтами все досить просто (це звичайний вектор/матриця), то розглянути функцію активації потрібно трохи детальніше. Вона визначає залежність вхідного сигналу від вихідного (найпростішим для розуміння варіантом є [тотожна функція](https://uk.wikipedia.org/wiki/%D0%A2%D0%BE%D1%82%D0%BE%D0%B6%D0%BD%D0%B5_%D0%B2%D1%96%D0%B4%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F), яка просто повертає вхідний параметр `f(x) = x`). Але в нейронних мережах найчастіше використовується [сигмоїда](https://uk.wikipedia.org/wiki/%D0%A1%D0%B8%D0%B3%D0%BC%D0%BE%D1%97%D0%B4%D0%B0), тому ми теж скористаємося нею у нашому прикладі.

![sigmoid](/old/article/1e630fb92fef334f812c5a5593dc818f.png)

Формула для функції та відповідне представлення в коді наведено нижче

![sigmoid equation](/old/article/ef01690ed20f3fb48a27b371522d8fc4.png)

```python
import numpy as np

def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))
```

Результатом роботи цієї нейронної мережі є [звичайний добуток] (https://uk.wikipedia.org/wiki/%D0%A1%D0%BA%D0%B0%D0%BB%D1%8F%D1%80%D0%BD%D0%B8%D0%B9_%D0%B4%D0%BE%D0%B1%D1%83%D1%82%D0%BE%D0%BA) вхідного вектора, вектора коефіцієнтів (ваги) та функції активації (сигмоїда).

```python
X = np.array([0, 1, 0, 1])
weights = np.array([0, 1, 1, 1])
print(sigmoid(np.dot(X, weights)))
# 0.8807970779778823
```

Для даного вхідного значення результат близький до очікуваного (`1`), але для `[0, 0, 0, 1]` дає досить неточний результат  `0.731`. Тому далі ми опишемо логіку для коригування коефіцієнтів та [використання оновлених значень](https://uk.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%B7%D0%B2%D0%BE%D1%80%D0%BE%D1%82%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BF%D0%BE%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%BD%D1%8F_%D0%BF%D0%BE%D0%BC%D0%B8%D0%BB%D0%BA%D0%B8) на кожному наступному кроці. Зміна значень векторів (матриць) коефіцієнтів з кожною ітерацією для знаходження оптимального результату і є **процесом навчання нейронної мережі**

### Будуємо мережу
Наша мережа буде мати один прихований шар і кожна вершина буде поєднана з кожною у наступному шарі. Взагалі є [дуже багато топологій](https://towardsdatascience.com/the-mostly-complete-chart-of-neural-networks-explained-3fb6f2367464) нейронних мереж, тому якщо використовувати точну термінологію - ми будемо створювати _feed forward_ мережу([мережа прямого поширення](https://uk.wikipedia.org/wiki/%D0%9D%D0%B5%D0%B9%D1%80%D0%BE%D0%BD%D0%BD%D0%B0_%D0%BC%D0%B5%D1%80%D0%B5%D0%B6%D0%B0_%D0%BF%D1%80%D1%8F%D0%BC%D0%BE%D0%B3%D0%BE_%D0%BF%D0%BE%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%BD%D1%8F)). В початковому прикладі був використаний простий [перцептрон](https://uk.wikipedia.org/wiki/%D0%9F%D0%B5%D1%80%D1%86%D0%B5%D0%BF%D1%82%D1%80%D0%BE%D0%BD). Схематично це виглядає так

![network 2](/old/article/31908324fd0b322c9cc6c0607ebf7078.png)

Тепер додамо функцію для поширення вхідних даних, яка просто почергово перемножає шари на їх коефіцієнти (для простоти ми відкидаємо [поправку шару](https://www.quora.com/What-is-bias-in-artificial-neural-network))

```python
def _feed_forward(self):
    self.layer1 = sigmoid(np.dot(self.input, self.weights1))
    self.output = sigmoid(np.dot(self.layer1, self.weights2))
```

І найскладніша частина мережі - функція [зворотнього поширення помилки](https://uk.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%B7%D0%B2%D0%BE%D1%80%D0%BE%D1%82%D0%BD%D0%BE%D0%B3%D0%BE_%D0%BF%D0%BE%D1%88%D0%B8%D1%80%D0%B5%D0%BD%D0%BD%D1%8F_%D0%BF%D0%BE%D0%BC%D0%B8%D0%BB%D0%BA%D0%B8). Суть полягає в коригуванні значень наших коефіцієнтів

```python
self.weights1 += d_weights1
self.weights2 += d_weights2
```

А щоб знайти значення, на які потрібно відкоригувати (змістити) початкові коефіцієнти використовується [алгоритм градієнтного спуску](https://uk.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D0%B4%D1%96%D1%94%D0%BD%D1%82%D0%BD%D0%B8%D0%B9_%D1%81%D0%BF%D1%83%D1%81%D0%BA). На цьому етапі також вводиться поняття [функції втрат](https://uk.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D1%96%D1%8F_%D0%B2%D1%82%D1%80%D0%B0%D1%82) - на скільки отримані дані далекі від очікуваних. На кожному кроці ми обчислюємо функцію втрат (_loss function_), а потім поширюємо цю похибку до попередніх шарів (звідси і назва методу _зворотнього поширення помилки_). І за допомогою алгоритму градієнтного спуску намагаємося мінімізувати цю похибку.

![gradient descent](/old/article/ae716a2de5663d3e83d5500e303afb51.png)

Для простоти використовуємо в якості функції втрат [суму квадратів різниць](https://en.wikipedia.org/wiki/Residual_sum_of_squares)

![residual sum of squares](/old/article/3d5982ef82163b629ab842a4fd73f229.png)

Застосовуючи [правило диференціювання складеної функції](https://uk.wikipedia.org/wiki/%D0%94%D0%B8%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D1%96%D1%8E%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F_%D1%81%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%BE%D1%97_%D1%84%D1%83%D0%BD%D0%BA%D1%86%D1%96%D1%97) ми можемо знайти похідну функції втрат, враховуючи наші коефіцієнти

Поширення помилки в коді буде виглядати так

```python
def _back_prop(self):
    loss_derivative_value = 2 * (self.y - self.output)

    sigmoid_derivative_value = sigmoid_derivative(self.output)

    loss_1 = loss_derivative_value * sigmoid_derivative_value
    d_weights2 = np.dot(self.layer1.T, loss_1)

    loss_2 = np.dot(loss_1, self.weights2.T) * \
             sigmoid_derivative(self.layer1)
    d_weights1 = np.dot(self.input.T, loss_2)

    self.weights1 += d_weights1
    self.weights2 += d_weights2
```

Все, нейронна мережа готова, можемо почати її перевірку в роботі.

### Тренуємо мережу
Спочатку отримаємо наші вхідні дані з файлу та поділимо їх на дві частини: дані для тренування мережі та дані для перевірки точності її роботи.

```python
df = pd.read_csv('data.csv')
size = int(len(df)*0.8)
df_train = df[:size]
df_test = df[size:]
X_train = df_train[['x1', 'x2', 'x3', 'x4']].copy()
y_train = df_train.filter(['y'], axis=1)

X_test = df_test[['x1', 'x2', 'x3', 'x4']].copy()
y_test = df_test.filter(['y'], axis=1)
```

80% вхідних даних використаємо для навчання, а решту для перевірки її роботи. Додамо ще один метод , який буде повторювати процес прямого поширення та зворотнього поширення помилки задану кількість разів (ітерацій).

```python
def fit(self):
    iterations = 1000
    print('Training network...')
    for _ in range(iterations):
        self._feed_forward()
        self._back_prop()
```

Залишилося лише ініціалізувати мережу та запустити процес навчання

```python
nn = NeuralNetwork(X_train, y_train)
nn.fit()

with np.printoptions(precision=3, suppress=True):
    print(nn.output)
```

Тепер наша мережа натренована і ми можемо використовувати її на нових невідомих раніше їй даних (які відповідають формату вхідних даних). Для цього викорстаємо метод `predict`

```python
def predict(self, x):
    layer1 = sigmoid(np.dot(x, self.weights1))
    output = sigmoid(np.dot(layer1, self.weights2))
    return output
```

Він використовує уже знайдені _оптимальні_ значення коефіцієнтів для обрахування очікуваного результату. Використаємо наш тестовий набір даних для перевірки результатів роботи. Для цього виведемо обраховане значення мережею та дійсне значення для цих вхідних даних.

```python
for (row, actual) in zip(X_test.values, y_test.values):
    print(nn.predict(row), actual)
```

Очевидно, що отримані дані дуже близькі до реальних і якби ми ще додали функцію активації на зразок [двійкового кроку](https://uk.wikipedia.org/wiki/%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D1%96%D1%8F_%D0%93%D0%B5%D0%B2%D1%96%D1%81%D0%B0%D0%B9%D0%B4%D0%B0), то передбачені дані повністю б відповідали фактичним.

```
[0.04475214] [0]
[0.99837902] [1]
[0.99836759] [1]
[0.99979784] [1]
```

### Точність результатів
Отримана мережа показала гарний результат, але як впевнитися в точності її роботи? Яким кількісним показником визначити, наскільки добре вона передбачає результати для нових вхідних даних. [Найпростіший спосіб](https://uk.wikipedia.org/wiki/%D0%A2%D0%BE%D1%87%D0%BD%D1%96%D1%81%D1%82%D1%8C) - порахувати кількість правильно передбачених величин і поділити його не довжину всього тестового набору даних. Точність є одним із показників, що використовується у [матриці помилок](https://en.wikipedia.org/wiki/Confusion_matrix), яка дозволяє всесторонньо оцінити коректність роботи нейронної мережі. Взагалі існує [велика кількість метрик](https://machinelearningmastery.com/metrics-evaluate-machine-learning-algorithms-python/), що дозволяють в числовому вигляді відобразити точність мережі під час роботи з раніше невідомими даними. Зауважу, що ми можемо використати як метрику і нашу початкову функцію втрат. Але додатково розглянемо ще одну, [RMSE](https://en.wikipedia.org/wiki/Root-mean-square_deviation). Вона показує, наскільки близькими в середньому є елементи двох векторів (числа у першому та у другому масиві). Менший показник означає близькі значення обох масивів та менше значення завжди краще. За домогою методу нижче ми порахуємо дану метрику для нашої мережі

```python
def accuracy(self, X_test, y_test):
    """RMSE accuracy, lower is better"""
    predictions = self.predict(X_test)
    return np.sqrt(((predictions - y_test) ** 2).mean())
```

На цьому етапі нам знову знадобляться наші тестові дані

```python
print('Accuracy (RMSE): {:.4}'.format(nn.accuracy(X_test, y_test)['y']))
# Accuracy (RMSE): 0.02241
```

Метрики потрібні, щоб порівнювати різні типи мереж чи покращення, які ви вносите в існуючу мережу, щоб переконатися, що зміни дійсно дають кращі результати.

### Що далі?
Ми створили просту нейронну мережу, яка змогла досить точно відтворити поведінку оригінальної функції та познайомилися з базовими концептами нейронних мереж. В наступній частині ми за допомогою бібліотеки [Keras](https://keras.io/) побудуємо нейронну мережу, яка буде самостійно проходити примітивну гру. Також ознайомимося з методами для отимізації мереж, які дозволять зробити її результати кращими, ніж результати гравця-людини. На цьому все, до зустрічі!

### Ресурси

* [Повний код мережі](https://github.com/bmwant/solenie/blob/master/gwendolyn/cubec/nn.py)
* [Візуалізація мережі](https://github.com/Prodicode/ann-visualizer)
* [Різноманітні функції активації](https://www.analyticsvidhya.com/blog/2017/10/fundamentals-deep-learning-activation-functions-when-to-use-them/)
* [Пишемо нейронну мережу з нуля](https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6)
* [Працюємо з бібліотекою pandas](https://www.dataquest.io/blog/pandas-python-tutorial/)
