---
title: Use multiple versions of Vagrant on the same machine
date: 2018-08-14 09:22:12
tags: [vagrant, virtualbox, ruby, ubuntu, vm]
author: Misha Behersky
language: en
---

Recently I faced an issue of running Vagrant version 1.8 because of plugin [incompatibility](https://github.com/eucher/opennebula-provider). I've removed my original installation (which was 2.1)  and did the work needed. But a while after that I had to use that old version once again. So not to repeat this boring process once again I decided to make my system work with two different versions of Vagrant simultaneously. To accomplish that we need to throw away regular installation process and build everything from sources.

```bash
$ cd /opt
$ sudo mkdir vagrant-2.1.2
$ sudo chown -R `id -u`:`id -g` vagrant-2.1.2/
$ git clone https://github.com/hashicorp/vagrant.git vagrant-2.1.2/
$ cd vagrant-2.1.2
$ git checkout v2.1.2
```

Now we have Vagrant sources for version (tag) we want and we can build from this state

```bash
$ bundle install --path vendor/bundle
$ bundle --binstubs exec
```

We install Vagrant with a help of [Bundler](https://bundler.io/) and create an executable we can invoke as regular `vagrant` binary. To make our life easier and not to type absolute path to executable `/opt/vagrant-2.1.2/exec/vagrant` each time we need to symlink it.

```bash
$ sudo ln -s /opt/vagrant-2.1.2/exec/vagrant /usr/bin/vagrant2
```

And try it our in our terminal

```bash
$ which vagrant2
/usr/bin/vagrant2
```

Now we can install our second Vagrant instance, this time we can do that in a usual way

```bash
$ wget https://releases.hashicorp.com/vagrant/1.8.4/vagrant_1.8.4_x86_64.deb
$ sudo dpkg -i vagrant_1.8.4_x86_64.deb
```

The last thing to make is to change Vagrant home directory to a different place. We installed version 1.8.4 as a package and it will look at default location, so we will change that path for 2.1.2 version. The folder mentioned stores all the boxes information, plugin installed and other metadata. It's critical to separate the data between versions of Vagrant in order to make them both work properly. There is a `VAGRANT_HOME` environment variable which tells Vagrant where to look at. We can create helper script that will automatically set/unset our variable and also symlink `vagrant` alias to a proper location (not to have a mess thinking every time which `vagrant`/`vagrant2` you need to type). Create a helper script in your home directory for example

```bash
$ cd
$ touch .toggle-vagrant-version.sh
$ chmod +x .toggle-vagrant-version.sh
```

and type/copy the following content to this file

```bash
#!/usr/bin/env bash

if [ -z "${VAGRANT_HOME}" ]; then
    sudo ln -sf "/opt/vagrant-2.1.2/exec/vagrant" "/usr/bin/vagrant"
    echo "Activated Vagrant 2.1.2"
    export VAGRANT_HOME="/opt/vagrant-2.1.2/.vagrant.d"
else
    sudo ln -sf "/opt/vagrant/bin/vagrant" "/usr/bin/vagrant"
    echo "Activated Vagrant 1.8.4"
    unset VAGRANT_HOME
fi
```

Let's verify it works properly:

```bash
$ source .toggle-vagrant-version.sh
Activated Vagrant 2.1.2
$ vagrant --version
Vagrant 2.1.2
$ source .toggle-vagrant-version.sh
Activated Vagrant 1.8.4
$ vagrant --version
Vagrant 1.8.4
```

It works! You can do your daily routine without any troubles now. The other hint you can do to optimize your workflow even better is to create a shell alias to switch between versions event faster. Edit your `~/.bashrc` (depends on which shell you are running) file adding new line

```bash
alias tvag="source $HOME/.toggle-vagrant-version.sh"
```

Instead of **tvag** alias enter any short word easy for you to remember and invoke it from the shell any time you want to switch current vagrant version.

```bash
$ source ~/.bashrc
$ tvag
```

I hope now you have one less problem.

### Tips
Make sure your `VAGRANT_HOME` directory exists to eliminate any runtime errors. If you want to preserve your previous settings from original installation you can manually copy that data by yourself

```bash
$ mkdir /opt/vagrant-2.1.2/.vagrant.d
$ cp -R ~/.vagrant.d /opt/vagrant-2.1.2/.vagrant.d
```

And another tip is for VirtualBox users: to automatically install your VirtualBox Guest Additions you can use Vagrant plugin which will do that for you

```bash
$ vagrant plugin install vagrant-vbguest
```

### Resources
* [Install Vagrant from sources docs](https://www.vagrantup.com/docs/installation/source.html)
* [Question on StackOverflow](https://stackoverflow.com/questions/51824976/installing-vagrant-from-sources)
* [Question on Google Groups](https://groups.google.com/forum/#!topic/vagrant-up/rUtvwH7b0ww)
