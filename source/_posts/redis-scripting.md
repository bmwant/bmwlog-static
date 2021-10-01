---
title: Redis scripting
tags: []
language: en
author: Misha Behersky
date: 2021-10-01 13:39:25
---


Redis has built in Lua interpreter allowing to evaluate scripts in the context of Redis server. I want to show you a couple of examples where this scripting feature might be helpful.
So imagine the following scenario (**use case #1**):
* you have decided to introduce [TTL](https://en.wikipedia.org/wiki/Time_to_live) to you records for optimization reasons. There is no default TTL in Redis, so keys are set to live forever. This might clog your memory resulting in frequent [evictions](https://redis.io/topics/lru-cache) affecting the performance. Therefore it's much more preferable to expire your items earlier and keep overall memory usage about *70-80%* level.
* you cannot [delete all the data](https://redis.io/commands/FLUSHALL) at once as your application relies on that. Needless to say you have already created same keys with *ttl* attribute set on them. The only issue you have right now is to delete old records without expiration date.

Normally you would go over all [keys](https://redis.io/commands/KEYS) within database, [check their ttl](https://redis.io/commands/ttl) value and [remove keys](https://redis.io/commands/del) without expiration one by one.

```bash
REDIS_ENDPOINT="redis-cache.abcde1.ng.0001.use1.cache.amazonaws.com"
KEYS=$(redis-cli -h "$REDIS_ENDPOINT" keys '*')

for k in $KEYS; do
  TTL=$(redis-cli -h "$REDIS_ENDPOINT" ttl "$k")
  if [[ $TTL -ne -1 ]]; then
    echo "."
    redis-cli -h "$REDIS_ENDPOINT" del "$k"
  fi
done
```

Make sure you have `redis-cli` executable installed before running the script

```bash
$ apt update && apt install -y redis-tools
$ ./delete_without_expiration.sh  # save the content above into the file
```

This shell script would do the jobs, but it has some major drawbacks:
* `keys` operation is blocking and is not recommended to be used on production environments
> It may ruin performance when it is executed against large databases
* for each key it requires at least one extra connection to be made (for the *ttl* check) and then one more in case deletion is required;
* this script is not *atomic*: it might need to be relaunched in case some network flakiness occurs;
* this is *horribly slow*: it will not perform well on any database with more than 1 million keys (which is not even a big number for any application heavily relying on the cache).

Let's rewrite these steps to the native Lua script

```lua
local pattern = '*'
for _, k in ipairs(redis.call('keys', pattern)) do
  local ttl = redis.call('ttl', k)
  if (ttl == -1) then
    redis.call('del', k)
  end
end
```

Although the algorithm is identical it will not suffer from extra network delays as it is ran directly by the engine itself. To be fair the latter solution is bettern in case you are running hosted Redis solution such as [AWS Elasticache](https://aws.amazon.com/elasticache/) otherwise network delays will not be noticable as you can run the script on the same machine where the Redis resides.

To trigger the script execute the command below

```bash
$ export REDIS_ENDPOINT="redis-cache.abcde1.ng.0001.use1.cache.amazonaws.com"
$ redis-cli -h "$REDIS_ENDPOINT" --eval delete_without_expiration.lua
```

Moving forward to the next example (**use case #2**) consider the following scenario:
* you need to downscale instance size in order to save costs (obviously you have collected all the metrics needed, monitored the usage over certain period of time and concluded it would not impact performance or any other critical APM metric);
* you cannot remove all the records at once, scale back down and then re-populate the cache with new items as it would disrupt application running causing possible downtime.

Normally you would do

```bash
$ export REDIS_ENDPOINT="redis-cache.abcde1.ng.0001.use1.cache.amazonaws.com"
$ redis-cli -h "$REDIS_ENDPOINT" flushall
$ redis-cli -h "$REDIS_ENDPOINT" flushall async  # to run in non-blocking manner
```

With our custom script we will be able to delete only subset of keys. Moreover we are going to introduce two new features: to be able to provide keys pattern as a [command line argument](https://redis.io/commands/eval) and to return total number of deleted items.

```lua
local counter = 0
local pattern = ARGV[1]
for c, k in ipairs(redis.call('keys', pattern)) do
  redis.call('del', k)
  counter = c
end
return counter
```

This is really useful when you know exactly the underlying naming for the most of your keys, meaning you can safely drop them provinding the known prefix/pattern. As a result total number of affected records will be printed back to the console.

```bash
$ redis-cli -h "$REDIS_ENDPOINT" --eval delete_keys.lua , ':1:f*'  # note comma in the middle
$ redis-cli -h "$REDIS_ENDPOINT" --eval delete_keys.lua , ':1:pattern*only'
```

> **NOTE**: make sure to insert comma in the command above as it serves as a delimiter between *KEYS* and *ARGV* and we are using only the latter within our script

Below you can see a chart of four subsequent invocations using different patterns that we've applied to the our database before downscaling procedure.

![items count](/images/redis_items.png)

This script helped us to drop half of the items in cache allowing to migrate to the twice as small instance size as the original one.

### Resources

* [Guide to Redis Lua scripting](https://www.compose.com/articles/a-quick-guide-to-redis-lua-scripting/)
* [Advanced Redis scripting with Lua](https://redis.com/ebook/part-3-next-steps/chapter-11-scripting-redis-with-lua/)
