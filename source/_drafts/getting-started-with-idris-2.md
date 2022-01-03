---
title: Getting started with Idris 2
tags: [idris, fp, dependent, types, macos]
author: Misha Behersky
language: en
---

### Installation

There is a dependency on [Racket](https://racket-lang.org/) programming language, so make sure you have downloaded and installed it first (it's a straightforward installation using `.dmg` file). Build process relies on Racket binaries, so don't forget to make them available by adjusting your `PATH` variable

```bash
$ export PATH=$PATH:"/Applications/Racket v8.3/bin"
```


```bash
$ brew update
$ brew install coreutils gmp
$ curl -sSL https://www.idris-lang.org/idris2-src/idris2-0.5.1.tgz -o idris2.tgz
$ tar -xvzf idris2.tgz
$ export PREFIX=$HOME/.idris2
$ export PATH=$PATH:$PREFIX/bin
$ export DYLD_LIBRARY_PATH=$PREFIX/lib
$ export IDRIS2_CG=racket
$ make bootstrap-racket
$ make install
```

Optionally, you can build a documentation by invoking yet another make target and opening `index.html` within your browser

```bash
$ make install-libdocs
$ open `idris2 --libdir`/docs/index.html
```

### Validating installation

To check whether everything works properly you can launch an extensive set of unittests with the command

```bash
$ make test
```

The process might take a while and you should see a bunch of `success` steps on the way as well as
`472/472 tests successful` message in the very end

![tests](/images/idris_tests.png)

### Add to PATH and install autocompletion

```bash
autoload -U +X compinit && compinit
autoload -U +X bashcompinit && bashcompinit
eval "$(idris2 --bash-completion-script idris2)"
```

### Hello, World!

Obviously, there is no reason to install a new programming language if we are not going to write a program in it. So create a text file `hello.idr` and open it in your favourite text editor

```idr
main : IO ()
main = putStrLn "Hello, World!"
```

That's it, check [this website](https://bmwant.github.io/idris-is-awesome.github.io/) to get started with some basic code examples in Idris or scroll down to the resources to get to tutorials and other useful links.

### Resources

* [Download Racket](https://download.racket-lang.org/)
* [Idris 2 tutorial](https://idris2.readthedocs.io/en/latest/tutorial/index.html)
* [Idris 2 official repository](https://github.com/idris-lang/Idris2)
* [Idris website](https://www.idris-lang.org/)
