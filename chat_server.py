#!env python

"""Chat server for CST311 Programming Assignment 3"""
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
clientXName = "Client X"
clientYName = "Client Y"
connection_socketX = None
connection_socketY = None

def connection_handler(connection_socket, address):
    global connection_socketX, connection_socketY

    while True:
        # Read data from the new connection socket
        incoming_message = connection_socket.recv(1024)

        # Determine if the sender is Client X or Client Y
        if connection_socket == connection_socketX:
            sender_name = clientXName
            receiver_socket = connection_socketY
        else:
            sender_name = clientYName
            receiver_socket = connection_socketX

        # Decode data from UTF-8 bytestream
        incoming_decoded = sender_name + ": " + incoming_message.decode()
        if incoming_decoded == sender_name + ": " + 'bye':
            break

        # Log message information
        log.info(f"Received message: '{incoming_decoded}' from: {str(address)}")

        # Forward the message to the other client
        if receiver_socket:
            receiver_socket.send(incoming_decoded.encode())

    # Close client socket
    connection_socket.close()


def main():
    global connection_socketX, connection_socketY

    # Create a TCP socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Bind the socket to the port
    server_socket.bind(('', server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(2)

    log.info(f"The server is ready to receive on port {server_port}")

    try:
        # Wait for two clients to connect
        connection_socketX, addressX = server_socket.accept()
        log.info(f"Connected to Client X at {str(addressX)}")

        connection_socketY, addressY = server_socket.accept()
        log.info(f"Connected to Client Y at {str(addressY)}")

        # Start a thread for each client
        threading.Thread(target=connection_handler, args=(connection_socketX, addressX)).start()
        threading.Thread(target=connection_handler, args=(connection_socketY, addressY)).start()

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()