---
title: Create simple Tor hidden service
date: 2017-12-14 13:43:37
tags: [security, tor, hacking, centos]
author: Misha Behersky
---

<p>In this article I want to share how it&#39;s simple to create a service in Onion web (Tor network). We will create simple web page that would be accessible via Tor browser. I will show the example for&nbsp;CentOS 7 (RHEL).</p>

<p>Make sure that your have configured your server as a webserver (nginx is assumed).</p>

<p>Next install tor package</p>

<pre>
<code class="language-bash">yum install epel-release
yum install tor</code></pre>

<p>and configure it&nbsp;<span class="inline-code">cp /usr/share/tor/defaults-torrc /etc/tor/torrc</span></p>

<p>Now edit config that was copied and make sure lines below are uncommented</p>

<pre>
<code class="language-bash">RunAsDaemon 1

DataDirectory /var/lib/tor

HiddenServiceDir /var/lib/tor/my_hidden_site
HiddenServicePort 80 127.0.0.1:8333

</code></pre>

<p>Skip all the lines intented for <strong>relays</strong> and modify only the one for&nbsp;<strong>location-hidden services</strong></p>

<p>Now update nginx configuration to point to your hidden resource&nbsp;<span class="inline-code">vim /etc/nginx/conf.d/my_hidden_site.conf</span></p>

<p>Paste sample configuration in that file</p>

<pre>
<code class="language-bash">server {
    listen       8333 default_server;
    listen       [::]:8333 default_server;
    server_name  _;
    root         /usr/local/my_hidden_site;

    location / {
   	    try_files $uri $uri/ =404;
    }
}</code></pre>

<p>Make sure you have created same sample html page at <span class="inline-code">/usr/local/my_hidden_site</span> directory&nbsp;</p>

<pre>
<code class="language-html">&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;My hidden service&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;h1&gt;Hey there from Tor!&lt;/h1&gt;
  &lt;/body&gt;
&lt;/html&gt;</code></pre>

<p>Now just restart nginx and tor services for changes to take effect</p>

<pre>
<code class="language-bash">nginx -t &amp;&amp; nginx -s reload
systemctl restart tor.service</code></pre>

<p>Check content of <span class="inline-code">/var/lib/tor/my_hidden_service/hostname</span>, open Tor browser and point it to the url generated. That&#39;s it.</p>

<h3>Notes</h3>

<p>This is simplified tutorial assuming that you have SELinux disabled. To check current status and disable it if not yet execute following</p>

<pre>
<code class="language-bash">sestatus
setenforce 0</code></pre>

<p>The other issue that might prevent tor service from start is permissions on directories. So make sure that you have proper access rights on folder <span class="inline-code">/var/lib/tor/my_hidden_service</span> (or any other folder that you&#39;ve specified)</p>

<pre>
<code class="language-bash">sudo chmod -R toranon:toranon /var/lib/tor/my_hidden_service</code></pre>

<h3>Resources</h3>

<p><a href="https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7" target="_blank">Install nginx on CentOS 7</a></p>

<p><a href="https://wiki.centos.org/HowTos/SELinux" target="_blank">How to deal with SELinux</a></p>