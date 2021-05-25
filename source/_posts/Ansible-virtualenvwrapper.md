---
title: Ansible + virtualenvwrapper
date: 2017-04-12 15:49:06
tags: [ansible, virtualenv, python, pip]
author: Misha Behersky
---

<p><a href="https://virtualenvwrapper.readthedocs.io/en/latest/" target="_blank">virtualenvwrapper</a> is a very convenient tool to use. It provides easier access to all the regular features you like in virtualenv.</p>

<p>But when it comes to automation with Ansible some issues might occur. You cannot just call workon venv&nbsp;within one task and then continue to work in the same context from another task. There are two options how to overcome this issue.</p>

<h3>Call python executable directly from environment directory</h3>

<p>In this case you need two extra variables: one for project&#39;s root and the other for the path to virtual environment</p>

<pre>
<code>- name: Install requirements
  shell: "{{ virtualenv_path }}/bin/pip install -r requirements.txt"
  args:
    chdir: "{{ root_directory }}"</code></pre>

<p>The same way you can call your python binary <span class="inline-code">{{ virtualenv_path }}/bin/python</span></p>

<h3>Explicitly modify environment</h3>

<p>Just modify PATH environment variable for the task and it will pick the right one python for you</p>

<pre>
<code>- name: Call script within proper environment
  shell: "python main.py"
  environment:
    PATH: "{{ virtualenv_path }}/bin:{{ ansible_env.PATH }}"
  args:
    chdir: "{{ root_directory }}"</code></pre>

<h3>Notes</h3>

<p>Consider using <a href="http://docs.ansible.com/ansible/pip_module.html" target="_blank">built-in pip module</a> for Ansible but in case you want to stick with virtualenvwrapper use one of the approaches above.</p>