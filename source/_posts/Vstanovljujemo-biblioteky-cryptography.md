---
title: Встановлюємо бібліотеку cryptography
date: 2014-12-19 16:56:14
tags: [python, cryptography, pip, windows, wheels]
author: Misha Behersky
---

<h3>
 Встановлюємо Cryptography для Windows
</h3>
<p>
 <a href="https://cryptography.io/en/latest/" target="_blank">
  Cryptography
 </a>
 - бібліотека для роботи з криптографічними функціями у Python. Але встановити її
 <a href="https://cryptography.io/en/latest/installation/#on-windows" target="_blank">
  по інструкції
 </a>
 мені так і не вдалося. Для
 <a href="https://pip.pypa.io/en/latest/index.html" target="_blank">
  pip
 </a>
 є крута штука, яка називається
 <a href="http://pythonwheels.com" target="_blank">
  wheels
 </a>
 . Це вже скомпільовані бібліотеки під вашу платформу, які пришвидшують встановлення і не потребують наявності компілятора.
</p>
<p>
 Отож, для
 <strong>
  Python 2.7, win32
 </strong>
 <a href="https://pypi.python.org/packages/cp27/c/cryptography/cryptography-0.7.1-cp27-none-win32.whl#md5=05ed516ca15f25d2169f7629ed1da1d912670ee329ff" target="_blank">
  завантажуємо
 </a>
 <em>
  wheel
 </em>
 -файл і виконуємо команду:
</p>
<pre>
<code class="language-bash">pip install cryptography-0.7.1-cp27-none-win32.whl</code></pre>
<p>
 Аналогічно можна зробити для інших платформ і версій Python. Можливо знадобиться додатково встановити
 <a href="http://slproweb.com/products/Win32OpenSSL.html" target="_blank">
  OpenSSL
 </a>
 (лінк в ресурсах).
</p>
<h3>
 Ресурси
</h3>
<p>
 <a href="https://www.crypto101.io" target="_blank">
  Курс з криптографії (англ.)
 </a>
</p>
<p>
 <a href="https://pypi.python.org/pypi/cryptography" target="_blank">
  Cryptography на PyPi
 </a>
</p>
<p>
 <a href="http://slproweb.com/download/Win32OpenSSL-1_0_1j.exe" target="_blank">
  OpenSSL для win32
 </a>
</p>