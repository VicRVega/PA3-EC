#!env python

"""Chat server for CST311 Programming Assignment 3 - Extra Credit"""
__author__ = "[Group 4]"
__credits__ = [
    "Chris Tangonan",
    "Edward Torres",
    "Victoria Ramirez",
    "Guillermo Zendejas"
]


import socket as s
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000
connection_socketX = None
connection_socketY = None
usernameX = None
usernameY = None
offline_for_X = []
offline_for_Y = []

def connection_handler(connection_socket, address):
    global connection_socketX, connection_socketY, usernameX, usernameY
    global offline_for_X, offline_for_Y

    #receive username from client
    username = connection_socket.recv(1024).decode()

    #check if client x or client y and add username
    if connection_socketX is None:
        usernameX = username
        #connection_socketX = connection_socket
        log.info(f"Username set for Client X: {usernameX}")

        #check for offline message for client x
        if offline_for_X:
            for message in offline_for_X:
                connection_socketX.send(message.encode())
            offline_for_X.clear() #clear once have been sent
    else:
        usernameY = username
        #connection_socketY = connection_socket
        log.info(f"Username set for Client Y: {usernameY}")
        #check for offline messages for other client
        if offline_for_Y:
            for message in offline_for_Y:
                connection_socketY.send(message.encode())
            offline_for_Y.clear() #clear once messages have been sent

    while True:
        try:
            #  Read data from the new connection socket
            #  Note: if no data has been sent this blocks until there is data
            incoming_message = connection_socket.recv(1024).decode()


            #if message is bye send it before closing
            if 'bye' in incoming_message:
                bye_message = f"{username} has left the chat."

                #forwared message "bye" before closing connection
                if connection_socket == connection_socketX and connection_socketY:
                    connection_socketY.send(bye_message.encode())
                elif connection_socket == connection_socketY and connection_socketX:
                    connection_socketX.send(bye_message.encode())
                break

            # Log query information including username
            log.info(f"Received message from {username}: {incoming_message}")

            # Forward message to the other client while storing offline messages
            if connection_socket == connection_socketX:
                if connection_socketY:
                    connection_socketY.send(incoming_message.encode())
                else:
                    offline_for_Y.append(incoming_message)
                    log.info(f"Stored offline message for {usernameY}")
            elif connection_socket == connection_socketY:
                if connection_socketX:
                    connection_socketX.send(incoming_message.encode())
                else:
                    offline_for_X.append(incoming_message)
                    log.info(f"Stored offline message for {usernameX}")
        except:
            break

    # Close client socket
    connection_socket.close()

def main():
    global connection_socketX, connection_socketY

    # Create a TCP socket
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)

    # Assign port number to socket, and bind to chosen port
    server_socket.bind(('',server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(2)

    # Alert user we are now online
    log.info("The server is ready to receive on port " + str(server_port))

    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Enter forever loop to listen for requests
        # When each client connects, create references to their respective sockets and addresses
        connection_socketX, addressX = server_socket.accept()
        log.info(f"Connected to Client X at {str(addressX)}")
        # implementation of threading for each client
        threading.Thread(target=connection_handler, args=(connection_socketX, addressX)).start()

        connection_socketY, addressY = server_socket.accept()
        log.info(f"Connected to Client Y at {str(addressY)}")
        # implementation of threading for each client
        threading.Thread(target=connection_handler, args=(connection_socketY, addressY)).start()

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()