import socket
import json

# 1. Create a socket server which can take two numbers, add them together, and
# return the result
#
# 2. Create a socket client that sends two numbers to the above server, and
# receives and prints the returned result.
#
# Submit your work by forking this repository. Add the server and client scripts
# to your fork and then issue a pull request.

# Create a TCP/IP socket
server_socket = socket.socket()

# Bind the socket to the port
server_address = ('localhost', 50000)

# Listen for incoming connections
server_socket.bind(server_address)

print "Waiting for connection."
while True:
    # Wait for a connection
    server_socket.listen(5)

    try:
        # Receive the data and send it back
        connection, client_address = server_socket.accept()

        print 'have connection.'

        # grab all the data from the recv buffer
        full_data = ''
        while True:
            packets = connection.recv(4096)
            if not packets:
                break
            else:
                full_data += packets
                print 'returning sum:'
                numbers = json.loads(full_data)
                num1 = float(numbers[0])
                num2 = float(numbers[1])
                result = num1 + num2
                message = 'The result: ' + numbers[0] + ' + ' + numbers[1] + ' = ' + str(result)
                print message
                connection.sendall(message)

    finally:
        print 'closing connection.'
        # Clean up the connection
        connection.close()

server_socket.close()
