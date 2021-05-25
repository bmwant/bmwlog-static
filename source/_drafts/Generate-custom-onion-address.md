---
title: Generate custom onion address
date: 2018-02-17 18:21:55
tags: [tor, security, hacking, privacy, deepweb]
author: Misha Behersky
---

<p>When creating a hidden tor service you might see resulting address looks like a mess of letters. There is an algorithm used to generate such an address:</p>

<ol>
	<li>Public/private key pair is generated</li>
	<li>Public key got hashed with <a href="https://en.wikipedia.org/wiki/SHA-1" target="_blank">SHA-1</a> algorithm</li>
	<li>First 80 bits of the output are encoded with <a href="https://en.wikipedia.org/wiki/Base32" target="_blank">Base32</a></li>
	<li>The result is the hostname of your onion service</li>
</ol>

<p>So, to have your own customized address you need to generate bunch of keys and check whether they fit your requirements. For bruteforcing purposes we&#39;ll be using&nbsp;<a href="https://github.com/ReclaimYourPrivacy/eschalot" target="_blank">eschalot</a>&nbsp;tool. Let&#39;s download and use it immediately</p>

<pre>
<code class="language-bash"># sudo apt install build-essential libssl-dev
# or whatever package os/package manager you use
git clone https://github.com/ReclaimYourPrivacy/eschalot.git
cd eschalot/
make
./eschalot -vp name -t 8 &gt; results.txt</code></pre>

<p>Now we are looking for address with prefix <span class="inline-code">name</span> and using 8 threads we&#39;ll output results in <span class="inline-code">results.txt</span> file. When process eventually complete (the longer prefix the longer a search) you can copy private key to the folder of yor service (e.g. <span class="inline-code">/var/lib/tor/hidden_service/private_key</span>) and restart tor.</p>

<pre>
<code class="language-bash"># or whatever service manager you use
systemctl restart tor.service</code></pre>

<p>With such a tool you can search by prefixes/suffixes or even regular expressions but keep in mind that for entries longer than 6 characters it may take a lot of time (days and exponentially growing to years and more).</p>

<h3>Resources</h3>

<p><a href="https://security.stackexchange.com/questions/29772/how-do-you-get-a-specific-onion-address-for-your-hidden-service" target="_blank">StackOverflow discussion</a></p>

<p><a href="https://github.com/katmagic/Shallot" target="_blank">Shallot tool for generating&nbsp;custom names</a></p>

<p><a href="https://github.com/lachesis/scallion" target="_blank">Scalion tool for generating custom names</a></p>