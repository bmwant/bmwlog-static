---
title: Writing custom remote commands for Celery workers
date: 2019-03-01 19:30:06
tags: [celery, python, flower, monitoring, aws, django]
author: Misha Behersky
language: en
---

There are [a lot of celery commands](http://docs.celeryproject.org/en/latest/userguide/monitoring.html#commands) allowing you to monitor task/worker statuses. It's really easy to extend that list with your custom command and we'll do that in order to get some extra monitoring for any task launched. I suppose that you already have [Flower](https://flower.readthedocs.io/en/latest/) configured and running and it runs on each of your workers hosted on [AWS](https://aws.amazon.com/). You can definitely update the code below according to your needs and make it work for your case as well. So what we are trying to accomplish: we want to be able go to the Flower UI task tracking page right away after triggering task execution. For that we will implement a custom worker control command which will respond with its IP address (assuming dynamic infrastructure, so you cannot just hardcode it within config/inventory file). In order to retrieve instance's IP address we will use [instance metadata endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html#instancedata-data-retrieval). This url `http://169.254.169.254/latest/meta-data/public-ipv4` allows us to retrieve external IP address of an instance from which this request is being executed. Wrapping this up as a custom command function

```python
import requests
from celery.worker.control import inspect_command

@inspect_command()
def get_worker_ip(state):
    hostname = socket.gethostname()
    # check dev environment
    if hostname == 'your-dev-machine-hostname':
        public_ip = '127.0.0.1'
    else:
        r = requests.get(settings.AWS_PUBLIC_IP_METADATA_URL)
        public_ip = r.text
    return {'ip': public_ip}
```

The only helper function we need then is the one which will generate a url for the status page. First we [broadcast our custom command](http://docs.celeryproject.org/en/latest/reference/celery.app.control.html#celery.app.control.Control.broadcast) to first worker we found active and based on its response we format a url template with proper IP address and task ID.

```python
def get_task_result_url(task_id):
    url_template = 'http://{creds}{ip_address}:5555/task/{task_id}'
    inspect = queue.control.inspect()
    active_workers = inspect.active()
    if not active_workers:  # we need at least one worker running
        logger.error('No worker is running at the moment')
        return
    # any worker would work, assuming at least one is running
    worker = list(active_workers.keys())[0]
    response = queue.control.broadcast('get_worker_ip', destination=[worker], reply=True)
    worker_ip = response[0][worker]['ip']

    creds = ''
    user = settings.CELERY_FLOWER_AUTH_USER
    password = settings.CELERY_FLOWER_AUTH_PASSWORD
    if user and password:
        creds = '{}:{}@'.format(user, password)

    return url_template.format(creds=creds, ip_address=worker_ip, task_id=task_id)
```

Note that this code works even with [Flower Basic Auth](https://flower.readthedocs.io/en/latest/auth.html#http-basic-authentication) being enabled. Just make sure you store this credentials within local config/environment variable.

Now let's see usage of this in an example

```python
>>> from tasks import my_task
>>> result = my_task.delay()
>>> url = get_task_result_id(result.id)
>>> url
'http://54.222.133.88:5555/task/2584a7ff-9eaf-4a8a-9ef1-8818202dd355'
```

**NOTE**: Chrome and other browsers [dropped support](https://www.chromestatus.com/feature/5669008342777856) for embedded credentials in URIs to comply with [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt), so pasting URL in your address bar will not automatically log you in (in case you are using basic auth), but you can easily embed this url into a template and allow users to click on that with seamless login.

### Update for Django users
If you are using [Django framework](https://www.djangoproject.com/) you often trigger background tasks on some user actions. It's pretty convenient to provide a link for monitoring task status back to them via [flash message](https://docs.djangoproject.com/en/dev/ref/contrib/messages/). You can do it easily like this

```python
from django.contrib import messages
from django.utils.safestring import mark_safe

from tasks import my_task, get_task_result_url

result = my_task.delay()
task_url = get_task_result_url(task_id=result.id)
message = 'Track your task <a href={} target="_blank">here</a>'.format(task_url)
messages.success(makr_safe(message))
```

That's it for today, have a great weekend and see you soon.

### Resources
* [Official docs on writing custom commands](http://docs.celeryproject.org/en/latest/userguide/workers.html#writing-your-own-remote-control-commands)
* [Monitoring Celery queue with Datadog](https://bmwlog.pp.ua/monitoring-celery-queue-with-datadog)
* [Writing custom routing for Celery](https://bmwlog.pp.ua/custom-celery-routing)
