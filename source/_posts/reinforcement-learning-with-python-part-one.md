---
title: Reinforcement learning with Python. Part 1
date: 2019-04-12 12:45:55
tags: [python, ai, reinforcement-learning]
author: Misha Behersky
language: en
---

Hi there, this is the first part on [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning) series. In this article I will try to explain some basic concepts using simple problem and in the next one we will implement a primitive algorithm to solve that in Python. Along the way we will create a complete solution for the real world problem using reinforcement learning techniques. Let's get started!

### Journey begins
Suppose we want to travel from Los Angeles to Last Vegas. We have a car with a tank's volume of 60L. Along the road we have 10 gas stations which are located equally far from each other. Our driver is **_an agent_** - someone who makes decisions of what to do. He has a plenty of **_actions_** to choose from. For example at each gas station we are able to fill a tank with 10, 20, 30, 40, 50 or 60 (full tank) liters of fuel as long as there is available free volume within it. Moreover we can travel 10, 20, 30, 40, 50 or 60 km as long as there is available fuel in a tank (for simplicity sake assume 1L per km consumption). Our driver might get tired so we have one extra idle action - just staying at a gas station not moving anywhere and not replenishing a tank (probably just having some coffee). In total we have 7 actions available - that's our **_action space_**. As you can see we have **_discrete action space_**. In other words we cannot move 15 or 21.5 kilometers - just stick with predefined values above. There are algorithms that works with **_continuous action space_** and we will have an eye on them later too. Let's have small pause and check out the car we'll be driving for the next couple of articles.

![bmw m2](/old/article/ce1b15f22fde33c29e501d3e4383c6f0.png)

_* this should be Tesla Model 3 but it doesn't have a gas tank_


During our trip we will go through different cities (gas stations). That's our **_environment_** - a tiny *world* where our agent learns and acts. We are able to visit each of those and we can describe ourselves as being in a city with a tank filled by some amount. That's when the notion of a **_state_** comes in. State is a representation of current environment and most of the time we are only able to partially experience it's internals by our **_observation_**. For this simple example those are indistinguishable, so let's not dive too deep and think about it as of information we can retrieve at any time during the trip. In our case we can describe it as a `(city, tank volume)` pair and represent as a table.

![state 0](/old/article/2f9df7abd7cb31e5a190a981c631df5d.png)

We always start our trip from LA having an empty tank. That corresponds to `(0, 0)` cell in a table. Our trip ends in a last row (we may end up having some extra fuel in a tank when reaching destination point). Each column in a table corresponds to a current amount of fuel we have. Each row corresponds to a city we are currently passing through. We can represent our **_state space_** (all possible states agent can be in) with a simple 70-items list and each state can be represented as a number `0-69`. From the state given we can easily figure out which city we are in and how much fuel do we have at the moment. Let's demonstrate that with a code

```python
from typing import Tuple


CITIES_NUM = 10
TANK_STATES_NUM = 7


def from_state(state: int) -> Tuple[int, int]:
    city_num = state // TANK_STATES_NUM
    tank_volume = (state % TANK_STATES_NUM) * 10

    assert 0 <= city_num < CITIES_NUM
    assert 0 <= tank_volume < TANK_STATES_NUM * 10
    return city_num, tank_volume


def to_state(city_num: int, tank_volume: int) -> int:
    assert tank_volume % 10 == 0
    assert city_num >= 0

    if city_num < CITIES_NUM:
        return city_num*TANK_STATES_NUM + tank_volume // 10
```

We have two helper functions which will convert our state to `(city, tank volume)` pair and back. Check that output of these functions corresponds to cells in our table. Being in a first yellow city with a full tank should give us `13` as a state

```python
>>> to_state(1, 60)
13
```

And being in state `64` means we have reached Las Vegas and still have 10L left.

```python
>>> from_state(64)
(9, 10)
```

Our agent can learn only by interacting with the environment. In order to do that we have to drive not only once but a **a lot** of times the same route from LA to Sin City. Each trip might be totally different from previous one (driver may stop at different gas stations or may rest more than usual) and it's called an **_episode_**. Each episode begins from starting state (`0` in our case) and ends in special **_terminal state_** (when we have reached Las Vegas). But how do we learn during an episode?

### Rewards
We begin by defining all the actions available to the agent. As usually they are easily represented by a simple list of integers.

