---
title: leak package
date: 2017-06-26 11:24:15
tags: [python, utils, pypi]
author: Misha Behersky
---

<h3>Intro</h3>

<p>In this article I&#39;m going to describe small utility that is intended to provide some useful information about packages released to the <a href="https://pypi.python.org/pypi" target="_blank">PyPI</a>. <span class="inline-code">leak</span> is a tool that shows you all the releases of a package specified that can be downloaded and installed. Sometimes it&#39;s very useful to see a list of them in order to be able install next/previous major/minor release of a package. And therefore to see all the versions available you need to manually go to the project&#39;s page and find the version you are interested in.</p>

<p>Recent versions of <span class="inline-code">pip</span> also know how to do it, so right now <span class="inline-code">leak</span> kinda overlaps with what we have as a built in feature</p>

<pre>
<code class="language-bash">Could not find a version that satisfies the requirement django==5.2.3 
(from versions: 1.1.3, 1.1.4, 1.2, 1.2.1, 1.2.2, 1.2.3, 1.2.4, 1.2.5, 
1.2.6, 1.2.7, 1.3, 1.3.1, 1.3.2, 1.3.3, 1.3.4, 1.3.5, 1.3.6, 1.3.7, 
1.4, 1.4.1, 1.4.2, 1.4.3,</code></pre>

<h3>Usage</h3>

<p>Installation of the package is simple and &nbsp;straightforward. Just type</p>

<pre>
<code class="language-bash">pip install leak
leak </code></pre>

<p>e.g.</p>

<pre>
<code class="language-bash">leak django</code></pre>

<p>It will display you sorted list of available versions and highlight the <em><strong>most popular one</strong></em> and the <em><strong>most recent one</strong></em> (with number of downloads and release date correspondingly). It will also provide short description, package home page URL and author&#39;s name as well as email.</p>

<p><img alt="" src="/img/article/014a00967ecb3e51bd9b36a1191ffccc.png" style="height:268px; width:654px" /></p>

<h3>Implementation</h3>

<p>Behind the scenes there is simple requests-based script that calls PyPI api <span class="inline-code">http://pypi.python.org/pypi/{package_name}/json</span>&nbsp;and just parses result printing it as table with colorized text.</p>

<p>It&#39;s still under <em>not-so-active</em> development, so feel free to open an issue/PR or just write me an email with any improvement you want to see within this tool.</p>

<p>See you!</p>

<h3>Resources</h3>

<p><a href="https://pypi.python.org/pypi/leak" target="_blank">Link to the page on PyPI</a></p>

<p><a href="https://github.com/bmwant/leak" target="_blank">Link to the GitHub repository</a></p>

<p><a href="https://github.com/pypa/packaging" target="_blank">Core utilities for python packaging</a></p>

<p><a href="http://semver.org" target="_blank">How to properly version you package not adding headeache for others</a></p>

<p><a href="https://pypi.python.org/pypi/termcolor" target="_blank">How to print colored output in console</a></p>

<p><a href="http://click.pocoo.org/5/utils/#ansi-colors" target="_blank">...but I recommend to use click instead though</a></p>