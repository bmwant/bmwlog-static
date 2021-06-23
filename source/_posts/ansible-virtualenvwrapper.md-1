---
title: Ansible + virtualenvwrapper
date: 2017-04-12 15:49:06
tags: [ansible, virtualenv, python, pip]
author: Misha Behersky
language: en
---

[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) is a very convenient tool to use. It provides easier access to all the regular features you like in virtualenv.

But when it comes to automation with Ansible some issues might occur. You cannot just call `workon venv` within one task and then continue to work in the same context from another task. There are two options how to overcome this issue.

### Call python executable directly from environment directory

In this case you need two extra variables: one for project&#39;s root and the other for the path to virtual environment

```yaml
- name: Install requirements
  shell: "{{ virtualenv_path }}/bin/pip install -r requirements.txt"
  args:
    chdir: "{{ root_directory }}"
```

The same way you can call your python binary `{{ virtualenv_path }}/bin/python`

### Explicitly modify environment

Just modify `PATH` environment variable for the task and it will pick the right one python for you

```yaml
- name: Call script within proper environment
  shell: "python main.py"
  environment:
    PATH: "{{ virtualenv_path }}/bin:{{ ansible_env.PATH }}"
  args:
    chdir: "{{ root_directory }}"
```

### Notes

Consider using [built-in pip module](http://docs.ansible.com/ansible/pip_module.html) for Ansible but in case you want to stick with virtualenvwrapper use one of the approaches above.
