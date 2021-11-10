#!/usr/bin/env python3.9

"""DHCP Server implementation in python"""

import socket

DHCP_HOST = "127.0.0.1"
OWN_PORT = 54100
BGP_PORT = 54400


class DHCPServer:
    """DHCP Server class"""

    def __init__(self):
        """Initialize DHCP Server"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.bind((DHCP_HOST, OWN_PORT))

    def start_dhcp(self):
        """Start The DHCP Server"""

        print("DHCP Server started!!")
        while True:
            self.sock.bind((DHCP_HOST, OWN_PORT))
            print("Listening for a connection on its own port....")
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            print("Connection by: ", addr)
            self.msg 
