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

# list of available servers
server_addresses = [
    ['localhost', ('localhost', 50000)],
    ['bluebox vm', ('67.214.217.209', 50000)]  # 67.214.217.209 # block647049-vxq.blueboxgrid.com
]

SERVER_ADDRESS = server_addresses[0][1]
SERVER_CHOSEN = False


def is_number(s):
    """basic guardian to verify numeric input"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_input():
    """Get user input for numbers and server choice"""

    # We will be manipulating these globals based on user input.
    global SERVER_CHOSEN
    global SERVER_ADDRESS

    # Allow the user to choose the server.
    if SERVER_CHOSEN == False:
        while True:
            message = 'Which server would you like to use? \n\
Please type the number of the server you want to use. Your options are: \n'
            i = 0
            for addr in server_addresses:
                message += str(i) + ') ' + str(addr[0]) + '\n'
                i += 1

            chosen_server = raw_input(message)

            if is_number(chosen_server):
                chosen_server = int(chosen_server)
                if 0 <= chosen_server < len(server_addresses):
                    SERVER_ADDRESS = server_addresses[chosen_server][1]
                    SERVER_CHOSEN = True
                    print str(server_addresses[chosen_server][0]) + ' chosen.\n'
                    break
                else:
                    print 'Invalid choice. Try again! \n\n'
            else:
                print 'Please type the number of the server you want to use.'

    print "--------------------------------------------------------------------------------\n"

    # Get the first number, verify it's a number before moving on.
    while True:
        num1 = raw_input('One number please: ')
        if is_number(num1):
            break
        else:
            print 'Hmm, looks like you didn\'t enter a number. Try again.'

    # Get the second number, verify it's a number before moving on.
    while True:
        num2 = raw_input('Another number please: ')
        if is_number(num2):
            break
        else:
            print 'Hmm, looks like you didn\'t enter a number. Try again.'

    # get that result!
    get_result(num1, num2)


def get_result(num1, num2):
    "Send num1 and num2 to the server and return the result"

    # save number pair
    numbers = (num1, num2)

    # generate json object
    numbersjson = json.dumps(numbers)

    # Create a TCP/IP socket
    my_socket = socket.socket()
    my_socket.settimeout(5)

    # Connect the socket to the port where the server is listening
    try:
        my_socket.connect(SERVER_ADDRESS)
        # Send data
        my_socket.sendall(numbersjson)

        while True:
            data = my_socket.recv(4096)
            if not data:
                break

            if data:
                print '\n\n' + str(data) + '\n\n'
                break

        my_socket.close()
        print "Let's do it again!"
        get_input()

    except:
        print 'Something went wrong. Try again later?'
    finally:
        my_socket.close()

print """

 ######  ##     ## ##     ##     ######  ##       #### ######## ##    ## ########
##    ## ##     ## ###   ###    ##    ## ##        ##  ##       ###   ##    ##
##       ##     ## #### ####    ##       ##        ##  ##       ####  ##    ##
 ######  ##     ## ## ### ##    ##       ##        ##  ######   ## ## ##    ##
      ## ##     ## ##     ##    ##       ##        ##  ##       ##  ####    ##
##    ## ##     ## ##     ##    ##    ## ##        ##  ##       ##   ###    ##
 ######   #######  ##     ##     ######  ######## #### ######## ##    ##    ##

This program adds 2 numbers using sockets!

"""

get_input()
