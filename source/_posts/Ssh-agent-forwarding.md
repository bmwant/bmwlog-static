---
title: ssh-agent forwarding
date: 2016-03-11 11:06:24
tags: [ssh, key, vagrant, osx]
author: Misha Behersky
---

<p>Інколи для доступу до приватного репозиторію на віддаленому компʼютері чи з гостьової віртуальної машини потрібно копіювати свої приватні ключі. Щоб цього не робити можна додати перенаправлення своїх ключів до потрібної нам машини. У випадку з віддаленим компʼютером додаємо це до файлу <strong>~/.ssh/config </strong>(створити, якщо не існує)</p>

<pre>
<code>Host 
  ForwardAgent yes</code></pre>

<p>Перевірте, що ваш ssh-агент запущений</p>

<pre>
<code>echo "$SSH_AUTH_SOCK"</code></pre>

<p>та ваш ключ видимий для нього</p>

<pre>
<code>ssh-add -L</code></pre>

<p>Якщо вашого приватного ключа немає в списку, додайте його командою <strong>ssh-add path_to_your_key</strong>.</p>

<p>Щоб після перезавантаження ключ не втрачався, додайте до скрипту завантаження вашого терміналу (<strong>~/.bash_profile</strong>&nbsp;чи аналогічний)</p>

<pre>
<code class="language-bash">key_file=$HOME/.ssh/id_rsa
if [[ -z $(ssh-add -L | grep $key_file) ]]; then
    ssh-add $key_file
fi</code></pre>

<p>Для Mac OS X замість цього можна виконати команду</p>

<pre>
<code>/usr/bin/ssh-add -K path_to_your_key</code></pre>

<p>Для Vagrant достатньо додати один рядок у <strong>Vagrantfile</strong></p>

<pre>
<code>Vagrant.configure("2") do |config|
  ...
  config.ssh.forward_agent = true
end</code></pre>

<p>Тепер не потрібно робити ніяких додаткових рухів з ключами, оскільки ваші локальні будуть перенаправлятися до необхідної машини.</p>

<h3>Ресурси</h3>

<p><a href="https://developer.github.com/guides/using-ssh-agent-forwarding/" target="_blank">Гітхаб туторіал</a></p>

<p><a href="https://coderwall.com/p/p3bj2a/cloning-from-github-in-vagrant-using-ssh-agent-forwarding" target="_blank">Перенаправлення у Vagrant</a></p>