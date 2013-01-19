#!/usr/bin/env python

import socket
from time import strftime, gmtime

host = ''  # listen on all connections (WiFi, etc)
port = 50000
backlog = 5  # how many connections can we stack up
size = 1024  # number of bytes to receive at once

# get file to serve
file = open('tiny_html.html', 'r').read()

## create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set an option to tell the OS to re-use the socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# the bind makes it a server
s.bind((host, port))
s.listen(backlog)


def ok_response(body):
    header = 'HTTP/1.1 200 OK\n'
    h_date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + '\n'
    everything = header + h_date + '\r\n' + body
    return everything

while True:  # keep looking for new connections forever
    client, address = s.accept()  # look for a connection
    data = client.recv(size)
    if data:  # if the connection was closed there would be no data
        client.send(ok_response(file))
        client.close()
