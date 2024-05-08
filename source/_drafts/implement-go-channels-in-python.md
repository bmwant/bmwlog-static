---
title: Implement Go channels in Python
tags: [python, go, asyncio, concurrency, channels]
author: Misha Behersky
language: en
date: 2023-03-05 21:26:55
---


Go language is well known for its native support

and handly methods of communicating and synchronizing built into the language.

Python is a [multi-paradigm language](https://en.wikipedia.org/wiki/Programming_paradigm#Support_for_multiple_paradigms) on its own and also shines when writing concurrent code with [asyncio](https://docs.python.org/3/library/asyncio.html)
In this article we will implement Go channel in Python to provide as similar experience to writing concurrent code in Python as you would using Go.

### Requirements

* Supports arrow notation for [sending and receiving](https://go.dev/ref/spec#Channel_types) over the channel
* Supports [`range` and `close`](https://go.dev/tour/concurrency/4)
* Supports [buffering](https://nanxiao.gitbooks.io/golang-101-hacks/content/posts/unbuffered-and-buffered-channels.html)

### Go approach
Let's now look at the classical [producer-consumer](https://www.cs.cornell.edu/courses/cs3110/2010fa/lectures/lec18.html) example which is often [used to showcase](https://gobyexample.com/closing-channels) synchronization using `exit`/`done` channel.

```go
package main

import (
	"time"
	"log"
)

func main() {
	ch := make(chan int, 2)
	exit := make(chan struct{})

	producer := func() {
		for i := 0; i < 5; i++ {
			log.Println("Sending", i)
			ch <- i
			log.Println("Sent", i)

			time.Sleep(1 * time.Second)
		}

		log.Println("Finished producing")

		close(ch)
	}

	consumer := func() {
		for v := range ch {
			log.Println("Received", v)
		}
		log.Println("Finished consuming")
		close(exit)
	}

	go producer()
	go consumer()

	log.Println("Waiting for everything to complete")
	<-exit
	log.Println("All done, exiting!")
}
```


### Let's write some Python

Due to language limitation some

```python

```



```python
from typing import Any

class Value:
    def __init__(self, value: Any = None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
```

In order to be able to receive values from channel using `value << channel` syntax we need to implmenent `__lshift__` method on the `Value` class.

```python
async def __lshift__(self, channel: Channel):
    new_value = await channel.get()
    self.value = new_value
```

Now let's check both sending and receiving data to a channel

```python
ch = Channel()
v = Value()

# Sending values to a channel
ch << 23
ch << "this is a string"

# Receiving values from channel
v << ch
print(f"v holds '{v}' value")
v << ch
print(f"v now holds '{v}' value")
```

When running this code *as-is* you will get the error below

```console
RuntimeWarning: coroutine 'Channel.__lshift__' was never awaited
RuntimeWarning: coroutine 'Value.__lshift__' was never awaited
```

That's the limitation we've talked about as we have to explicitly run the coroutine using `await`, so exact syntax is not possible to achieve. To make everything work update the lines as here

```python
await (ch << 23)
await (ch << "this is a string")

await (v << ch)
await (v << ch)
```

Finally, the output looks like expected, so we can move forward and implement more complex logic.

```console
v holds '23' value
v now holds 'this is a string' value
```

### Put everything together


```python
async def main():
    ch = Channel(size=2)
    exit = Channel()
    _ = Value()

    async def producer():
        for i in range(5):
            logging.info(f"Sending {i}")
            await (ch << i)
            logging.info(f"Sent {i}")
            await asyncio.sleep(1)

        logging.info("Finished producing")
        Close(ch)

    async def consumer():
        async for i in Range(ch):
            logging.info(f"Received {i}")

        logging.info("Finished consuming")
        Close(exit)

    go(producer())
    go(consumer())

    logging.info("Waiting for everything to complete")
    await (_ << exit)
    logging.info("All done, exiting!")


if __name__ == "__main__":
    asyncio.run(main())
```

As you can see the code is almost identical and visually undoubtedly similar to the Go variant (*wrt* syntax differences). There is also a minor change to the logging configuration (to make output look similar) and adding of the `go` alias for [create_task](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task) function to schedule an execution of a coroutine.

```python
import asyncio
import logging

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(message)s",
  datefmt="%Y/%m/%d %H:%M:%S",
)

# Launch coroutines with `go` syntax
go = asyncio.create_task
```

Here's an output produced when running the program

![python output](/images/python_channel.png)

### Resouces

* [Complete source code](https://github.com/bmwant/jaaam/tree/main/channel)
