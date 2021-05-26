---
title: Disable Internet connection in unittests
date: 2017-09-20 13:48:42
tags: [python, mock, unittest, pytest, socket]
author: Misha Behersky
language: en
---

<p>Sometimes you can forget to mock all of the functions with side effect within your unittests and that might cause some issue. First it violates unittests principle to be launched in isolated environment and to not strictrly depend on any component that is not tested at the moment. And it might happen that you will not be able to launch unittests after your Internet connection is gone.</p>

### Solution

<p>Obviously you should use pytest for your unittests and it has nice <a href="http://pythontesting.net/framework/pytest/pytest-fixtures-nuts-bolts/#autouse" target="_blank">autouse fixtures</a>. We can mock built in <span class="inline-code">socket</span> module before any invocation of test and therefore intercept any call that tries establish some connection. Then some kind of exception should be thrown showing we have to mock function thas has side effect.</p>

<pre>
<code class="language-python">import pytest


class SocketBlockedException(RuntimeError):
    """
    An exception raised in tests when some function tries to establish a connection.
    """


@pytest.yield_fixture(autouse=True)
def disable_socket():
    socket_mock = mock.patch('socket.socket', side_effect=SocketBlockedException).start()
    yield
    socket_mock.stop()</code></pre>

<p>This approach will ensure we do not have any unexpected calls and our unittests can be launched even without Internet connection being active.</p>

### Resources

<p><a href="https://github.com/miketheman/pytest-socket" target="_blank">pytest plugin to disable socket calls</a></p>

<p><a href="http://alexmarandon.com/articles/python_mock_gotchas/" target="_blank">python mock gotchas</a></p>
