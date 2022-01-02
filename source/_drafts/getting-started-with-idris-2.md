---
title: Getting started with Idris 2
tags: [idris, fp, dependent, types, macos]
author: Misha Behersky
language: en
---

### Installation

```bash
$ brew update
$ brew install coreutils gmp
curl -sSL https://www.idris-lang.org/idris2-src/idris2-0.5.1.tgz -o idris2.tgz
tar -xvzf idris2.tgz
export PREFIX=$HOME/.idris2
export PATH=$PATH:$PREFIX/bin
export DYLD_LIBRARY_PATH=$PREFIX/lib
export IDRIS2_CG=racket
```
### Resources
* https://download.racket-lang.org/
* https://idris2.readthedocs.io/en/latest/tutorial/index.html
* https://github.com/idris-lang/Idris2
* https://www.idris-lang.org/
