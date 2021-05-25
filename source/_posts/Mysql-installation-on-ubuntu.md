---
title: MySQL installation on Ubuntu 18.04
date: 2019-01-22 12:36:27
tags: [ubuntu, mysql, database, server, sql]
author: Misha Behersky
---

Basic installation is an easy process and requires typing just a couple of commands

```
$ sudo apt update
$ sudo apt install mysql-server
$ sudo mysql_secure_installation
```

Answer the questions provided and your basic installation is finished. Now you need to make sure your can access your database with _username_/_password_ pair. 

```
$ sudo mysql
```

This will take you in MySQL prompt where you need to set a password for the `root` user with commands provided below

```
mysql> SELECT user,authentication_string,plugin,host FROM mysql.user;
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

**NOTE:** Make sure to replace _password_ with your own secure password.

Exit a shell

```
mysql> FLUSH PRIVILEGES;
mysql> exit
```

and check you are able to connect with a password created

```
$ mysql -u root -p
```

Let's create a database so we can connect to it with a help of any client and use it within our applications

```
mysql> CREATE DATABASE [database-name];
mysql> exit
```

### Backup and restore your database
Now suppose that you have to migrate between instances and create a database dump which can be transfered as a file and then restored on a new machine. [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) will help as to accomplish this.

```
$ which mysqldump
$ /usr/bin/mysqldump -uroot -ppassword [database-name] > db_`date "+%d_%m_%y"`.dump
```

**NOTE:** `-u` is an argument for your _username_ and `-p` is for _password_ (there is no spaces between keys and their values)

Now from our target machine we can copy a remote dump file and restore it within current MySQL installation

```
$ scp -r [remote-user]@[remote-ip]:[remote-path] .
```

You need to provide _username_ and _remote ip address_ as well as a _path_ on remote machine to the backup file. `.` at the end of a command means _copy to current directory_. Resulting command might look like this `scp -r ubuntu@54.154.11.44:/home/ubuntu/db_22_01_19.dump .`

Having a dump locally allows us to restore database from a file. 

```
$ mysql -u root -p [database-name] < db_22_01_19.dump
```

To make sure restore procedure has been completed successfully you might want to open MySQL shell once again and check content for our database is in place

```
mysql> show databases;
mysql> use [database-name];
mysql> show tables;
mysql> select * from [table-name];
mysql> exit
```

That's it. Be vigilant and don't forget to periodically create backups of your database not to loose important data.

### Resources
* [Tutorial from DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)
* [Install MySQL using Debian packages](https://dev.mysql.com/doc/mysql-installation-excerpt/5.5/en/linux-installation-debian.html)