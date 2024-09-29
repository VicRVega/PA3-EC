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
import time
import threading

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000
thread_list = []
connections = []
clientXName = "Client X"
clientYName = "Client Y"
connection_socketX = None
connection_socketY = None
addresses = []

def connection_handler(connection_socket, address):
    global connection_socketX, connection_socketY, clientXName, clientYName

    username = connection_socket.recv(1024).decode()

    if connection_socket == connection_socketX:
        clientXName = username
    else:
        clientYName = username

    log.info("f{username connected from {address}")

    while True:
        #  Read data from the new connection socket
        #  Note: if no data has been sent this blocks until there is data
        incoming_message = connection_socket.recv(1024)

        # Creating local references for the other client's socket and string name
        otherClientSocket, otherClientName = (connection_socketX, clientXName) if address[0] == "10.0.0.3" else (connection_socketY, clientYName)

        # Decode data from UTF-8 bytestream
        incoming_decoded = otherClientName + ": " + incoming_message.decode()
        if incoming_decoded == otherClientName + ": " + 'bye':
            break

        # Log query information
        log.info("Received query test \"" + str(incoming_decoded) + "\"" + "from: " + str(address))


        # # Perform some server operations on data to generate response
        # # time.sleep(10)
        # response = query_decoded.upper()

        log.info("Other socket is: \nconnection_socket: " + str(otherClientSocket))

        forwarded_message = incoming_decoded.encode()

        # Sent response over the network, encoding to UTF-8
        otherClientSocket.send(forwarded_message)

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
        while True:
            # When each client connects, create references to their respective sockets and addresses
            connection_socketX, addressX = server_socket.accept()
            log.info("Connected to " + str(addressX) + "\nconnection_socket: " + str(connection_socketX))

            connection_socketY, addressY = server_socket.accept()
            log.info("Connected to " + str(addressY) + "\nconnection_socket: " + str(connection_socketY))

            # TODO: Determine if address has already visited server

            # implementation of threading for each client
            threading.Thread(target=connection_handler, args=(connection_socketX, addressX)).start()
            threading.Thread(target=connection_handler, args=(connection_socketY, addressY)).start()

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()