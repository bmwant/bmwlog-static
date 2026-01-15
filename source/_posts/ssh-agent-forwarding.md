---
title: ssh-agent forwarding
date: 2016-03-11 11:06:24
tags: [ssh, key, vagrant, osx]
author: Misha Behersky
language: ua
archived: true
---

Інколи для доступу до приватного репозиторію на віддаленому компʼютері чи з гостьової віртуальної машини потрібно копіювати свої приватні ключі. Щоб цього не робити можна додати перенаправлення своїх ключів до потрібної нам машини. У випадку з віддаленим компʼютером додаємо це до файлу `~/.ssh/config` (створити, якщо не існує)

```
Host myhost.com
  ForwardAgent yes
```

Перевірте, що ваш ssh-агент запущений

```bash
$ echo "$SSH_AUTH_SOCK"
```

та ваш ключ видимий для нього

```bash
$ ssh-add -L
```

Якщо вашого приватного ключа немає в списку, додайте його командою `ssh-add path_to_your_key`.

Щоб після перезавантаження ключ не втрачався, додайте до скрипту завантаження вашого терміналу (`~/.bash_profile` чи аналогічний)

```bash
key_file=$HOME/.ssh/id_rsa
if [[ -z $(ssh-add -L | grep $key_file) ]]; then
    ssh-add $key_file
fi
```

Для Mac OS X замість цього можна виконати команду

```bash
$ /usr/bin/ssh-add -K path_to_your_key
```

Для Vagrant достатньо додати один рядок у `Vagrantfile`

```ruby
Vagrant.configure("2") do |config|
  ...
  config.ssh.forward_agent = true
end
```

Тепер не потрібно робити ніяких додаткових рухів з ключами, оскільки ваші локальні будуть перенаправлятися до необхідної машини.

### Ресурси

* [Гітхаб туторіал](https://developer.github.com/guides/using-ssh-agent-forwarding/)
* [Перенаправлення у Vagrant](https://coderwall.com/p/p3bj2a/cloning-from-github-in-vagrant-using-ssh-agent-forwarding)
