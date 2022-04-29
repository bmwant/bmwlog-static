---
title: Run processes in the background
tags: [bash, linux, jobs, bg, fg]
author: Misha Behersky
language: en
date: 2022-04-28 13:22:34
---

Suppose you have some long running script (we'll use Python here as an example)

```python
import time

def main():
    for i in range(1000):
        print(f"Processing {i}...", flush=True)
        # Actual heavy-lifting instead of sleeping
        time.sleep(10)

if __name__ == "__main__":
    main()
```

and you have launched it in active terminal session like this `python script.py` (or `poetry run python script.py`).

Suddenly you've realized that this is going to take couple of hours to finish and you need to either exit current shell or logout from remote instance where you have your ssh connection established. Nobody wants to lose the time and work spent and in most cases you cannot just restart a process the proper way (see options below) due to the reasons:

* script is most likely not [idempotent](https://en.wikipedia.org/wiki/Idempotence#Computer_science_meaning) (in other words it cannot be launched multiple times producing same output results and not causing any additional side-effects)
* script is not designed to be resumed, it cannot pick up from the interrupted spot
* it will break consistency between your data when invoked repeteadly
* let's face it: for simple scripts you don't generally think about all the items above and do not handle all the possible corner cases

### Solution

* Press `Ctrl`-`Z` in active window. This will send [SIGTSTP](https://dsa.cs.tsinghua.edu.cn/oj/static/unix_signal.html) signal to your process causing it to suspend

![stopped process](/images/process_stopped.png)

* Type `jobs` in the same shell. [This utility](https://ss64.com/bash/jobs.html) will list all jobs in current session. `jobs -l` will also display process ID or any other information available

![jobs list](/images/process_jobs.png)

* Now we can use another utility called [bg](https://ss64.com/bash/bg.html) to start executing this job in background. Type `bg %1` to continue running our process in the background. Note how we reference a job by prefixing its number with `%` sign

![bg](/images/process_bg.png)

This would be enough if you process does not produce output to the terminal. Otherwise it can mess up a screen or in case messages are produced fast enough make it impossible to work properly within the session. You can type `stty tostop` to make sure that job will be stopped automatially once it writes to its standard output or standard error.

In the meanwhile we will use [reredirect](https://github.com/jerome-pouiller/reredirect) to dynamically redirect output of an already running process.

```bash
$ git clone https://github.com/jerome-pouiller/reredirect.git
$ cd redirect
$ make

# skip this step if you do not have root permissions
$ sudo make install
```

Use process identificator obtained from `jobs -l` and launch this command

```bash
# reredirect -m [output-filename] [PID]
$ reredirect -m output.log 22729

# Run from installation directory if you do not have root permissions
$ ./reredirect -m output.log 22729
```

You are still able to track progress and examine output with tail command `tail -f output.log`

![tail](/images/process_tail.png)

* Last step in this entangled procedure is to make sure we can drop current active session without killing the process. This might be useful in case you plan to close ssh connection to the remote and then reconnect again for the updates. Shell has [disown](https://www.cyberciti.biz/faq/unix-linux-disown-command-examples-usage-syntax/) command which is designed for this purpose.

```bash
$ disown %1
```

Note that referencing is exactly the same by the job number. However after detaching the process you will not see it within `jobs` output as current shell does not own this process anymore. Still, PID will remain the same and you can track progress by inspecting output with `tail -f output.log`

![grep](/images/process_grep.png)

### Meet nohup

If you want to follow a procedure described above from the very beginning you should first make sure all the output is written to a text file (to omit all the hacks with modifying processes at a runtime)

```bash
$ poetry run python script.py > output.log 2>&1
```

In this command we redirect *stdout* to a `output.log` file and then pointing *stderr* to the same location where *stdout* goes.

Then you apply `Ctrl`-`Z` and `bg` trick to ensure process is running in the background. To simplify this you can initially add ampersand symbol (`&`) to the end of the command, so it will run as a backround process in the first place.

```bash
$ poetry run python script.py > output.log 2>&1 &
```

![background](/images/process_background.png)

Note that you can always bring any process running in the background to foreground. [fg](https://ss64.com/bash/fg.html) does exactly this thing. Remember to refer the job by percentage sign and its number when invoking. `fg %1` will send first job to the foreground and you can again bring it to the background at any time needed.

Next step would be to call `disown` on the job (like `disown %1`) to make sure we can safely close current shell session without interrupting our process.
Lastly, meet [nohup](https://ss64.com/bash/nohup.html) utility which can also help us to omit this step if we plan to launch such a long-running background process. So, final version of the invocation of your command **should always look like this**

```bash
# nohup [your command goes here] > output.log 2>&1 &
$ nohup python script.py > output.log 2>&1 &
```

This is the proper and safe way to execute process in the background and ensure it will not mess current session with its output or terminate unexpectedly when session is closed.

### Use screen

There is a preferred way of running anything on the remote instance via ssh connection, so dropped connection will not affect work being done there. We can also use same tool for running background processes. First, install [screen](https://ss64.com/bash/screen.html) program

```bash
# Depending on the system you run
$ sudo apt install -y screen
# or
$ sudo yum install -y screen
```

Next, type `screen` which will automatically move you into new session where you can simply run your script without any modifications

```bash
$ python script.py
```

and then detach from current screen session by typing `Ctrl`-`A` then `D`.

To check the list of all active screens (and you can launch as many of them as you like) type this

```bash
$ screen -ls
```

To restore back into your detached session you can type command below and check the progress and output of your command

```bash
$ screen -r
```

There is a lot more of this utility and it's a really powerful tool to be used as a window manager / terminal multiplexer, but for the purpose of running a process in the background this should be enough. At this note I'm leaving you here with a bunch of extra links to check. Stay curious, fight for freedom 🇺🇦

### Resources

* [jobs utility](https://man7.org/linux/man-pages/man1/jobs.1p.html)
* [nohup utility](https://man7.org/linux/man-pages/man1/nohup.1.html)
* [bg command](https://man7.org/linux/man-pages/man1/bg.1p.html)
* [fg command](https://man7.org/linux/man-pages/man1/fg.1p.html)
* [How to use screen utility](https://linuxize.com/post/how-to-use-linux-screen/)
