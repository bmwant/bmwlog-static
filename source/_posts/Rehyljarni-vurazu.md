---
title: Регулярні вирази #1
date: 2016-09-29 12:28:43
tags: [compilers, regex, python, algorithms]
author: Misha Behersky
---

<p>Невеличка стаття на примітивно-базовому рівні про те, як працюють регулярні вирази. Я хотів би написати серію про створення власного транслятора і це може бути одним із таких постів. Тут я хочу написати коротку програму, яка буде перевіряти вхідний рядок на відповідність нашому заданому регулярному виразу.</p>

<p><a href="https://en.wikipedia.org/wiki/Regular_expression" target="_blank">Регулярний вираз</a> - це <a href="https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Grammars" target="_blank">граматика</a>, що задає <a href="https://en.wikipedia.org/wiki/Programming_language" target="_blank">мову</a>. Простіше кажучи, це група&nbsp;правил, записаних&nbsp;у вигляді набору символів, що визначає, якого вигляду конструкції може містити певна задана мова.</p>

<p>Щоб написати програму, що буде розбирати регулярний вираз, потрібно розуміти поняття <a href="https://en.wikipedia.org/wiki/Deterministic_finite_automaton" target="_blank">автомату</a>.</p>

<p><em>Автомат </em>- це сутність, що визначається такими поняттями:</p>

<p><strong>M = (Q, T, q0, d, F)</strong></p>

<p><strong>Q </strong>- множина всіх станів автомата.</p>

<p><strong>T</strong> - множина вхідних символів.</p>

<p><strong>q0</strong> - початковий стан (входить в множину Q).</p>

<p><strong>d</strong> - функція переходів автомата.</p>

<p><strong>F</strong> - &nbsp;множина кінцевих станів автомата (підмножина Q).</p>

<p>Побудуємо автомат, що буде розбирати регулярний вираз <strong>E = (+ | - | e) d d*</strong>.</p>

<p><strong>E</strong> (expression)&nbsp;- регулярний вираз.</p>

<p><strong>e</strong> (empty) - порожній рядок.</p>

<p><strong>d</strong> (digit) - <a href="https://en.wikipedia.org/wiki/Arabic_numerals" target="_blank">цифра</a>.</p>

<p><strong>| </strong>(вертикальна риска, <a href="https://en.wikipedia.org/wiki/Pipeline_(Unix)" target="_blank">pipe</a>) - операція &quot;<a href="https://en.wikipedia.org/wiki/Logical_disjunction" target="_blank">або</a>&quot;. Повинен бути присутній хоча б один символ з перелічених.</p>

<p><strong>* </strong>- символ може повторюватися довільну кількість разів (від нуля до нескінченності).</p>

<p>Потрібно виділити всі можливі стани і відповідні переходи до них. Найпростіше це подати графічно:</p>

<p><img alt="" src="/img/article/c4c8180017a431128d0048a492c96bf7.png" style="height:436px; width:851px" /></p>

<p><strong>S</strong> (start) - це початковий стан, <strong>F </strong>(finish) - кінцевий. З початкового стану ми можемо прочитати символи додавання, віднімання чи нічого (порожній символ) і перейти в стан <strong>B </strong>зчитування цифри. В стані&nbsp;<strong>C</strong> у нас уже є гарантовано одна цифра і ми переходимо безумовно (по порожньому символу) в стан&nbsp;<strong>D</strong>. В ньому ми можемо крутитися в циклі доти, доки зустрічаємо цифру або ж одразу перейти в кінцевий стан&nbsp;<strong>F</strong>. Тепер ми знаємо всі можливі умови і переходи, які можна записати кодом:</p>

<pre>
<code class="language-python">class InvalidInput(ValueError):
    pass


def match_string(text):

    def read_char():
        yield from text

    cursor = read_char()
    try:
        ch = next(cursor)

        if ch == '+' or ch == '-':
            ch = next(cursor)

        if ch.isdigit():
            while True:
                try:
                    ch = next(cursor)
                except StopIteration:
                    break
                if not ch.isdigit():
                    raise InvalidInput('Number should contain only digits')

        else:
            raise InvalidInput('Number should start with a digit')
            
    except StopIteration:
        raise InvalidInput('Unexpected end of input')</code></pre>

<p>Все що тут відбувається - це посимвольне зчитування вхідних даних і перевірка на відповідність поточного символа очікуваному стану. Якщо символ не відповідає стану - отримаємо помилку вхідних даних InvalidInput. Даною програмою тепер можна перевіряти рядки на відповідність нашому регулярному виразу. Так всередині влаштовані багато інструментів розбору регулярок.</p>

<p>Але коли регулярка стає складнішою, а вхідний текст довшим - хочеться мати змогу швидко знайти місце помилки в разі невірних вхідних даних. Таку функціональність ми спробуємо додати до нашого аналізатору.</p>

<p>Створимо клас</p>

<pre>
<code class="language-python">class Matcher(object):
    def __init__(self, text):
        self.pos = 0
        self.text = text</code></pre>

<p>що буде зберігати позицію останнього зчитаного символу. Також додамо два методи для отримання наступного символу і відображення помилки</p>

<pre>
<code class="language-python">def read(self):
    for pos, char in enumerate(self.text):
        self.pos = pos
        yield char

def error(self, message):
    term.writeLine('Error at position {pos}: {message}'.format(
        pos=self.pos, message=message), term.red)
    term.writeLine(self.text)
    term.write('-'*self.pos, term.yellow)
    term.write('^\n', term.yellow)
    raise InvalidInput(message)
</code></pre>

<p>І сам метод <strong>match</strong>&nbsp;майже без модифікацій</p>

<pre>
<code class="language-python">def match(self):
    cursor = self.read()
    try:
        ch = next(cursor)

        if ch == '+' or ch == '-':
            ch = next(cursor)

        if ch.isdigit():
            while True:
                try:
                    ch = next(cursor)
                except StopIteration:
                    break
                if not ch.isdigit():
                    self.error('Number should contain only digits')

        else:
            self.error('Number should start with a digit')
            
    except StopIteration:
        self.error('Unexpected end of input')</code></pre>

<p>Тепер коли виникне помилка - ми побачимо інформативне повідомлення з вказанням місця в рядку, де вона була виявлена.</p>

<p><img alt="" src="/img/article/d595c82b4cd23deb810300af1c01594c.png" /></p>

<h3>Ресурси</h3>

<p><a href="http://bmwlog.pp.ua/post/106" target="_blank">Бібліотека для кольорового прінту в консолі</a></p>

<p><a href="http://regexr.com" target="_blank">Погратися з регулярними виразами онлайн</a></p>

<p><a href="http://sketchtoy.com" target="_blank">Де малювати такі недолугі картинки</a></p>

<p><a href="https://gist.github.com/bmwant/f9c3dbd5d2c69dd1f7cc7f1551a5ff4b" target="_blank">Код на Гітхабі</a></p>

<p>&nbsp;</p>