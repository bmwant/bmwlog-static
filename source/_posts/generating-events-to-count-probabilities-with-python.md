---
title: Generating events to count probabilities with Python
date: 2019-01-14 09:29:22
tags: [probability, game, theory, python, simulating]
author: Misha Behersky
language: en
---

In the {% post_link count-your-probabilities-using-python 'previous article' %} we have talked about confirming solution for simple probabilistic problems. What if we have slightly complex environment and we cannot calculate all the possible outcomes? We can still make a bunch of experiments and by the [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers) the average of the results will be close to expected value. As usually Python will help us generate vast amount of possible events and we will compare that result to our initial guess. Let's try to solve some examples using this approach!

### Example 1
A baseball team wins each game with probability *40%* and the games are all independent. What is the probability that they get their first win of the season in their fifth game?

**Solution**

Losing probability is [a complement probability](https://en.wikipedia.org/wiki/Complementary_event) so it's equal to *60%*. Therefore by [multiplication rule for independent events](https://en.wikipedia.org/wiki/Independence_(probability_theory)#For_events) we need to count losing 4 games in a row and then winning fifth game. `0.6*0.6*0.6*0.6*0.4 = 0.05184` which is a *5%* chance for such an outcome.

**Confirmation**

First let's define a function which will tell us whether we win a game.

```python
win_probability = 0.4

def wingame():
    return random.random() < win_probability
```

Next we introduce a concept of [Bernoulli trial](https://en.wikipedia.org/wiki/Bernoulli_trial) - it's just a random experiment with exactly two possible outcomes. Our experiment is about winning in the fifth game only.

```python
games = 5

def trial():
    for game in range(1, games+1):
        if wingame() is True:
            if game != 5:
                return False
            return True
    return False
```

Then we conduct a lot of experiments to see whether our [empirical probability](https://en.wikipedia.org/wiki/Empirical_probability) will eventually converge to correct solution.

```python
trials = [100, 10**3, 10**6]
for n in trials:
    success = 0
    for event in range(n):
        if trial() is True:
            success += 1
    print(n, success, success/n * 100)
```

_Number of events_; _success outcomes_; _probability_
* 100; 9; **9.0**
* 1000; 47; **4.7**
* 1000000; 51711; **5.1711**

To visually confirm convergence we can build a plot showing relation between probability deviation and number of events.

![plot 1](/old/article/aa10488838a831a98207033d58d09413.png)

That's exactly what we have expected, let's confirm other problems as well.

### Example 2
In a certain game of tennis, Alex has a *60%* probability to win any given point against Blake. The player who gets to 4 points first wins the game, and points cannot end in a tie. What is Alex's probability to win the game?

**Solution**

The are four different possible outcomes for Alex to win:
* Alex wins `4-0`. It's a `0.6^4` probability of winning.
* Alex wins `4-1`. Blake can win any of the 5 games except the last one. So it's a combination of 1 from 4 possible multiplied by winning 4 games and losing one.

![equation](/old/article/c831e8afc8203c19a8d90406cb3ab908.png)

* Alex wins `4-2`. The same logic applied here: we multiply combinations of 2 out of 5 by winning 4 games probability and losing 2 of them.

![equation](/old/article/04755375f8043434a9a9f695e10ec733.png)

* Alex wins `4-3`. Instead of writing the same formula I provide a generalization for arbitrary `N` (number of points to win) and `p` (probability of having a point)

![equation](/old/article/6c4b3c7bdea8342c8b50568788e4ce97.png)

Adding up all of this partial probabilities we end up with *71%* result.

**Confirmation**

Following the same approach we have

```bash
win_probability = 0.6

def wingame():
    """Whether Alex wins the game or not"""
    return random.random() < win_probability
```

and our trial

```bash
def trial():
    alex_score = 0
    blake_score = 0
    while True:
        if wingame() is True:
            alex_score += 1
        else:
            blake_score += 1

        if alex_score == 4:
            return True

        if blake_score == 4:
            return False
```

Code for repeating experiments is the same as above

```bash
trials = [100, 10**3, 10**6]
for n in trials:
    success = 0
    for event in range(n):
        if trial() is True:
            success += 1
    print(n, success, success/n * 100)
```

_Number of events_; _success outcomes_; _probability_
* 100; 73; **73.0**
* 1000; 715; **71.5**
* 1000000; 710356; **71.0356**

Chart shows the same probability as we calculated before

![plot 2](/old/article/37726f35b19938f999cecd4263b9b41f.png)

### Example 3
You and a friend take turns rolling a fair six-sided die, and the first person to roll a 6 wins. What is the probability that the person who makes the first roll wins the game?

**Solution**

Let's start by iterating on possible outcomes. Suppose you win in a first roll. Then the probability of winning is `1/6`. In order to win next time (`5/6` for losing in a first roll) you need your friend to roll something other than 6 (it's a `5/6` probability) and then to have a winning roll (which is a `1/6`).
Following the same logic we encounter infinite sum `1/6 + 5/6*5/6*1/6 + 5/6*5/6*5/6*5/6*1/6 + ... +`. We can calculate it easily using a formula for [geometric series](https://en.wikipedia.org/wiki/Geometric_progression#Infinite_geometric_series). `1/6 / (1 - 25/36) = 0.545` which is *54.5%* in result.

**Confirmation**

At this point you can try and implement a solution by yourself because everything is the same as previously

```bash
def winroll():
    return random.randint(1, 6) == 6

def trial():
    for i in count():
        if winroll() is True:
            return i % 2 == 0

trials = [100, 10**3, 10**6]
for n in trials:
    success = 0
    for event in range(n):
        if trial() is True:
            success += 1
    print(n, success, success/n * 100)
```

_Number of events_; _success outcomes_; _probability_
* 100; 52; **52.0**
* 1000; 543; **54.30**
* 1000000; 545099; **54.5099**

Additional a chart confirming convergence to the same value

![plot 3](/old/article/7eacfd0c439e3f7abadffcdcdd01fa67.png)

### Example 4
Two people, Alice and Bill, each roll a fair 20-sided die. What is the probability that Alice's roll is higher than Bill's roll?

**Solution**

For each number a player has equal `1/20` probability. It's impossible for Alice to win with `1` (it's not higher than any other number). For `2` there are one possible outcome from Bill's side which brings a victory to Alice. For `3` there are two possible outcomes and the same goes up to `20` which has 19 positive responses.
The only thing we need is to add all the probabilities together `1/20 * (1/20 + 2/20 + ... + 19/20) = 1/20 * 190/20 = 19/40 = 0.475`. To quickly calculate the sum within brackets we can use [sum of arithmetic sequence](https://en.wikipedia.org/wiki/Arithmetic_progression#Sum). This gives us *47.5%* as a result.

**Confirmation**

Code should look very familiar

```bash
def roll():
    return random.randint(1, 20)

def trial():
    # Alice's roll and Bill's roll
    return roll() > roll()

trials = [100, 10**3, 10**6]
for n in trials:
    success = 0
    for event in range(n):
        if trial() is True:
            success += 1
    print(n, success, success/n * 100)
```

_Number of events_; _success outcomes_; _probability_
* 100; 44; **44.0**
* 1000; 461; **46.1**
* 1000000; 474146; **47.4146**

Resulting plot is also behaves as expected

![plot 4](/old/article/f0222d7779e23cdebf9e35c504941536.png)

### Summary
Probabilities might be tricky but following simple principles and confirming our guesses with a code we can increase confidence for our solution and empirically verify its correctness. You can apply same technique to almost any probabilistic problem, so do not stop here and go for new adventures. See you soon.

### Resources
* [Full source code for the examples](https://github.com/bmwant/solenie/blob/master/gwendolyn/blog/lln_mc.py)
* [Building charts with Matplotlib](https://matplotlib.org/users/pyplot_tutorial.html)
