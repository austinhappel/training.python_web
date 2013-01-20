#!/usr/bin/env python

import socket
from time import strftime, gmtime
import os

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

# I'm not 100% sure if the 400 error codes are correct.
response_codes = {
    200: 'HTTP/1.1 200 OK\r\n',

    # This is returned if we have an HTTP request but the method is not GET.
    405: 'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD\r\n',

    # This is returned if the request is not HTTP at all, or malformed.
    400: 'HTTP/1.1 400 Bad Request\r\n'
}


# Parse the client's request.
def parse_request(request):
    """ Parses a request and returns the URI of the request. If the request is
    not an HTTP request using the GET method, an error is thrown."""

    print 'got request: ' + request

    global response_codes

    lines = request.split('\r\n')

    # Request type is in the first line.
    index_get = lines[0].find('GET')
    index_http = lines[0].find('HTTP')

    try:
        # Return the URL of the request if it's a HTTP GET request,
        # send error response otherwise.
        if index_http > -1 and index_get > -1:
            print 'Client is requesting HTML'
            uri = lines[0][(index_get + 4):index_http - 1]
            return uri

        # raise a value error if not http or GET.
        raise ValueError('The request (%s) is not an HTTP GET request.' % (lines[0]))

    # We can't go any farther if the request is bad. Send a response to the client
    # notifying them of this.
    except ValueError:
        client_error_response(index_http, index_get)


def client_error_response(index_http, index_get):
    """ Returns an error response to the client. """

    global response_codes

    if index_http > -1:
        if index_get == -1:
            print 'Have HTTP request, but invalid method.'
            client_response('', 405)
    print 'This is not an HTTP request.'
    client_response('', 400)


def client_response(msg, header_code=200):
    """ Returns a reponse to the client with the 200 OK header """

    global response_codes

    response = {
        'header_response_code': response_codes[header_code],
        'header_datetime': strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + '\r\n',
        'body': str(msg),
        'close': '\r\n'
    }

    print response['header_response_code']

    client.send(response['header_response_code'] + response['header_datetime'] +\
    response['body'] + response['close'])


def resolve_uri(uri):
    """Resolves a uri in a subfolder `web` at the current working directory."""
    cwd = os.getcwd() + '/web'
    requested_path = cwd + uri

    if os.path.exists(str(requested_path)):
        print 'path exists'
        if os.path.isfile(requested_path):
            raise NotImplementedError('Not implemented.')

        if os.path.isdir(requested_path):
            client_response('')
    else:
        raise ValueError('Path does not exist.')

while True:  # keep looking for new connections forever
    client, address = s.accept()  # look for a connection
    data = client.recv(size)
    if data:  # if the connection was closed there would be no data
        uri = parse_request(data)
        if uri != None:
            resolve_uri(uri)

        client.close()