```python
ACTIONS = [
    -60,  # drive 60 km
    -50,
    -40,
    -30,
    -20,
    -10,  # drive 10 km
      0,  # nothing useful
     10,  # fill tank with 10L
     20,
     30,
     40,
     50,
     60,  # fill tank with 60L of a fuel
]
```

The idea of the reinforcement learning is that some actions are better than others in certain states. Agent should learn how to behave optimally (in the best way possible) in each state in order to maximize its reward. It gets positive rewards when doing right/good actions and negative rewards when doing something wrong (bad actions). At each time step agent receives a **_reward_** from the environment for an action being performed. Total amount of rewards collected through an episode is called a **_return_** and the goal of an agent is to maximize the return. That's why it's important to properly define rewarding mechanism as it will be an intrinsic motivator for the agent to do right things.

In our environment an agent will receive negative reward of `-1` at each time step. That's reward equivalent of saying *go from one place to another in shortest time*. Without such a punishment our agent might decide to just stuck in one city drinking coffee and having some fun. When reaching the destination point it will get a positive reward of `+20`.

What should driver do in order to get maximal total reward? Intuitively we understand that we need to spend less time on gas stations and more time driving (e.g. always filling the whole tank and moving until it's empty). But how does driver know what to do in a certain situation? The answer is by following a certain **_policy_**. In simple words policy is a mapping between states and actions. Think of it as a driver's handbook/guide showing what to do in a city when you have read tank's indicators. We can achieve our main goal of maximizing return by finding such a policy that will dictate best actions for any given state (kinda cheatsheet for our simple game). Let's assume that we've got such a handbook from another driver that drives this route from time to time. How do we know this guide is good and whether it's good enough for us?

### Policy evaluation
In case we have existing policy we could do a **_rollout_**, just an episode for the policy given. Agent will follow recommendations from the policy and will get some return in the end. We need to implement `step` function and call it again and again until the end of episode.

```python
class Environment(object):
    def __init__(self):
        self._state = None
        self._max_steps = 20
        self.reset()

    def reset(self):
        self._state = 0
```

In the code above you can see `_max_steps` variable introduced. That was done to add a constraint on the episode length. If agent will stuck in some city doing nothing we won't wait forever and hope something changes. This limitation will allow an episode to eventually terminate even if the agent did not reach the termination state by himself. Also you might notice `reset` method which sets the environment to its initial state. As I mentioned before we will need to run a dozen of episodes and therefore we need to make sure that we do not start from the middle of the route at the beginning of a rollout.

The main method is implemented below and follows our logic of `-1`/`+20` rewards. It makes some manipulations with an action value in order to get proper new state. Note that we are not doing any extra sanity check here and assuming that action passed is valid.

```python
def step(self, action: int) -> Tuple[int, int]:
    city_num, tank_volume = from_state(self._state)
    tank_volume += action

    if action < 0:
        city_num += abs(action) // 10  # moving forward
    new_state = to_state(city_num, tank_volume)

    reward = -1
    if city_num == CITIES_NUM-1:  # we have reached it
        reward = 10
        new_state = None
    return reward, new_state
```

From this point we are ready for the whole trip at the end of which we will receive total "points" collected.

```python
def rollout(self, policy):
    self.reset()
    cumulative_reward = 0
    for i in range(self._max_steps):
        action = policy[self._state]
        reward, new_state = self.step(action)
        cumulative_reward += reward
        self._state = new_state
        if self._state is None:
            break

    return cumulative_reward
```

At each step we are asking an agent for its decision (an action produced by the policy) and receiving a reward and a next state from the environment. We do that until episode terminates by reaching the destination or exceeding our steps constraint.

We can measure the results of the rollout and a result produced by another policy and in such way compare them. A good place to start here is always by providing some baseline for the return (some relative value we can compare later to). A **_random policy_** is usually used for that. Basically in each state driver will make its decisions by throwing a dice roll ({% post_link count-your-probabilities-using-python '[1]' %} {% post_link generating-events-to-count-probabilities-with-python '[2]' %}) and choosing an action based on that. Here's an implementation for the random policy.

```python
MAX_TANK_VOLUME = 60

class RandomPolicy(object):
    def action(self, observation):
        city_num, tank_volume = from_state(observation)
        available_actions = list(range(
            -tank_volume,
            MAX_TANK_VOLUME-tank_volume+1,
            10,
        ))
        return random.choice(available_actions)
```

As you already might have noticed some actions are not available in some states. For example we cannot go from state `0` to state `7` as we don't have a fuel for that. We still can act with any of 0-60 though. To handle this issue policy should pick only an action which is available (based on observation). Environment on the other side should either give some large negative reward or simply not change its state (in our example we already have `-1` reward for each time step, so that will do a job). After evaluating our policy we can compare that to random one and if it's better we can set it as our new baseline and continue a process of finding the best one. Suppose that driver has been told to fill a tank with 10L in each city and then go to the next city (i. e. visit each city). We can write that as a code like this

```python
class SuggestedPolicy(object):
    def action(self, observation):
        # state and observation are the same in our example
        city_num, tank_volume = from_state(observation)
        if not tank_volume:
            return 10  # get 10L of fuel
        if tank_volume == 10:
            return -10  # go to the next city
        return 0  # do not know what to do, so just waiting
```

You can think of it as of the big dictionary (as I mentioned policy is just a mapping) which looks like the following (when being in the first column in our table we fill a tank and for the second column we move by 10km)

```python
policy = {
    # fill a tank
    0: 10,
    7: 10,
    14: 10,
    21: 10,
    ...
    63: 10,
    # move to another city once we have a fuel
    1: -10,
    8: -10,
    15: -10,
    ...
    57: -10,
    # do nothing in any other state
    2: 0,
    3: 0,
    4: 0,
    ...
    55: 0,
}
```

To make our policy support indexing as a dictionary we need to add one magic method

```python
def __getitem__(self, observation):
    return self.action(observation)
```

Now we are ready to evaluate our both policies and see which one shows better results

```python
def evaluate(policy, num_episodes=1) -> float:
    env = Environment()
    total_reward = 0
    for i in range(num_episodes):
        reward = env.rollout(policy)
        total_reward += reward
    avg_reward = total_reward / num_episodes
    print('Average reward is: {:.2f}'.format(avg_reward))
    return total_reward / num_episodes
```

As you can see we have extra `num_episodes` parameter. This one is needed for a valid evaluation. Due to randomness involved in our `RandomPolicy` we might obtain totally different results within different runs, so we just average those to have a better picture. On the other hand `SuggestedPolicy` will always produce the same result no matter how many episodes are played. We call such a policy a **_deterministic_** one because it gives the same output for a given state every time. **_Stochastic_** policy is an opposite one and it returns an action for the state based on some [distribution](https://en.wikipedia.org/wiki/Normal_distribution) (e.g. half of a time doing one action and half of a time another one). Below the result for the evaluation is presented (you may have different value for a random policy)

```python
>>> random_policy = RandomPolicy()
>>> evaluate(random_policy, 10)
0.9

>>> suggested_policy = SuggestedPolicy()
>>> evaluate(suggested_policy)
3.0
```

Now we know that following our colleague's handbook we can do a better job that spontaneously selecting an action every time. Let's have another trip with random policy and visualize it to better understand what's going on.

![random rollout](/old/article/6b4ce371fc463483aa38390b7dbdf8ba.webp)

As you can see this time random policy produced even better result and that means we are still far from ideal. `t` parameter on the right represents our current time step (remember we have a constraint of 20 time steps); `s` corresponds to a current state and `s'` is our new state after performing action `a` and receiving reward `r` for it. Only on step with index `7` we receive a positive reward for accomplishing a goal and `-1` for any other step. Note that on step `6` agent decided to stay in _light green_ city wasting time and therefore just obtaining a negative reward for that.

When comparing sequences of cells on the table produced by a policy we might see them creating some kind of a path. We call that path **_trajectory_** and usually it's represented by a list of `(s, a, r, s')` tuples.

![trajectories for both policies](/old/article/43a96a2c19323a5ba4c8ba89cdbc757a.png)

In our case better policy will lead to shorter trajectory, so we'll reach our destination faster.

That's pretty much it! We've managed to finish our trip and now we know at the end of it whether our route was good or bad based on a reward feedback provided.

### Summary
In this article we have described main terminology in reinforcement learning domain. I hope that was easy to grasp because of simple example and analogies given. In the next article we will talk about value function, action-value function, value iteration and policy iteration.
Let me know in the comments how this post can be improved and what topic you want to read about in next RL-related posts. See you soon.

### Resources
* [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)
* [An introduction to RL on FreeCodeCamp](https://medium.freecodecamp.org/an-introduction-to-reinforcement-learning-4339519de419)
* [Great intro from OpenAI](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)
* [RL courses by David Silver (from DeepMind)](http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html)
