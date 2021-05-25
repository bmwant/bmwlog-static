---
title: Enhance your developing workflow with notifications on pull requests
date: 2018-05-25 09:42:08
tags: [python, github, bot, workflow, heroku]
author: Misha Behersky
---

How to make your code changes to be delivered faster? How to reduce time your pull requests being in _Needs review_ state? How to ensure developers are not blocked waiting for the feedback from their teammates? 
In this article we will write simple tool that integrates with your VCS and your messenger and answers to questions above.

### Quick overview
We will be using [Python 3](https://www.python.org/)/[aiohttp](https://aiohttp.readthedocs.io/en/stable/)/[PostgreSQL](https://www.postgresql.org/)/[Heroku](https://www.heroku.com/) and [Github](https://github.com/) as a platform for our version control system and [Slack](https://slack.com) as a messenger. In a few words the idea is the following: on each opened pull request that is ready to be reviewed developer should assign a proper label (e.g. `Needs review`) and our application will automatically send a message to a channel/room/chat with a link notifying teammates about action required from their side.

### Database setup
The only entity required for our application is the `Review`.

![erd](/img/article/93c24e29a207398cb1a2faa381695d31.png)

It allows us to implement some additional logic on top of it. Without storing this auxiliary data in our storage we would not be able to count any statistics/repeat notifications/trigger actions based on criteria (e.g. remove label from github page when we already have two approves).
Schema of our database looks like this:

```sql
CREATE TABLE IF NOT EXISTS reviews(
  id SERIAL PRIMARY KEY,
  count_value INTEGER DEFAULT 0, -- number of approves
  waiting_from TIMESTAMP NOT NULL, -- when the label was initially assigned
  issue_number INTEGER NOT NULL,  -- to track github issue number
  pr_name VARCHAR(200) NOT NULL,  -- human readable name to display
  pr_url VARCHAR(400) NOT NULL  -- link to the target pull request
);
```
The easiest way to create a PostgreSQL database for this schema is by using [docker](https://www.docker.com/). It's ok if you have already installed a database server on your host machine, just provide correct `DATABASE_URL` value in config later and skip this step.
```bash
$ docker volume create pgdata
$ docker run --name local-postgres -v pgdata:/var/lib/postgresql/data \
-d postgres
$ docker run -it --rm --link local-postgres:postgres postgres \
psql -h postgres -U postgres
postgres=# CREATE DATABASE pr_review_notifier;
postgres=# \q
$ docker run -it -v $(pwd):/opt --rm --link local-postgres:postgres postgres \
psql -h postgres -U postgres -d pr_review_notifier -f /opt/init_database.sql
```
This commands will do exactly the following:
1. Create volume to persist our database data between container restarts
2. Launch container for PostgreSQL database using our volume and officially provided docker image
3. Run `psql` script within the container and create our database through it
4. Execute initialization script on our database.

Now our database is ready and we can connect to it from python code using [aiopg](https://github.com/aio-libs/aiopg).
```python
import aiopg

async def insert_new_review(issue_number, pr_name, pr_url):
    async with aiopg.create_pool(config.DATABASE_URL, echo=True) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                date = int(time.time())
                query = (
                    'INSERT INTO reviews(waiting_from, issue_number, pr_name, '
                    'pr_url) VALUES(to_timestamp(%s), %s, %s, %s) '
                    'RETURNING id;'
                )
                await cur.execute(query, (date, issue_number, pr_name, pr_url))
                result = await cur.fetchone()
                return result[0]
```
The function above is self-sufficient (we can actually connect aiopg to our aiohttp application and reuse connection pool) and allows us to insert new rows for upcoming reviews. After inserting a record we definitely will need to retrieve it from the database. We need to implement another function but this time small [attrs](http://www.attrs.org/en/stable/) library will assist us. It allows to create objects which values can be accessed via dot notation which is very handy feature for our code. So basically we create a so-called model using this package:
```python
import attr

@attr.s
class Review(object):
    id = attr.ib()
    count_value = attr.ib()
    waiting_from = attr.ib()
    issue_number = attr.ib()
    pr_name = attr.ib()
    pr_url = attr.ib()
```
It's the representation of our database table in Python code for easier processing. And another function to retrieve review by its id (we'll be returning `Review` object defined above).
```python
async def get_review_by_id(review_id):
    async with aiopg.create_pool(config.DATABASE_URL) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = 'SELECT * FROM reviews WHERE id = %s;'
                await cur.execute(query, (review_id,))
                result = await cur.fetchone()
                if result is not None:
                    return Review(*result)
```
At this point we are ready to implement our main application which will handle all the events. In the simplest form our pipeline should look like this:

![sequence](/img/article/fcee2fb157bf32f7b64e0d73144e2844.png)

We receive a request from github [via webhooks](https://developer.github.com/webhooks/) and based on that data decide what to do next. Basically we need to register endpoint in our application
```python
def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/payload', handle_pr_event)
```
and add corresponding dispatcher for each type of the event we want to handle
```python
async def handle_pr_event(request):
    data = await request.json()

    action = data.get('action')
    if action == 'labeled':
        await _handle_labeled(data)
    elif action == 'submitted':
        # any other action you want to handle
				pass
    else:
        logger.debug(f'Unknown action {action}')

    return web.Response(text='Ok')
```
The only thing left is to register our application on Github for it to know where send our events to.

![add webhook](/img/article/f4409200af303002b88b7265905d7615.png)

Choose your repository, go to **Settings** -> **Webhooks** -> **Add webhook** and fill the form above. Right now you need to select only **Pull requests** checkbox but later you can subscribe to any event you want to handle. For **Payload URL** parameter you need to provide a callback endpoint to your application, so when developing locally you should have your server to be visible to the other machines on the Internet. Very small tool [ngrok](https://ngrok.com/) can help you with that and create a temporary tunnel to your app with a valid domain name you can share with anyone or use for testing purposes as we need right now. Another good idea is to create two webhooks: one for production and one for local development (not to edit callback url each time you switch between versions). Resulting parameter should look like `http://b491bdac.ngrok.io/payload`.


### Integration with messengers
We will cover only Slack integration here but adding another integration is as easy as subclassing from `Notifier` and implementing your own `send_message` method. Mostly all the popular messengers provide an api endpoints which you can hit with simple http request allowing to send messages. Basically the only thing you need is to get an access token that proves your application access rights. For Slack you can obtain your token [here](https://api.slack.com/tokens) and save it to the config file. And then we just send our text with additional parameters that allow to customize your resulting message (more on this [here](https://api.slack.com/docs/messages#formatting_messages)). It's  simple POST-request with aiohttp client to the [api provided by Slack](https://api.slack.com/methods/chat.postMessage).

```python
import aiohttp
import config


class Notifier(object):
    def __init__(self):
        pass

    async def send_message(self, message, *, channel: str):
        if not channel.startswith('#'):
            raise ValueError('Channel name should start with #')

        data = {
            'token': config.SLACKBOT_TOKEN,
            'text': message,
            'unfurl_links': False,
            'link_names': True,
            'channel': channel,
            'parse': 'none',
            'username': config.DEFAULT_SLACK_BOT_NAME,
            'icon_emoji': config.DEFAULT_SLACK_ICON,
        }

        url = 'https://slack.com/api/chat.postMessage'
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                result = await response.json()
                # you can additionally check the response to be sure
                # everything went smoothly
```
You can even reuse this code separately or test message sending like this:
```python
n = Notifier()
n.send_message('Hello there!', channel='#general')
```
Now let's assemble all the code together and launch and application (update our main `app.py` file):
```python
def main():
    port = int(os.environ.get('PORT', 8080))
    app = web.Application()
    setup_routes(app)
    web.run_app(app, port=port)

if __name__ == '__main__':
    main()
```
And run it with `python app.py` or `pipenv run python app.py` in case you are using [pipenv](https://docs.pipenv.org/). Feel free to inspect source code of the project (link provided at the end of article) in case you had some issues gluing all the pieces together.

### Deploying
The quickest way to deploy your application is to use Heroku platform. It's free and also provides [free postgres addon](https://www.heroku.com/postgres) to connect persistent storage.
After registering and installing Heroku-CLI we will need to do one-time initial setup to configure database and provide secret credentials to our app
```bash
$ heroku run "psql \$DATABASE_URL -f init_database.sql"
```
The command above is the same database initialization that we did before for our local postgres instance. Now set config variables for production environment via command line or do that via web interface
```bash
$ heroku config:set BASE_URL='https://<your-app-name>.herokuapp.com/'
$ heroku config:set SLACKBOT_TOKEN='<your-slackbot-token>'
$ heroku config:set GITHUB_CLIENT_ID='<your-client-id>'
$ heroku config:set GITHUB_CLIENT_SECRET='<your-client-secret>'
```
Our application is all set up and now for the deployment we just need to run `$ git push heroku master` and repeat that on each update (Heroku will automatically reinstall missing dependencies as well as restart application for you).
The only thing left is to ensure that everything works fine now and you can to that hitting `https://<your-app-name>.herokuapp.com` in your browser or by checking output from application itself with `$ heroku logs`. 
Obviously the best way to test your app is by adding a label on a pull request and getting a notification in your messenger.

![add label](/img/article/9eaee8067350358f985a559d0e47fb07.png)

![notification](/img/article/1a0960c79eda33f8a36670bcca41bf0b.png)

That's it! Come up with other ideas how to improve this code and make your workflow even better.

### Resources
* [Link to the project on Github](https://github.com/bmwant/pr-review-notifier)
* [Make nice sequence diagrams](https://www.websequencediagrams.com/)
* [How to make you local webserver visible to the rest of the world (Ukrainian)](https://bmwlog.pp.ua/post/75)