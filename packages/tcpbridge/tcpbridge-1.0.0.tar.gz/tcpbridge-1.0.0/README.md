### TCPBridge

[![Build Status](https://semaphoreci.com/api/v1/projects/be1ed091-9d94-49d5-8391-781d1f1d76b8/1282662/shields_badge.svg)](https://semaphoreci.com/emlidltd/tcp-bridge)

TCP bridge for data transfer

### Requirements

> Only for tests

* pytest
* pytest-cov

### Install/Uninstall

`make install`

`make uninstall`

### Example

```
import socket
from tcpbridge import SocketSink, TCPBridge

svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svr_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
svr_sock.bind(('localhost', 9002))
svr_sock.listen(1)

cli_sock, _ = svr_sock.accept()
socket_sink = SocketSink(sock=cli_sock)
```

Single endpoint TCP Bridge  

> In background

```
bridge = TCPBridge(sink=socket_sink, port_in=9000)
bridge.start()
...
bridge.stop()
```

Dual endpoint TCP Bridge 

> Not in background

```
bridge = TCPBridge(sink=socket_sink, port_in=9000, port_out=9001)
bridge.start(in_background=False)
...
bridge.stop()
```

