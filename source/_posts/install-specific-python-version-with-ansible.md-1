---
title: Install specific Python version with Ansible
date: 2018-05-22 11:02:16
tags: [python, ansible, devops, ubuntu, playbook]
author: Misha Behersky
language: en
---

Really quick tutorial of how to install a custom Python version from source code with a help of Ansible.  The resulting playbook will help us to install python in automatic mode on any remote machine as well as on virtual machine within [Vagrant](https://www.vagrantup.com/). So the code of Ansible playbook first followed with a little bit of explanation

```yaml
---

- name: Install required packages
  apt: name={{item}} state=installed
  with_items:
    - build-essential
    - libssl-dev
    - libreadline-dev
    - openssl
  become: true

- name: Download archive with python
  get_url:
    url: "https://www.python.org/ftp/python/{{ python_version }}/Python-{{ python_version }}.tgz"
    dest: "/tmp/python.tgz"
    force: yes

- name: Extract python archive
  unarchive:
    src: "/tmp/python.tgz"
    dest: "/opt"
    copy: no

- name: Build python from source code
  shell: |
    ./configure && \
     make && \
     make install
  args:
    chdir: "/opt/Python-{{ python_version }}"
  become: true
```

First we install packages that are required to compile/build Python properly, then download and extract source code from official ftp and finally build it from sources with a help of a `make` tool.
Optionally, you can add a check for current python version to save your time if running a playbook often enough

```yaml
- name: Check which python version is installed
  shell: "python3 --version"
  register: python_output
  ignore_errors: true
```

After that just wrap the task above in a `block` section with `when` condition or do the similar with `inlude`.

```yaml
- name: Install specific version of Python
  include: "python.yml"
  when: python_output.stdout != "Python {{ python_version }}"
```

And yes, you can make it as a separate role or include directly into the `tasks` section within your playbook. In case of using Vagrant you need to update your `Vagrantfile` if haven't done it yet.

```
  config.vm.provision :ansible do |ansible|
    ansible.playbook = "ansible/provision.yml"
    ansible.config_file = "ansible/ansible.cfg"
  end
```

Do not forget to specify required python version in your `vars.yml` and you'll be good to go. Next time invoking a playbook on a remote or running provisioning on your vm (`vagrant provision`) you will get Python installed and ready to use.

### Other approaches
You can try to install python with a help of apt-get using [package archives provided by deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa). There is [an ansible module](http://docs.ansible.com/ansible/latest/modules/apt_module.html) allowing you to write tasks corresponding to commands below

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.5
```

This PPA contains most recent Python versions for each minor release so it will not fit your needs in case you should have specific _patch_ version on your system. (X.Y.Z - _x_ - **major**, _y_ - **minor**, _z_ - **patch**).

Next option is to use [pyenv](https://github.com/pyenv/pyenv) and allow it to install required distribution for you

```bash
$ pyenv install 3.5.2
```

That's it! Stick with preferred solution and don't forget to reuse the approach writing ansible playbook for that.

### Resources
* [Install Python 3.6 on Ubuntu Xenial manually](https://bmwlog.pp.ua/post/123)
* [Install Python 3.5 on Ubuntu manually](https://bmwlog.pp.ua/post/90)
