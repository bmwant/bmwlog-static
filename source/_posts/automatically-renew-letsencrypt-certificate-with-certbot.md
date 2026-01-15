---
title: Automatically renew letsencrypt certificate with certbot
date: 2018-06-19 10:09:38
tags: [nginx, encryption, cron, https, certificate]
author: Misha Behersky
language: en
---

Renewing your certificate is really easy with just `certbot renew` but it does expire once per 90 days, so it's a good idea to automate this process and stop worrying about your website being unavailable because of invalid certificate. We'll do that with a help of cron `crontab -e` and enter the command below

```
0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew
```

after [saving a file](https://stackoverflow.com/a/11828573/1744914) you can list your jobs to verify our new one is in place `cron -l`. Our job will run twice per day just to make sure a website runs without any interruptions even if [Let's Encrypt](https://letsencrypt.org/) has some issues on their side.

### Troubleshooting
If you have such an error

```
Cert is due for renewal, auto-renewing...
Could not choose appropriate plugin: The nginx plugin is not working; there may be problems with your existing configuration.
The error was: NoInstallationError()
```

it means that certbot cannot find nginx installation because of a cron not having same env (especially `PATH` variable) that is used to lookup the executable. Fix this slightly modifying a command

```
0 0,12 * * *  PATH="$PATH:/sbin" python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew >> /var/log/certupdate.log 2>&1
```

There are two modifications: the first one is to point to our nginx location (check whether it's the correct one with `which nginx` and the second one is to have our output in a file located within `/var/log` directory. That will allow us to figure out from logs potential future issues in case we have any.

Also if you want to understand better what the command above does mean here is a quick hint on crontab syntax

![crontab syntax](/old/article/38b6781458ce32ee95fea3439704fc3b.jpg)

### Resources
* [Introduction to cron](http://www.unixgeeks.org/security/newbie/unix/cron-1.html)
* [Certbot documentation on auto renewal](https://certbot.eff.org/docs/using.html#automated-renewals)
