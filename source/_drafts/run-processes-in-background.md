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

* Type `jobs` in the same shell. [This utility](https://man7.org/linux/man-pages/man1/jobs.1p.html) will list all jobs in current session. `jobs -l` will also display process ID or any other information available

![jobs list](/images/process_jobs.png)

* Now we can use another utility called [bg](https://man7.org/linux/man-pages/man1/bg.1p.html) to start executing this job in background. Type `bg %1` to continue running our process in the background. Note how we reference a job by prefixing its number with `%` sign

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

You are still able to track progress and examine output with tail command `tail -f output.txt`


![tail](/images/process_tail.png)

* Last step in this entangled procedure is to make sure we can drop current active session without killing the process. This might be useful in case you plan to close ssh connection to the remote and then reconnect again for the updates. Shell has [disown](https://www.cyberciti.biz/faq/unix-linux-disown-command-examples-usage-syntax/) command which is designed for this purpose.

```bash
$ disown %1
```

Note that referencing is exactly the same by the job number. However after detaching the process you will not see it within `jobs` output as current shell does not own this process anymore. Still, PID will remain the same and you can track progress by inspecting output with `tail -f output.log`

![grep](/images/process_grep.png)

### Meet nohup


### Use screen
