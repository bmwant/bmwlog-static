---
title: Простий сокетний сервер на Python
date: 2014-11-11 16:42:22
tags: [python, server, socket]
author: Misha Behersky
language: ua
archived: true
---

І відразу код

```python
import socket
import sys

HOST = ''  # interface
PORT = 8888  # port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')

# Now keep talking with the client
while 1:
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    conn.send(b'Welcome to the server. Type something and hit enter\n')
    while True:
        data = conn.recv(1024)
        reply = 'Reply text\n'
        if not data:
            break

        conn.sendall(bytes(reply, 'utf-8'))

    conn.close()

s.close()
```

Щоб протестувати, виконаємо команду

```bash
$ telnet localhost 8888
```

і у відповідь на введені нами дані маємо отримати

```
Reply text.
```
