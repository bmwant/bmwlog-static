---
title: Install Python 3.6 on Ubuntu 16.04 Xenial
date: 2019-01-10 08:03:43
tags: [python, python3, ubuntu, pip]
author: Misha Behersky
---

<p>By default Ubuntu is shipped with Python 3.5.2 or whatever but to use latest version (e.g. 3.6.4 as in example below) you need to install it manually. So we need to download dependencies, source code and the build it by yourself. You may execute commands from your home directory or from any other temporary directory (we need source code only once)</p>

```bash
$ sudo apt install build-essential zlib1g-dev libreadline-dev libssl-dev openssl
$ wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
$ tar -xvf Python-3.6.4.tar.xz
$ cd Python-3.6.4
$ ./configure
$ make
$ sudo -H make install
```

And that's it!

Now verify your installation with

```bash
$ pip3 --version
$ python3.6
```

<p>If you want to type <span class="inline-code">python3</span> in terminal and open a latest installation you may need to symlink your executable with the alias like this</p>

<pre>
<code class="language-bash">which python3  # output path 1
which python3.6  # output path 2
# e.g. sudo ln -sf /usr/local/bin/python3.6 /usr/local/bin/python3
sudo ln -sf  [output path 2] [output path 1]
</code></pre>

<p>Enjoy!</p>
