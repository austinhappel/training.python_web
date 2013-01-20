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


# Parse the client's request.
def parse_request(request):
    print 'got request: ' + request

    response_codes = {
        200: 'HTTP/1.1 200 OK\r\n',
        405: 'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD\r\n',
        400: 'HTTP/1.1 400 Bad Request\r\n'
    }

    header_date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + '\r\n'

    lines = request.split('\r\n')

    # Request type is in the first line.
    index_get = lines[0].find('GET')
    index_http = lines[0].find('HTTP')

    # Return the URL of the request if it's a HTTP GET request,
    # but throw a ValueError if not.
    if index_http > -1:
        if index_get > -1:
            print 'Client is requesting HTML'
            request = lines[0][(index_get + 3):index_http]
            return response_codes[200] + header_date + '\r\n' + str("<h1>your request is: " + request + "</h1>")

        # Bullet 3 wants us to raise a ValueError, but instead we'll return a 405
        # raise ValueError('The request (%s) is not an HTTP GET request.' % (lines[0]))
        print 'Have HTTP request, but invalid method.'
        return response_codes[405]

    # If this isn't an HTTP request, send 400 error (bad request)
    return response_codes[400]


while True:  # keep looking for new connections forever
    client, address = s.accept()  # look for a connection
    data = client.recv(size)
    if data:  # if the connection was closed there would be no data
        client.send(parse_request(data))
        client.close()
