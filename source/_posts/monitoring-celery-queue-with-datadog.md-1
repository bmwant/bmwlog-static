---
title: Monitoring Celery queue with Datadog
date: 2019-12-23 17:02:50
tags: [devops, celery, monitoring, ansible, datadog]
author: Misha Behersky
language: en
---

![queue graphs](/old/article/1614ef4e1efa3faa912a721cdb81c90c.png)

Sometimes your Celery workers are having hard time processing all the tasks from a queue. It might be due to your tasks being _long running_ or due to a high load on workers themselves. Obviously you need to consider [autoscaling](http://docs.celeryproject.org/en/latest/reference/celery.bin.worker.html#cmdoption-celery-worker-autoscale) in order to handle this issue but in a first place you need to know is something going wrong. For this purpose we will setup monitoring with [Datadog platform](https://www.datadoghq.com/). The easiest way to know when your queue is getting bigger is by restricting your workers of fetching more than one task at once (set [prefetch limit](http://docs.celeryproject.org/en/latest/userguide/optimizing.html#prefetch-limits) to 1: pass `--prefetch-multiplier=1` when launching your worker). This way tasks would be hanging in a queue if no worker is able to process it and therefore it will be easy to monitor queue size.

I'm assuming that you have already [installed datadog agent](https://docs.datadoghq.com/agent/?tab=agentv6) and you are using [Redis](https://redis.io/) as [a broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html). Celery will create a list for your queue with a key named after your queue name (default one is `celery` in case you do not have an [extra routing](http://docs.celeryproject.org/en/latest/userguide/routing.html#changing-the-name-of-the-default-queue)). The only thing you need to do is to create a file with content

```yaml
init_config:

instances:
  - host: "your.redis.host.com"
    port: "6379"

    keys:
      - celery
```

and place it at the `/etc/datadog-agent/conf.d/redisdb.d/conf.yaml` destination. Now restart agent and verify check was discovered and works properly

```bash
$ sudo service datadog-agent restart  # restart agent
$ sudo datadog-agent status
$ sudo datadog-agent status | grep redis  # verify redis check config was loaded
$ sudo datadog-agent check redisdb  # send check to Datadog manually
```

Now go to you Datadog dashboard and add new timeseries chart for `redis.key.length` metric.

![adding a chart](/old/article/b58a0fc5130331648151793e01689563.png)

Specify error/warning thresholds according to number of workers available. Ideally queue size should not grow at all, so do not set this value higher than `20`. Finally you should set up a [monitor](https://docs.datadoghq.com/monitors/) for the same metric and send notifications to email/messengers when queue is bigger than it should be.

### Update for Ansible users
In case you need to add monitoring to multiple instances and you are using [Ansible](https://docs.ansible.com/ansible/latest/index.html) to provision your infrastructure you can add just one task that will automate all the thing for the process above.

```yaml
---

- tasks:
  - name: install check for redis
    template:
      src: dd_redis_conf.yaml.j2
      dest: /etc/datadog-agent/conf.d/redisdb.d/conf.yaml
      owner: "dd-agent"
      group: "dd-agent"
    notify:
      - restart datadog-agent

- handlers:
  - name: restart datadog-agent
    service:
      name: "datadog-agent"
      state: restarted
    become: yes
```

Now you can feel a bit relaxed and think about optimizing/refactoring your tasks and scaling infrastructure for workers. Do not forget to add other tools for Celery monitoring such as [Flower](https://flower.readthedocs.io/en/latest/)!

### Resources
* [Ansible role for installing Datadog agent](https://github.com/DataDog/ansible-datadog)
* [Submitting other custom metrics with Python](https://gist.github.com/conorbranagan/87307c4376f64895f54c)
