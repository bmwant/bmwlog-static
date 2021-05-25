---
title: Simple FFI in Idris
date: 2020-03-26 18:41:40
tags: [idris, ffi, c, functional]
author: Misha Behersky
---

[FFI](https://en.wikipedia.org/wiki/Foreign_function_interface) *Foreign Functions Inerface* allows you to call a code written in one language from a code written in another language. In this post I will show you how to do that in [dependently typed](https://wiki.haskell.org/Dependent_type) programming language called [Idris](https://www.idris-lang.org/). We will be able to call C code from Idris and vice versa.

### Invoking C code from Idris

First let's create simple program in C which will allow us to calculate factorial (file `factorial.c`)

```c
#include "factorial.h"

int factorial(int number) {
    if(number == 0) return 1;
    return number * factorial(number-1);
}
```

Header file is also required as it will provide a function declaration for our exposed factorial function (file `factorial.h`)

```c
int factorial(int);
```

Now you should be able to compile it with [GCC](https://gcc.gnu.org/) like this

```bash
$ gcc -c factorial.c
```

Once that done let's look at Idris code which needs only two extra directives to make everything works

```idris
module Main

%include C "factorial.h"
%link C "factorial.o"

factorial : Int -> IO Int
factorial x = foreign FFI_C "factorial" (Int -> IO Int) x

main : IO ()
main = do result <- factorial 9
          putStrLn ("factorial 9 = " ++ show result)
```

As you can see we define a function as usually with a special call to *foreign* and the rest is handled by the underlying runtime implementation.

![type of foreign](/img/article/50c28852f2173f9baa8a8cb19ae450a9.png)

Now you are able to either compile your code or call it directly from a REPL

```
$ idris ffi.idr -o ffi
$ ./ffi
factorial 9 = 362880

$ idris ffi.idr
*ffi> :exec main
factorial 9 = 362880
```

### Calling bulletproof Idris code from C

For this example we are going to create Idris data type which is equivalent to the list of integers (file `list.idr`)

```idris
nil : List Int
nil = []

cons : Int -> List Int -> List Int
cons x xs = x :: xs

showList : List Int -> IO String
showList xs = do putStrLn "Our list is: "
                 pure $ show xs

exportList : FFI_Export FFI_C "list.h" []
exportList = Data (List Int) "ListInt"
  $ Fun nil "nil"
  $ Fun cons "cons"
  $ Fun showList "showList"
  $ End
```

We provide `nil` and `cons` functions allowing to construct a list and helper `showList` function which displays our list on a screen. As opposed to C header file which declares functions we need to have special export functions (`exportList` from the above) which defines functions and types alongside their aliases as a return value. To proceed type `idris list.idr --interface -o list.o` into a shell. This code will generate object file and a header which we are going to include into our C source code

```c
#include "list.h"

int main() {
  VM* vm = idris_vm();
  ListInt lst = cons(vm, 10, cons(vm, 20, nil(vm)));
  printf("%s\n", showList(vm, lst));
  close_vm(vm);
  return 0;
}
```

C part is a bit trickier as we need to create an Idris virtual machine which will be running our functions and every function call also expects `vm` as a first parameter. At the end we need to free resources, so there is a `close_vm` call as well.

Finally back to our compilation command which is a bit complex this time

```bash
$ gcc idris_list.c list.o `idris $@ --include` `idris $@ --link` -o list
```

and if nothing goes wrong you should be able to run `list` executable

```bash
$ ./list
Our list is:
[10, 20]
```

Ok, at this point you should have an overall idea of how to do inter-language calls. This might be useful for creating language bindings for popular libraries in Idris (like [this Qt binding for Haskell](http://www.isptech.co.uk/qtHaskell/index.html) for example). So if you are interested in developing ecosystem for this amazing language here's your next adventure. Happy coding!

### Resources

* [Idris documentation on FFI](http://docs.idris-lang.org/en/latest/reference/ffi.html)
* [Programming in Idris by examples](https://bmwant.github.io/idris-is-awesome.github.io/)