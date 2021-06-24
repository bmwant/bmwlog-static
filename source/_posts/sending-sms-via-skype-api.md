---
title: Sending sms via Skype api
date: 2016-12-08 19:02:18
tags: [python, skype, api, fun]
author: Misha Behersky
language: en
---

Recently I faced a problem of sending sms to a number that was not completely known: I had three missing digits. Like you know somebody can leave his number in such way: `+380986*581**`. I found that Skype provides [developer tools for building a bot](https://docs.botframework.com/en-us/skype/getting-started), but failed to implement anything probably because it was too late at night. So results in google showed that there is another library that can attach to running process of skype - [Skype4Py](https://github.com/Skype4Py/Skype4Py). Simple script came up after couple of minutes

```python
# -*- coding: utf-8 -*-
import time
import Skype4Py
import click


def main():
    skype = Skype4Py.Skype()
    skype.Attach()
    number_template = '+3809865{}81{}{}'
    for i in range(0, 1000):
        i1 = i // 100
        i2 = i  // 10 % 10
        i3 = i % 10
        phone = number_template.format(i1, i2, i3)
        click.secho('Sending {} sms to {}...'.format(i, phone), fg='blue')
        text = 'Wanna say something {} time...'.format(i)

        sms = skype.SendSms(phone, Body=text)
        time.sleep(0.5)

    click.secho('Finished', fg='green')


if __name__ == '__main__':
    main()
```

We need this additional timeout between sending messages, so Skype will have enough time to process message queue that is growing very fast. Also you can accomplish this brute forcing of all possible numbers by using `product` method from `itertools`.

```python
from itertools import product

for i1, i2, i3 in product(range(10), range(10), range(10)):
    print(i1, i2, i3)
```

### Note

On MacOS X because of 32-bit issue you may encounter segmentation fault error. To avoid this just append this to a command while launching script

```bash
$ arch -i386 python sms_sender.py
```

The saddest thing is that you have to use Python 2.7 and 3 is not supported.

![skype logo](/old/article/294de1445dc53518aae9c1a404e0a92e.png)

And as not all of your numbers will be valid ones that are currently maintained by a provider you might get dozens of messages about failed delivery. For 1K numbers I had something about 150 effective numbers. And of course you will be charged for sending those messages! I believe there is also an ability to check programmatically whether message delivery failed, but it was not a point for me at that moment. And as always - you are able to create some cool stuff, so do not hesitate to use your brain.

![console logs](/old/article/07f37a4a1082341ea92ae45d33e5e4d0.png)

### Resources

* [Python 2 itertools module](https://docs.python.org/2/library/itertools.html#itertools.product)
