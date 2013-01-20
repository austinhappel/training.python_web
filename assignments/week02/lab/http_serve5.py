#!/usr/bin/env python

# Save the file as http_serve5.py
# Update the resolve_uri method. If the URI names a file, return it as the body of a 200 OK response.
# You'll need a way to return the approprate Content-Type: header.
# Support at least .html, .txt, .jpeg, and .png files
# Try it out.

import socket
from time import strftime, gmtime
import os

host = ''  # listen on all connections (WiFi, etc)
port = 50000
backlog = 5  # how many connections can we stack up
size = 1024  # number of bytes to receive at once

## create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set an option to tell the OS to re-use the socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# the bind makes it a server
s.bind((host, port))
s.listen(backlog)

# I'm not 100% sure if the 400 error codes are correct.
response_codes = {
    200: 'HTTP/1.1 200 OK',

    # This is returned if we have an HTTP request but the method is not GET.
    405: 'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD',

    # This is returned if the request is not HTTP at all, or malformed.
    400: 'HTTP/1.1 400 Bad Request'
}


class ClientResponse:

    # Parse the client's request.
    def parse_request(self, request):
        """ Parses a request and returns the URI of the request. If the request is
        not an HTTP request using the GET method, an error is thrown."""

        print 'got request: ' + request

        global response_codes

        lines = request.split('\r\n')

        # Request type is in the first line.
        index_get = lines[0].find('GET')
        index_http = lines[0].find('HTTP')

        try:
            if index_http > -1 and index_get > -1:
                # Resolve the URL of the request if it's a HTTP GET request,
                # send error response otherwise.
                uri = lines[0][(index_get + 4):index_http - 1]
                self.uri = uri  # save the uri for other methods to use if needed
                self.resolve_uri(uri)

            else:
                # raise a value error if not http or GET.
                raise ValueError('The request (%s) is not an HTTP GET request.' % (lines[0]))

        # We can't go any farther if the request is bad. Send a response to the client
        # notifying them of this.
        except ValueError:
            self.client_error_response(index_http, index_get)

    def client_error_response(self, index_http, index_get):
        """ Returns an error response to the client. """

        if index_http > -1:
            if index_get == -1:
                print 'Have HTTP request, but invalid method. Sending 405 header.'
                self.send_headers(header_code=405)
                self.client.close()

        print 'This is not an HTTP request. Sending 400 header.'
        self.send_headers(header_code=400)
        self.client.close()

    def send_headers(self, header_code=200, headers=[]):
        """sends fully formed headers to the client."""
        global response_codes

        myHeaders = ''
        default_header = [
            response_codes[header_code],
            'Date: '  + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
        ]

        # Build the header string with the default headers first
        for x in default_header:
            myHeaders += x + '\r\n'

        # Append any additional headers passed in
        for x in headers:
            myHeaders += x + '\r\n'

        myHeaders += '\r\n'

        print "sending headers:"
        print myHeaders

        self.client.send(myHeaders)

    def resolve_uri(self, uri):
        """Resolves a uri in a subfolder `web` at the current working directory."""

        print "Resolving URI"

        cwd = os.getcwd() + '/web'
        requested_path = cwd + uri

        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'txt': 'text/plain',
            'html': 'text/html'
        }

        if os.path.exists(str(requested_path)):
            print 'path exists.'
            if os.path.isfile(requested_path):
                print 'path is file, streaming asset to client.'
                asset = open(requested_path, 'r')
                fileName, fileExtension = os.path.splitext(requested_path)
                headers = []

                if fileExtension[1:] in mime_types:
                    headers = [
                        'Accept-Ranges: bytes',
                        'Content-Length: ' + str(os.path.getsize(requested_path)),
                        'Content-Type: ' + mime_types[fileExtension[1:]],
                        'Connection: keep-alive'
                    ]

                    self.send_headers(headers=headers)

                    while True:
                        strng = asset.readline(512)
                        if not strng:
                            break
                        self.client.send(str(strng))

                    asset.close()
                    client.close()

            if os.path.isdir(requested_path):
                self.client_response(msg='')
        else:
            raise ValueError('Path does not exist.')

    def __init__(self, client, data, error=False):
        self.client = client
        self.parse_request(data)

# keep looking for new connections forever
while True:
    client, address = s.accept()  # look for a connection
    data = client.recv(size)
    if data:  # if the connection was closed there would be no data
        response = ClientResponse(client, data)
        client.close()
