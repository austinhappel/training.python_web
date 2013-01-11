import socket
import json


def is_number(s):
    """basic guardian to verify numeric input"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_input():

    while True:
        num1 = raw_input('One number please: ')
        if is_number(num1):
            break
        else:
            print 'Hmm, looks like you didn\'t enter a number. Try again.'

    while True:
        num2 = raw_input('Another number please: ')
        if is_number(num2):
            break
        else:
            print 'Hmm, looks like you didn\'t enter a number. Try again.'

    get_result(num1, num2)


def get_result(num1, num2):
    # save number pair
    numbers = (num1, num2)
    numbersjson = json.dumps(numbers)

    # Create a TCP/IP socket
    my_socket = socket.socket()
    my_socket.settimeout(5)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 50000)

    try:
        my_socket.connect(server_address)
        # Send data
        my_socket.sendall(numbersjson)

        while True:
            data = my_socket.recv(4096)
            if not data:
                break

            if data:
                print data
                break

        my_socket.close()
        print "Let's do it again!"
        get_input()

    except:
        print 'Something went wrong. Try again later?'
    finally:
        my_socket.close()

print "Let's add 2 numbers!"
get_input()
