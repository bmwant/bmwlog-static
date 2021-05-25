---
title: Fast way to share code snippet from terminal
date: 2018-03-11 20:18:02
tags: [code, tips, cheatsheet, hints, notes]
author: Misha Behersky
---

![demo screen](/img/article/857ebbbac3813dfd8332f4ea7c29eedd.png)
Sometimes you want to quickly share code scratch over the Internet. Usually you open services like [pastebin](https://pastebin.com/) or [Github gist](https://gist.github.com/) and get a link to your code from there. I want to share a really quick way to do this from your command line with a help of [termbin](http://termbin.com/).
Assuming you already have your file `my_code.py` and you want to share it. Just type
```
$ cat my_code.py | nc termbin.com 9999
```
and you'll get an unique link to you code as an output of this command. Now you can share it with your friends or teammates.
For even better user experience you may add this command as one of your aliases like this
```
$ echo 'alias tb="nc termbin.com 9999"' >> .bashrc
$ exec $SHELL
```
In case you want the link to be copied to the clipboard you can improve command even more
```
$ sudo apt-get install xclip
$ echo 'alias tbc="nc termbin.com 9999 | xclip -selection clipboard"'
$ exec $SHELL
```
Examples of usage
```
# output link to your file in terminal
$ cat my_code.py | tb 
# save link to your shared file into clipboard
$ cat my_code.py | tbc
$ echo "Test sharing some text data" | tbc
```
This small improvement to your shell is really handy and will be helpful to quickly share snippets with others.
Thanks for reading.