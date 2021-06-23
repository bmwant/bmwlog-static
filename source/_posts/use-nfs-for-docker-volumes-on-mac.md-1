---
title: Use NFS for docker volumes on Mac
tags: []
language: en
author: Misha Behersky
date: 2021-06-09 12:10:38
---


We are using docker/[docker-compose](https://docs.docker.com/compose/) as a development environment for our project and to sync the code between container and IDE [volume]() is used. Unfortunately, performance for the file-related operations on MacOS is really horrible and it's kinda a [well-known issue](https://github.com/docker/for-mac/issues/1592).

Common solution usually is to set `cached` option on a volume like this (`.` is a current working directory for the project)

```yaml
version: '3'
services:
  app:
    image: 'python:3.9-slim'
    volumes:
      - .:/var/www/html:cached
```

It gives some of improvement, but couple of commands might gain you another extra seconds while developing, so meet [NFS](https://en.wikipedia.org/wiki/Network_File_System).
### Using NFS volume instead

First of all create this file (or edit it if exists) `sudo vim /etc/exports`

```
/Users/username/workspace -alldirs -mapall=501:20 localhost
```

where `/Users/username/workspace` is a path to the directory where all of your projects reside. It allows sharing any directory within folder specified (so you might specify just a single project's dir here).

Next edit this file `sudo vim /etc/nfs.conf` to allow Docker's NFS connections by the daemon

```
nfs.server.mount.require_resv_port = 0
```

Now restart the daemon to pick up added changes

```bash
$ sudo nfsd restart
$ sudo nfsd status
```

We are ready to adjust `docker-compose.yml` file and mount volume the new way

```bash
$ cp docker-compose.yml docker-compose-nfs.yml
```

A copy of configuration is created not to conflict with your teammates who have different operating systems and this configration will be invalid for them. If you are doing this just for yourself it's probably a good idea to even add this file to `.gitignore`.

```yaml
version: '3'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - nfsmount:/var/www/html

volumes:
  nfsmount:
    driver: local
    driver_opts:
      type: nfs
      o: addr=host.docker.internal,rw,nolock,hard,nointr,nfsvers=3
      device: ":${PWD}"
```

And start your project as usually explicitly providing compose configuration via `-f` flag

```bash
$ docker-compose -f docker-compose-nfs.yml up -d
```

That's it, let's check what has been changed about performance.

### Comparison

I have selected couple of popular commands used when developing simple Django/React based web application. Those do a lot of file-related operations, so will be indicative for our tests.

* **cmd1**: `poetry run python manage.py collectstatic`
* **cmd2**: ``rm -rf `find . -name __pycache__` ``
* **cmd3**: `npm run build`
* **cmd4**: `NODE_ENV=production npm run build`

As you can see on a chart below NFS configuration clearly wins (not significantly, but noticable when frequently execute them during the day)

![chart](/images/nfsvscachecomparison.png)

So as a conclusion it's worth trying to set up NFS volume for your local dev env. You can also take a look at [docker-sync](https://docker-sync.readthedocs.io/en/latest/getting-started/installation.html#installation-osx) and [docker-bg-sync](https://github.com/cweagans/docker-bg-sync) projects to try different approaches and see what works better for you.

### Resources
* [Revisiting Docker for Mac's performance with NFS volumes](https://www.jeffgeerling.com/blog/2020/revisiting-docker-macs-performance-nfs-volumes)
