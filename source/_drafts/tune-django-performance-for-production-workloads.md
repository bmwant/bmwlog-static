---
title: Tune Django performance for production workloads
tags: [python, django, gunicorn, nginx, highload]
author: Misha Behersky
language: en
---

### Collecting baseline metrics

First of all we need to obtain metrics that are going to represent our baseline performance. This is critical to see whether our optimizations are affecting performance and in which way. It's often possible to introduce a change which makes performance drastically worse.
We are going to use [Hey]() load testing tool to simulate the load and will make further assumptions based on the results provided by this benchmark.


```bash
$
```
