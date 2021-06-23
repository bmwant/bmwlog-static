---
title: Signing your github commits with GPG keys
date: 2019-06-04 12:05:59
tags: [gpg, github, ubuntu, git, security]
author: Misha Behersky
language: en
---

If you ever wondered how to sign your commits (to assure others that it was you who really did the commit) or just wanted a nice `Verified` label right after your commit message on github page - you opened the right article to follow.

![verified](/old/article/487ba60287903628a1d2df8793048d38.png)

### Installing requirements
First you need to install [GPG command line tools](https://www.gnupg.org/download/) allowing you to create a personal key which will be using to sign your commits. We need to install `libgpg-error`, `libgcrypt`, `libksba`, `libassuan`, `ntbTLS` and `nPth`.

```bash
$ mkdir /tmp/gpg
$ cd /tmp/gpg
$ wget https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.31.tar.bz2
```

Optionally, after downloading an archive you might check the file not to be broken and downloaded correctly. Just invoke `sha1sum` executable on a file and check the output with the one [provided on the site](https://www.gnupg.org/download/integrity_check.html) (at the bottom of the page).

```bash
$ sha1sum libgpg-error-1.31.tar.bz2
2bafad316d4e3e12bae4822b14ed9020090e6acf  libgpg-error-1.31.tar.bz2
```

If checksum is the same unpack the archive and build libraries from source code, otherwise try to download it again or by using `curl` or your browser.

```bash
$ tar -xvf libgpg-error-1.31.tar.bz2
$ cd libgpg-error-1.31
$ ./configure
$ make
$ sudo make install
```

You won't see any **success** message so just check the output to contain `Libraries have been installed in` without any critical warnings. Just follow the procedure with every item in the list below

![gpg tools](/old/article/ecd05adc745537c089dcacf110b881d3.png)

Check that we have our new fresh version installed

```bash
$ gpg --version
gpg (GnuPG) 2.2.7
libgcrypt 1.8.2
Copyright (C) 2018 Free Software Foundation, Inc.
```

### Install Pinentry
_Pinentry_ is a collection of passphrase entry dialogs which is required for almost all usages of GnuPG and therefore is required to be install. The good news is that the installation process is completely the same. Also you need to choose any GUI backend (gtk/gnome/qt etc) and make sure at least one is installed (you can always `sudo apt-get install gtk2.0` if in doubt)

```bash
$ wget https://www.gnupg.org/ftp/gcrypt/pinentry/pinentry-1.1.0.tar.bz2
$ tar -xvf pinentry-1.1.0.tar.bz2
$ cd pinentry-1.1.0/
$ ./configure
$ make
$ sudo make install
```

**NOTE**: on MacOS system just use [brew](https://brew.sh/) to seamlessly install `gpg`: `brew install gpg`. See [this answer](https://stackoverflow.com/a/40066889/1744914) in case of any issues.

### Generating new key

```bash
$ gpg --full-generate-key
```

Press <kbd>Enter</kbd> to choose all the default values `RSA and RSA` but only change `keysize` from **2048** to **4096**.
Your key has been generated and you can list of all the keys available on your system with

```bash
$ gpg --list-secret-keys --keyid-format LONG
```

Now we are ready to add that key to our Github account. Just follow the instructions [here](https://help.github.com/articles/adding-a-new-gpg-key-to-your-github-account/) and insert an output from the command below

```bash
$  gpg --armor --export <your-key-id>
```

where **your-key-id** is the second part of the listing keys output `rsa4096/<your-key-id>` after the slash.

Now you are ready to configure git signing commits for a given repository or globally

```bash
$ git config commit.gpgsign true  # current repository
$ git config --global commit.gpgsign true  # globally
$ git config --global user.signingkey <your-key-id>
```

And when creating your next commit do not forget to provide `-S` flag:

```bash
$ git commit -S -m "My first signed commit"
```

**NOTE**: [you might omit](https://stackoverflow.com/a/20628522/1744914) `-S` flag if `commit.gpgsign` git config is set to `true`

Watch a nice label on your commits history on Github. Happy coding!

### Resources
* [Generating new key tutorial from Github](https://help.github.com/articles/generating-a-new-gpg-key/)
* [Git documentation on signing your work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
