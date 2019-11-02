"""
 # Author: Adrian Saul Reiban
 # Date: 23/08/2019
"""

import socket
import threading
import logging


class Tello:

    # Configure a logging level
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Tello class constructor
    def __init__(self, name_drone, drone_address, computer_port):
        # Set the name of the Tello drone
        self.name_drone = name_drone

        # Set the Tello ip address and set your comunication port
        self.tello_address = (drone_address, 8889)

        # Set the address and port of your local computer
        self.local_address = ('', computer_port)

        # UDP Connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind to local direction and port
        self.sock.bind(self.local_address)

        # Save Tello's response based on the command sent
        self.response = None

        # Create an execution thread that calls the receive function, so that it runs in the background
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    # This function is responsible for sending data to Tello EDU
    def send(self, command):
        # Try to send the message, otherwise the exception is printed
        try:
            self.sock.sendto(command.encode(), self.tello_address)
            logging.info("Sending message to %s: " % self.name_drone + command)
        except Exception as e:
            logging.error("Error sending message to %s: " % self.name_drone + str(e), exc_info=True)

    # This function is responsible for receiving data from Tello EDU
    def receive(self):
        while True:
            # Try to send the message, otherwise the exception is printed
            try:
                response, drone_address = self.sock.recvfrom(128)
                self.response = response.decode(encoding='utf-8')
                logging.debug("Message received from %s: " % self.name_drone + self.response)
            except Exception as e:
                # If there is an error, the socket is closed
                self.sock.close()
                logging.error("Error in receiving the %s message: " % self.name_drone + str(e), exc_info=True)

    # This function close the communication socket
    def close_sockets(self):
        self.sock.close()
        logging.info("Communication with %s closed" % self.name_drone)

    def __str__(self):
        return ("\n\rThe drone data are: " +
                "\n\t* Name of drone: %s" % self.name_drone +
                "\n\t* IP address and port: IP: %s Port: %s " % self.tello_address + "\n")

