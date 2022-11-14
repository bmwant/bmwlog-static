---
title: hapless. Easily run and manage background processes
tags: [bash, jobs, background, cli, python]
author: Misha Behersky
language: en
date: 2022-11-13 10:52:38
---

In the [previous article](run-processes-in-background) we've talked about running and tracking processes in the background with the tools that Linux provides. Fortunately, there is a much easier and convenient way to do that using [hapless](https://pypi.org/project/hapless/) package. This is a Python project I've been recently working on and you can install it using [pip](https://pip.pypa.io/en/stable/) like this

```bash
$ pip install --upgrade hapless
```

The only thing you need to add is a short prefix `hap run` to a command you want to run in the background

```bash
$ hap run ./my_long_running_script.sh
$ hap run python another_script.py --with-flags --and-arguments=true
```

It will automatically handle output redirection and detach process from current shell, so it is safe to launch it within remote ssh session, close the connection and return back in a while. To retrieve status of the processes and get list of all the tracked ones simply type

```bash
$ hap
# or
$ hap status
```

On a creation it will also generate unique id for each process started, but you can also provide your own alias using `-n`/`--name` flag to refer the process later

![hap status](/images/hap_status.png)

Besides that you can specify process by providing its sequential number, so all the invocations below are valid

```bash
$ hap status 1  # just a number from the first column
$ hap status hap-23i0lo  # automatically generated ID
$ hap status long  # any custom name you provided when launching with -n flag
```

![hap single status](/images/hap_status_hap.png)

There is also a `-v`/`--verbose` flag for the `status`/`show` command, so you can get detailed information about the process including complete environment and paths to output files.

### Options available

Next thing you usually want to do is to check an output for the process (both stdout and stderr is possible). Keep in mind that you can refer to process the same way as above

```bash
$ hap logs hap-dmp4ch  # show stdout
$ hap logs -f 2  # follow logs, similar to `tail -f`
$ hap logs --stderr long  # print stderr for the process named long
```

Another useful feature is the ability to pause execution of the process and resume it at any point

```bash
$ hap pause hap-23i0lo
$ hap suspend hap-23i0lo  # same as above
# resume execution
$ hap resume hap-23i0lo
```

Moreover, you can send any arbitrary signal to the process through *hapless*

```bash
$ hap signal hap-23i0lo 9  # sends SIGKILL
$ hap signal hap-xfu2q0 15  # sends SIGTERM
```

### Cleanup

*hapless* stores information about processes internally and preserves data upon completion, so if you don't care about finished processes you might want to invoke `hap clean` which will leave only ongoing ones (note that in the summary table the PID of the finished processes is dimmed as those do not exist anymore).

![hap clean](/images/hap_clean.png)

That's almost it as the main idea is to make launch command as easy as possible and have a convenient way to quickly check status of processes started (simply `hap`). For the rest of options available invoke `hap --help` or check the link below for the documentation.

### Resources

* [Complete list of commands available](https://github.com/bmwant/hapless/blob/main/USAGE.md)
