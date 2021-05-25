---
title: Replacement for your Makefile
date: 2016-10-19 15:48:23
tags: [python, make, devops, infra, tools]
author: Misha Behersky
---

<h3>Intro</h3>

<p>Makefile is a <a href="https://www.gnu.org/software/make/manual/make.html" target="_blank">gnu utility</a> that was aimed to simplify compilation process. You can forget long command with dozens of flags or params and with makefile u have targets and they can save your time while typing complicated command. If you familiar with bash aliases then it&#39;s very similar concept. That helps a lot in day to day tasks. The command below would be easy as <strong>make tests</strong></p>

<pre>
<code class="language-bash">tests:
	@pip install -r requirements/test-requirements.txt
	@py.test --junitxml=./testResults.xml --cov-config=.unit_coveragerc --cov-report xml --cov ./ test/</code></pre>

<p>But in a large project this file can grow up to 1K lines of code which is hard to read and understand because of such reasons:</p>

<ul>
	<li>you should learn completely different syntax (that differs even from bash scripts you probably use too)</li>
	<li>hard to understand for newcomers and some rules are really hard to remember</li>
	<li>you cannot use it on different platforms like FreeBSD&nbsp;</li>
	<li>you want to have same language across your projects, it&#39;s more convenient</li>
</ul>

<p>So, meet <a href="http://www.pyinvoke.org" target="_blank">pyinvoke</a> - a tool that helps you deal with issues above and can completely replace makefile. It&#39;s very similar to the <a href="https://github.com/ruby/rake" target="_blank">Ruby Rake</a> one.</p>

<p>In typical python project you have a bunch of task you use from time to time - just use the decorator and write them as usual python functions.</p>

<p>What will you have out of the box:</p>

<ul>
	<li>namespacing</li>
	<li>task aliasing</li>
	<li>before/after&nbsp;hooks</li>
	<li>parallel execution</li>
	<li>flag-based style of command-line parsing</li>
	<li>multiple tasks in single invocation&nbsp;</li>
</ul>

<p>The tool is python 3 compatible and has no other dependencies.&nbsp;It&#39;s definitely worth it to try this tool.</p>

<h3>Slides</h3>

<p>My slides from PyCon Poland 2016 Lightning talk</p>

<iframe src="//www.slideshare.net/slideshow/embed_code/key/3JUtakXCYqnKwc" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe>

<h3>Resources</h3>

<p><a href="http://medium.com/@tomchentw/makefile-to-automate-things-304ce6779bf" target="_blank">Makefile tutorial</a></p>