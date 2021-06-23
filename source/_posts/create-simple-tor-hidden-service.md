---
title: Create simple Tor hidden service
date: 2017-12-14 13:43:37
tags: [security, tor, hacking, centos]
author: Misha Behersky
language: en
---

In this article I want to share how simple it is to create a service in Onion web (Tor network). We will create simple web page that would be accessible via Tor browser. I will show the example for CentOS 7 (RHEL).

Make sure that your have configured your server as a webserver (nginx is assumed).

Next install tor package

```bash
$ yum install epel-release
$ yum install tor
```

and configure it `cp /usr/share/tor/defaults-torrc /etc/tor/torrc`

Now edit config that was copied and make sure lines below are uncommented

```
RunAsDaemon 1

DataDirectory /var/lib/tor

HiddenServiceDir /var/lib/tor/my_hidden_site
HiddenServicePort 80 127.0.0.1:8333
```

Skip all the lines intented for **relays** and modify only the one for **location-hidden services**

Now update nginx configuration to point to your hidden resource `vim /etc/nginx/conf.d/my_hidden_site.conf`

Paste sample configuration in that file

```nginx
server {
    listen       8333 default_server;
    listen       [::]:8333 default_server;
    server_name  _;
    root         /usr/local/my_hidden_site;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Make sure you have created same sample html page at `/usr/local/my_hidden_site` directory

```html
<html>
  <head>
    <title>My hidden service</title>
  </head>
  <body>
    <h1>Hey there from Tor!</h1>
  </body>
</html>
```

Now just restart nginx and tor services for changes to take effect

```bash
$ nginx -t && nginx -s reload
$ systemctl restart tor.service
```

Check content of `/var/lib/tor/my_hidden_service/hostname`, open Tor browser and point it to the url generated. That's it.

### Notes

This is simplified tutorial assuming that you have SELinux disabled. To check current status and disable it if not yet execute following

```bash
$ sestatus
$ setenforce 0
```

The other issue that might prevent tor service from start is permissions on directories. So make sure that you have proper access rights on folder `/var/lib/tor/my_hidden_service` (or any other folder that you've specified)

```bash
$ sudo chmod -R toranon:toranon /var/lib/tor/my_hidden_service
```

### Resources

* [Install nginx on CentOS 7](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7)
* [How to deal with SELinux](https://wiki.centos.org/HowTos/SELinux)
