---
title: Count your probabilities using Python
date: 2019-01-02 14:30:03
tags: [python, probability, algorithm, logic]
author: Misha Behersky
---

![cubes](/old/article/ca5da93f41ce32d6a16d7752eff8265b.jpg)

Everyone familiar with probabilities knows that they can be tricky. And when solving even really simple problems an answer might be unituitive (as in famous [Linda problem](https://en.wikipedia.org/wiki/Conjunction_fallacy)). The simplest way to count your probability is by using straightforward formula `P = (number of successful outcomes) / (number of all outcomes)`. There is one issue with this approach though: we need to know the size for the space of the events in order to calculate the result. That's why there is a number of other helpful formulae allowing to make shortcut calculation. With a help of a computer we can easily generate vast amount of possible outcomes and verify that we have applied correct equation for the particular problem. In this article I'll show couple of examples that will make us sure the solution is correct for some unintuitive examples.

### Example 1
There are 10 white beads and 6 black beads in your pocket. You pull 2 of those beads out of your pocket at random, without replacement. What is the probability that both beads are the same color?

**Solution**

With a help of [combinatorics](https://en.wikipedia.org/wiki/Combinatorics) we can calculate number of possible arrangements of two beads from 16 total items.

![equation](/old/article/e90f9fb86843343287d3de8ecdae3e46.png)

`C(16 2) = 16! / (2! 14!) = 120`. Now we need to count the number of positive outcomes.

It's the same formula for white `C(10 2) = 10! / (2! 8!) = 45` and for black `C(6 2) = 6! / (2! 4!) = 15`. Using [sum rule for independent events](https://en.wikipedia.org/wiki/Rule_of_sum)

![sum rule](/old/article/5130eb7126c8302990d5c0cbaae5c13b.png)

we have `45/120 + 15/120 = 60/120 = 1/2` which is the final answer.

**Confirmation**

We'll start with generating all possible outcomes for an action. Let's represent our beads with numbers. Each unique number represents one bead and we use *even* numbers for *black* beads and *odd* numbers for *white* beads. These helper functions will tell them apart.

```python
def is_white(num):
    return num % 2

def is_black(num):
    return not is_white(num)

def same_color(num, other):
    return num % 2 == other % 2
```

Next we generate all possible outcomes (taking two beads from our initial bag) with a help of [permutation function](https://docs.python.org/3/library/itertools.html#itertools.permutations). We'll heavily rely on itertools module later, so make sure you've imported required functions to follow examples below like this

```python
from itertools import count, permutations, islice, product
```

This will help us quickly initialize input sequences in a [functional programming manner](https://docs.python.org/3/library/functional.html).

```python
black_beads = list(islice(filter(is_black, count()), 6))
white_beads = list(islice(filter(is_white, count()), 10))
beads = [*black_beads, *white_beads]
outcomes = list(permutations(beads, 2))
```

Inspecting the whole list of outcomes shows us that we have exactly the half of the pairs with matching color which is the same as calculated by a formula.

```python
successful_outcomes = list(filter(same_color_pair, outcomes))
print(len(successful_outcomes) / len(outcomes))
```

Confirmed! `0.5` is our `1/2` probability. You may notice that we have `240` outcomes in our space but `120` when calculating via equation. That's because an order doesn't matter for us, so taking `4` and then `11` is the same as taking `11` and then `4` because we consider only matching of their colors.

### Example 2
There are 5 black beads and 5 white beads in your pocket. You pull the beads out of your pocket one at a time, at random and without replacement. What is the probability that the third bead drawn from your pocket is the same color as the first?

**Solution**

In my opinion this is very unintuitive problem. After pulling first bead we have only 9 of them left in the bag. Also we have no information about second bead at all. Suppose we pulled out black bead then we still have equal probability for each of the 9 beads.  Since only 4 of them are black we have `4/9` probability of matching color. Probability wouldn't change for the white bead too as we follow the same logic.

**Confirmation**

First we define a function for comparing color of first and third bead drawn

```python
def same_first_and_third(triple):
    return same_color(triple[0], triple[2])
```

and then follow usual procedure of generating space of possible events

```python
beads = list(islice(count(), 10))
outcomes = list(permutations(beads, 3))
successful_outcomes = list(filter(same_first_and_third, outcomes))
print('{}/{}'.format(len(successful_outcomes), len(outcomes)))
```

This gives us expected `320/720 = 4/9` resulting probability.

### Example 3
You flip a fair coin 10 times. What is the probability that there are exactly 8 heads in those 10 flips?

**Solution**

For each coin we have two possible states [so there are](https://en.wikipedia.org/wiki/Combination#Number_of_k-combinations_for_all_k) `2x2x...x2` (ten times) `2^10` total states. We need to pick eight heads from these arrangements so we need to count combinations of 8 elements from 10 total

![combinations](/old/article/c94ef73e817133e198c1af9208a6f68c.png)

In our case `n=10` and `k=8`, so calculation gives us `10! / (8! 2!) = 45`. Using our base formula we can infer `45/2^10 = 45/1024` probability of having exactly 8 heads for our 10 flips.

**Confirmation**

Let `1` represent a head and `0` represent a tail. We need [to generate](https://docs.python.org/3/library/itertools.html#itertools.product) all possible arrangements of zeros and ones with a length of 10 and then count how many outcomes contain exactly 8 entires of heads. This simple function will do that for us

```python
def eight_heads(flips):
    return flips.count(1) == 8
```

As before we output the ration between successful events and number of total events

```python
outcomes = list(product([1, 0], repeat=10))
successful_outcomes = list(filter(eight_heads, outcomes))
print('{}/{}'.format(len(successful_outcomes), len(outcomes)))
```

Correct answer `45/1024` is confirmed.

### Example 4
There are 10 blue marbles and 7 red marbles in a bag. What is the probability that three marbles drawn from the bag (without replacement) are all red?

**Solution**

There are `C(17 3) = 17! / (3! 14!) = 680` possible ways to draw three marbles. There are only `C(7 3) = 7! / (3! 4!) = 35` distinct combinations for three red marbles. So our probability is `35/680 = 7/136`.

**Confirmation**

We begin by defining helper function which will tell us whether all the marbles in our sample are red.

```python
def all_red_marbles(triple):
    return triple[0] % 2 == triple[1] % 2 == triple[2] % 2 == 1
```

We will map *blue* color to *black* and *red* color to *white* not to introduce new functions and reuse existing ones.

```python
blue_marbles = list(islice(filter(is_black, count()), 10))
red_marbles = list(islice(filter(is_white, count()), 7))
marbles = [*blue_marbles, *red_marbles]
outcomes = list(permutations(marbles, 3))
successful_outcomes = list(filter(all_red_marbles, outcomes))
print('{}/{}'.format(len(successful_outcomes), len(outcomes)))
```

This gives us `210/4080` probability which is the same as ours `7/136` final result.

### Conclusion
When in doubt verify your solution with a help of a code. That will make you double think on a problem and spot any flaws in your conclusions. In the next article I will show you how similar technique to the problems where you cannot generate whole space of possible events with a help of [LLN (law of large numbers)](https://en.wikipedia.org/wiki/Law_of_large_numbers) and [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method). Leave your comments and questions below and see you soon.
