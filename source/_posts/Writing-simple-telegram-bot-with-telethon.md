---
title: Writing simple Telegram bot with Telethon
date: 2019-12-23 14:09:00
tags: [python, telegram, bot, api]
author: Misha Behersky
language: en
---

In this article I will quickly create a showcase of using [Telethon Python library](https://docs.telethon.dev/en/latest/) in order to make a simple [Telegram](https://telegram.org/) bot. Our bot will be a member of a group/channel and once someone changes group's description bot will post that about information as a separate message.

### Preparation
We need a couple of things in order to get started
1. Register a new bot with a help of [BotFather](https://core.telegram.org/bots#6-botfather)
2. Create new API application to obtain `APP_ID` and `APP_HASH` variables. Follow [the steps here](https://docs.telethon.dev/en/latest/basic/signing-in.html)
![registering an app](/old/article/e5d53b14217b3ba28d50cd0263835238.png)
3. Install Telethon library. Both regular `pip install telethon` and modern `poetry add telethon` will work.
4. Make sure you are familiar with [asyncio](https://docs.python.org/3/library/asyncio.html) and [how asynchronous programming works](https://realpython.com/async-io-python/) in Python.

### Handling the right event
We can listen to any event that happens in a chat. For example when a title/description has been changed we will receive [ChatAction event](https://docs.telethon.dev/en/latest/quick-references/events-reference.html#chataction). In the example below we will listen to any incoming message in the group responding with an updated description. First we need to create a bot instance


```python
from telethon.sync import TelegramClient

# make sure you have defined api_id, api_has, bot_token somewhere in the code
bot = TelegramClient('bot', API_ID,  API_HASH).start(bot_token=BOT_TOKEN)
```

Once done we need to create a handler responsible of dealing with the specific kind of the events

```python
from telethon.sync import events

@bot.on(events.NewMessage)
async def any_message_arrived_handler(event):
    print('We are handling message events')
```

Now let's run execution loop and add the bot to any test group we already have

```python
bot.run_until_disconnected()
```

You will see logging in your console after any new message arrives into the channel.

### Implementing the logic
The one most important thing left is to implement the main application logic

```python
from telethon import functions

DESC = ''

async def any_message_arrived_handler(event):
    global DESC
    chat = await event.get_chat()
    result = await bot(functions.messages.GetFullChatRequest(
        chat_id=chat.id
    ))
    description = result.full_chat.about
    if description != DESC:
        DESC = description
        await bot.send_message(
            chat.id, f'Description has been changed to **{description}**')
```

As you can see we store current topic in a global variable, so once process restarts we would loose latest topic. You can use [Sqlite](https://docs.python.org/3.9/library/sqlite3.html) to have a simple persistent storage or just write it to the file. The only trick here is to obtain [ChatFull](https://tl.telethon.dev/constructors/chat_full.html) instance otherwise we will not be able to get the description.

That's it, now you are able to enhance it with any custom features you want. Happy coding!

### Resources
* [Complete project on the Github](https://github.com/bmwant/tabtab)
* [Related StackOverflow question](https://stackoverflow.com/questions/48432287/how-to-get-telegrams-channel-description-in-telethon)
* [Use Poetry in your project](https://bmwlog.pp.ua/post/using-poetry-in-production)
