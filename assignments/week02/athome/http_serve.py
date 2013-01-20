#!/usr/bin/env python

# Complete your HTTP Web Server. Accomplish as many of the following goals as
# you are able:
#
# * If you were unable to complete the first five steps in class, circle back
#   and finish them
#
# * Complete the 'Bonus point' parts from the first five steps, if you haven't
#   already done so
#
# * Format your directory listing as HTML
#
# * In the HTML directory listing, make the files clickable links
#
# * Add a new, dynamic endpoint. If the URI /time-page is requested, return an
#   HTML page with the current time displayed.

import socket
from time import strftime, gmtime
import os
import make_time

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
    404: 'HTTP/1.1 404 Not Found',
    # This is returned if we have an HTTP request but the method is not GET.
    405: 'HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD',

    # This is returned if the request is not HTTP at all, or malformed.
    400: 'HTTP/1.1 400 Bad Request'
}


class ClientResponse:

    cwd = os.getcwd() + '/../lab/web'

    # Parse the client's request.
    def parse_request(self, request):
        """ Parses a request and returns the URI of the request. If the request is
        not an HTTP request using the GET method, an error is thrown."""

        print 'got request:\n' + request

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

        else:
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

        print "Resolving URI: " + uri

        cwd = self.cwd

        requested_path = str(cwd + uri)

        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'txt': 'text/plain',
            'html': 'text/html'
        }

        # firstly, check if the uri is time-page.
        if uri == '/time-page':
            self.send_headers(headers=['Content-Type: text/html'])
            self.client.sendall(make_time.make_time())
            return

        if os.path.exists(requested_path):
            print 'Client is requesting a path that exists.'
            if os.path.isfile(requested_path):
                print 'Path is file, streaming asset to client.'
                asset = open(requested_path, 'r')
                fileName, fileExtension = os.path.splitext(requested_path)

                headers = [
                    'Accept-Ranges: bytes',
                    'Content-Length: ' + str(os.path.getsize(requested_path)),
                    'Content-Type: ' + (mime_types[fileExtension[1:]] if fileExtension[1:] in mime_types else 'text/plain'),
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
                print "Client is requesting a directory."
                self.send_headers(headers=['Content-Type: text/html'])
                self.client.send(self.generate_html_from_dir(requested_path))
        else:
            print "Client is requesting a path that does not exist. Sending 404."
            print requested_path
            self.send_headers(header_code=404)

    def generate_html_from_dir(self, path):
        """Generates an html list of the directory structure and returns it."""

        # directory requests may or may not have a '/' at the end...
        if path.endswith('/') == False:
            path += '/'

        # the current uri is needed to generate correct anchors for the links.
        uri = self.uri
        if uri.endswith('/') == False:
            uri += '/'

        html = '<html><head></head><body><ul>'

        for listing in os.listdir(path):
            if os.path.isdir(path + listing):
                html += '<li><a href="%s">%s</a></li>' % (uri + listing, listing)

            if os.path.isfile(path + listing):
                html += '<li><a href="%s">%s</a></li>' % (uri + listing, listing)

        html += '</ul></body></html>'
        return html

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
