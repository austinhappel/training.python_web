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


def parse_request(request):
    print 'got request: ' + request
    lines = request.split('\r\n')

    index_get = lines[0].find('GET')
    index_http = lines[0].find('HTTP')

    if (index_get > -1 and index_http > -1):
        print 'Client is requesting HTML'
        request = lines[0][(index_get + 3):index_http]
        return "<h1>your request is: " + request + "</h1>"


def ok_response(body):
    header = 'HTTP/1.1 200 OK\r\n'
    h_date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + '\r\n'
    everything = header + h_date + '\r\n' + body
    return everything

while True:  # keep looking for new connections forever
    client, address = s.accept()  # look for a connection
    data = client.recv(size)
    if data:  # if the connection was closed there would be no data
        response = parse_request(data)
        client.send(ok_response(response))
        client.close()
