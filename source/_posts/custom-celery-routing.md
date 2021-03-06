---
title: Custom Celery routing
date: 2019-03-01 19:29:24
tags: [celery, docker, python, redis, ci]
author: Misha Behersky
language: en
---

In this article I'm going to share an approach that we use to execute some long running background tasks for our project.

So I use [Celery](http://www.celeryproject.org) as a task executor with a [Redis](https://redis.io) broker backend. I have couple of different environments for my workers so each of those runs within docker container. We want to support hot reloading too. For example we have our environment changed and that would require building new images and running workers within this new environment. At the same time we want currently running processes to finish without any interruptions and new task submitted to be picked up by new workers.

### Current implementation

Right now I have following pipeline

* On each requirements change of dockerfiles change we trigger new jenkins build that will create images with new environment
* Tag for the image is created dynamically based on a hash sum from from requirements
* On each deploy (we use [Ansible](http://docs.ansible.com/ansible/index.html) for that) we render docker-compose files with corresponding image tags
* At this point we have our workers running with the new envrionment

![architecture diagram](/old/article/8d400e33fa2b3e0fb30a953e84a39c3e.png)

So, what's left? We need to gracefully kill all previous workers and dynamically route new tasks to new workers. But first things first.

### How to get a tag

```python
import glob
import hashlib

from pip.req import parse_requirements


def get_requirements(filename):
    """
    Gets requirements from a file ignoring comments and extra data.
    """
    return [str(r.req) for r in parse_requirements(filename, session='')]


def get_requirements_hash(requirements):
    hasher = hashlib.sha256()
    hasher.update(requirements)
    return hasher.hexdigest()


def get_current_project_requirements():
    """
    Returns all requirements for the project as a string each
    requirement per new line.
    """
    project_requirements = []
    for filename in sorted(glob.glob('requirements/*.txt')):
        project_requirements.extend(get_requirements(filename))

    return '\n'.join(project_requirements)


def get_current_image_tag():
    """
    Based on hash of all the requirements files return a tag
    for latest docker images.
    """
    all_reqs = get_current_project_requirements()
    image_tag = get_requirements_hash(all_reqs)
    return image_tag
```

In this example we get all the `*.txt` files in requirements directory but it can be any text file as long as `get_current_project_requirements` will be consistent about its results (notice `sorted` function to make sure that we will always have same order for the lines therefore the same hash for identical requirements).

Our custom router needs to implement `route_for_task` method which will tell based on parameters provided the right queue we need. There is a safe callback that would be redirecting to latest queue in case no active queue for the current version was found. You can actually omit this and just fail with an error at this point.

```python
class VersionRouter(object):
    def __init__(self, current_tag, exchange=None):
        self.tag = current_tag
        self.exchange = exchange or Exchange('default', type='direct')

    def route_for_task(self, task, args=None, kwargs=None):
        print('args passed: {}'.format(args))
        print('kwargs passed: {}'.format(kwargs))

        version = kwargs.get('version', '')

        if version.startswith('v1'):
            queue_version = 'q1'
        elif version.startswith('v2'):
            queue_version = 'q2'
        elif version.startswith('vN'):
            queue_version = 'qN'
        else:
            raise RuntimeError('Unsupported version {}'.format(version))

        queue_name = '{queue_version}-{current_tag}'.format(
            queue_version=queue_version,
            current_tag=self.tag,
        )
        return self._route_to_active_queue_or_latest(queue_name)

    def _route_to_active_queue_or_latest(self, queue_name):
        return self._create_version_route(queue_name) \
            if self._version_has_active_queue(queue_name) \
            else self._create_version_route(self.latest_queue_name)

    def _version_has_active_queue(self, queue_name):
        return queue_name in [q['name']
                              for queues in self._get_active_queues().values()
                              for q in queues]

    def _get_active_queues(self):
        return self.celery.control.inspect().active_queues()

    @property
    def latest_queue_name(self):
        return 'latest-{}'.format(self.tag)

    @staticmethod
    def _create_version_route(queue_name):
        return {
            'exchange': self.exchange,
            'queue': queue_name,
            'routing_key': queue_name
        }
```

Now we need to tell Celery how to use this router, so we will update its configuration

```python
current_tag = get_current_image_tag()
router = VersionRouter(current_tag=current_tag)
celery_config = {
    'CELERY_DEFAULT_EXCHANGE': 'default',
    'CELERY_DEFAULT_ROUTING_KEY': router.latest_queue_name,
    'CELERY_DEFAULT_QUEUE': router.latest_queue_name,
    'CELERY_QUEUES': (
        Queue('default', default_exchange, routing_key='default'),
        Queue('latest', mbtest_exchange, routing_key='latest'),
        Queue('3p0', mbtest_exchange, routing_key='3p0'),
        Queue('2p9', mbtest_exchange, routing_key='2p9'),
        Queue('2p8', mbtest_exchange, routing_key='2p8'),
    ),
    'CELERY_ROUTES': (router,),
}

celery_app = Celery('celery_tasks', config_source=celery_config)
```

Here's an example of dictionary-based config but you can provide your configuration in the usual way you used to.

Now on deploys we need to stop consuming tasks on queues with previous tags allowing them to finish in orphaned containers. I invoke ansible task with following python script for that.

```python
from celery_tasks import celery_app
from utils import get_current_image_tag


def stop_consuming():
    consumers = ('v1', 'v2', 'vN', 'latest')
    current_tag = get_current_image_tag()
    for consumer in consumers:
        consumer_queue = '{}-{}'.format(consumer, current_tag)
        print('Stopping workers from listening on queue {}'.format(consumer_queue))
        celery_app.control.cancel_consumer(consumer_queue)
```

And then we just launch docker compose with a compose file created from such a template

```yaml
workerv1:
  image: {{ worker_v1_image_name }}:{{ current_image_tag }}
  command: |
    celery worker
    --app "celery_tasks"
    --queues "v1-{{ current_image_tag }}"
    --hostname "v1"

workervN:
  image: {{ worker_vN_image_name }}:{{ current_image_tag }}
  command: |
    celery worker
    --app "celery_tasks"
    --queues "vN-{{ current_image_tag }}"
    --hostname "vN"
```

### Final thoughts

This approach works fine for us but we still have all the workers running on the same node with a broker itself. In order to scale this solution I suggest using RabbitMQ as a broker and distribute workers across multiples nodes (e.g. by the version), hopefully Ansible also allows to use multiple hosts. The only issue we have is some delay needed to build new images in order to launch integration tests with new images but anyway it's worth it.

### Resources

* [docker-compose reference](https://docs.docker.com/compose/compose-file/#build)
* [Jenkins plugin for triggering a job on push](https://wiki.jenkins-ci.org/display/JENKINS/GitHub+Plugin)
* [Celery Flower to monitor queues and tasks](http://flower.readthedocs.io/en/latest/)
* [Celery and RabbitMQ](http://suzannewang.com/celery-rabbitmq-tutorial/)
* [Portainer to monitor running containers](http://portainer.io/overview.html)
