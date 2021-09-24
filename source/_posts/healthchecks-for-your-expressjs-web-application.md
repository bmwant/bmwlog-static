---
title: Healthchecks for your Express.js web application
date: 2018-03-12 09:42:33
tags: [healthcheck, expressjs, nodejs, javascript, monitoring]
author: Misha Behersky
language: en
---

In this article I want to describe easy way to set up a healthcheck for your application using amazing service [healthchecks.io](https://healthchecks.io). First lets understand what healthcheck is. It's a periodical ping of your application expecting some successful response. When answer is not received within some safe interval or within couple of retries your service assumed to be dead and a notification or an alert is sent. There are two types of healthchecks:
1. **To your service**. Your application implements an `/healthcheck` or `/status` endpoint which respond with `200` status when everything is in operational state.
2. **From your service**. Your application sends request to third-party endpoint notifying that it is alive and working.

To set up first type of healthcheck you might do something like this

```bash
$ npm i express-healthcheck --save
```

and then add endpoint to your routes

```javascript
app.use('/healthcheck', require('express-healthcheck')({
    healthy: function () {
        return { everything: 'is ok' };
    }
}));
```

After configuring your side just connect some third party service from the [list of available](https://www.hongkiat.com/blog/monitor-website-up-downtime-30-free-web-services-and-tools/) and you are good to go.

But we will focus on the second approach as it's the one that healthchecks.io implements. Add your first healthcheck in UI

![add healtcheck](/old/article/199370e0dbe732b3a3bee487c5049077.png)

and then add this code inserting url that was generated on previous step

```javascript
var   https = require('https');

function sendHealthcheck() {
  console.debug('Sending healthcheck...');
  https.get('https://hchk.io/<your-unique-id-here>');
}

setInterval(sendHealthcheck, 10 * 60 * 1000); // every ten minutes
```

Next thing you need is to configure your intervals. **Period** is expected time between pings and **grace time** is a delay before alert is sent in case ping was not received.

![set timers](/old/article/52e3652a57a63bb6bad100f54f93c99f.png)

It's really simple and the only thing left is to configure preferred way to receive your alerts. There are a lot of available integrations such as [Slack](https://slack.com), [Telegram](https://telegram.org/), [Pushover](https://pushover.net/), [Pushbullet](https://www.pushbullet.com/) and others. By default it will send notifications to your email and in some cases that might be enough.

Using this service will help you monitor availability of your web sites and quickly repair them before users will get frustrated. Ten minutes of your time now may save you from headache in future.

Stay in touch.
