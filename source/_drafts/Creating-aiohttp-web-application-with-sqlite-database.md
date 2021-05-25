---
title: Creating aiohttp web application with SQLite database
date: 2018-03-08 07:53:10
tags: [python, asyncio, aiohttp, sqlite, web]
author: Misha Behersky
---

In this article I'm going to describe using SQLite database within your aiohttp web application. Actually, using this approach you can connect any [ODBC](https://en.wikipedia.org/wiki/Open_Database_Connectivity) compatible database. Begin with installing required dependencies ([Debian](https://en.wikipedia.org/wiki/Debian)-based system assumed)
```
$ sudo apt-get install unixodbc unixodbc-dev python-pyodbc libsqliteodbc
```

### Init your database for the first time
First of all you need to create your database file and a schema for it. Simplest way to do this is to create `*.sql` script and run it. Basic example looks like this
```
CREATE TABLE IF NOT EXISTS t1(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  number_value INTEGER DEFAULT 0,
  text_value TEXT NOT NULL
);
```

Then just run this command from a command line `sqlite3 database.db < init_database.sql` where `database.db` is the name of your database. It's more convenient to store your script in separate file but you can do that from within python code as well
```
async def test_init_database(loop=None):
    async with connect(loop=loop) as conn:
        async with conn.cursor() as cur:
            sql = 'CREATE TABLE IF NOT EXISTS t1(n INTEGER, t TEXT);'
            await cur.execute(sql)
```

### Reuse connection parameters
In case you create a connection with same parameters multiple times you can specify permanent parameters once and then save time and make a code cleaner
```
import asyncio
import aioodbc

loop = asyncio.get_event_loop()

# specify your database name here e.g. `database.db`
dsn = 'Driver=SQLite3;Database=sqlite.db' 

connect = partial(aioodbc.connect, dsn=dsn, echo=True, autocommit=True)

async with connect(loop=loop) as conn:
    pass
```

### Do not forget to commit your changes
You can control [transaction isolation levels](https://en.wikipedia.org/wiki/Isolation_(database_systems)#Isolation_levels) within connection to your database, so make sure you have enabled `autocommit` or commit your changes manually with explicit call.
Code with manual commiting
```
async def test_manual_commit(loop=None):
    async with aioodbc.connect(dsn=dsn, loop=loop) as conn:
        async with conn.cursor() as cur:
            sql = 'INSERT INTO t1(number_value, text_value) VALUES(1, "test");'
            await cur.execute(sql)
            # Make sure your changes will be actually saved into database
            await cur.commit()

    async with aioodbc.connect(dsn=dsn, loop=loop) as conn:
        async with conn.cursor() as cur:
            sql_select = 'SELECT * FROM t1;'
            await cur.execute(sql_select)
            # At this point without autocommiting you will not see
            # the data inserted above
            print(await cur.fetchone())
```
Code with autocommiting
```
async def test_auto_commit(loop=None):
    async with aioodbc.connect(dsn=dsn, autocommit=True, loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute('INSERT INTO t1(number_value, text_value) VALUES(2, "test 2");')
            # No need to call `commit` method anymore
						
    async with aioodbc.connect(dsn=dsn, loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM t1;')
            print(await cur.fetchone())
```

### Do not use string formatting when building sql queries
When you need to provide parameters to your sql query use built-in ability to parametrize a query with `?` placeholders.
```
async def test_query_placeholders():
    async with connect(loop=loop) as conn:
        async with conn.cursor() as cur:
            # Substitute sql markers with variables
            await cur.execute('INSERT INTO t1(number_value, text_value) VALUES(?, ?);',
                              ('2', 'test 2'))
            # NOTE: make sure to pass variables as tuple of strings even if
            # your data types are different to prevent
            # pyodbc.ProgrammingError errors. You can even do like this
            values = (3, 'test 3')
            await cur.execute('INSERT INTO t1(number_value, text_value) VALUES(?, ?);',
                              *map(str, values))

            # Retrieve id of last inserted row
            await cur.execute('SELECT last_insert_rowid();')
            result = await cur.fetchone()
            print(result[0])
```
But why to use placeholder instead of string formatting? Imagine this synthetic example using `sqlite3` module
```
import sqlite3

number = 42

# Malformed data provided from some bad guy
text = '"text"); DELETE FROM t1; --'

# Your query that is created using string formatting
query = 'INSERT INTO t1(n, t) VALUES({}, {})'.format(number, text)
```
and when you execute such kind of code your code/data may corrupt 
```
con = sqlite3.connect('database.db')
cur = con.cursor()
cur.executescript(query)
```
In this situation you end up with empty table and your data being lost. So remember to always sanitize/escape your code or rely on third-party libraries/code that will do this for you.

### Always use context managers
When not using context manager you may end up having unclosed connections in case any error occurred. You should handle closing connection by yourself enclosing code within `try/finally` block.
```
async def test_without_context_managers(loop=None):
    conn = await aioodbc.connect(dsn=dsn, loop=loop)
    cur = await conn.cursor()

    try:
        await cur.execute("SELECT 42 AS;")
        rows = await cur.fetchall()
        print(rows)
    except:
        pass
    finally:
        await cur.close()
        await conn.close()
```
Keep in mind these tips not only when working with this exact database/package but for every piece of your code. To see more examples visit [aioodbc examples directory](https://github.com/aio-libs/aioodbc/tree/master/examples) and for real world project check our [this repository](https://github.com/bmwant/pr-review-notifier).
See you later folks!

### Resources
* [Async Postgresql client](https://aiopg.readthedocs.io/en/stable/)
* [Async MySQL client](https://aiomysql.readthedocs.io/en/latest/)
* [Sync pyodbc client](https://github.com/mkleehammer/pyodbc/wiki)
* [SQLite3 standard module](https://docs.python.org/3/library/sqlite3.html)