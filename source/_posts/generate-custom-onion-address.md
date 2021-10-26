---
title: Generate custom onion address
date: 2018-02-17 18:21:55
tags: [tor, security, hacking, privacy, deepweb]
author: Misha Behersky
language: en
---

When creating a hidden tor service you might see resulting address looks like a mess of letters. There is an algorithm used to generate such an address:

* Public/private key pair is generated
* Public key got hashed with [SHA-1](https://en.wikipedia.org/wiki/SHA-1) algorithm
* First 80 bits of the output are encoded with [Base32](https://en.wikipedia.org/wiki/Base32)
* The result is the hostname of your onion service

So, to have your own customized address you need to generate bunch of keys and check whether they fit your requirements. For bruteforcing purposes we'll be using [eschalot](https://github.com/ReclaimYourPrivacy/eschalot) tool. Let's download and use it immediately

```bash
$ sudo apt install build-essential libssl-dev
# or whatever package os/package manager you use
$ git clone https://github.com/ReclaimYourPrivacy/eschalot.git
$ cd eschalot/
$ make
$ ./eschalot -vp name -t 8 > results.txt
```

Now we are looking for address with prefix `name` and using 8 threads we'll output results in `results.txt` file. When process eventually complete (the longer prefix the longer a search) you can copy private key to the folder of yor service (e.g. `/var/lib/tor/hidden_service/private_key`) and restart tor.

```bash
# or whatever service manager you use
$ systemctl restart tor.service
```

With such a tool you can search by prefixes/suffixes or even regular expressions but keep in mind that for entries longer than 6 characters it may take a lot of time (days and exponentially growing to years and more).

### Resources

* [StackOverflow discussion](https://security.stackexchange.com/questions/29772/how-do-you-get-a-specific-onion-address-for-your-hidden-service)
* [Shallot tool for generating custom names](https://github.com/katmagic/Shallot)
* [Scalion tool for generating custom names](https://github.com/lachesis/scallion)
