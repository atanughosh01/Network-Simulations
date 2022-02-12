#!/usr/bin/env python3.9

"""DHCP Server implementation in python"""

import socket

HOST = "127.0.0.1"      # Standard loopback interface address (localhost)
DHCP_PORT = 54100       # Port to listen on (non-privileged ports are > 1023)
BGP_PORT = 54400


class DHCPServer:
    """DHCP Server class"""

    def __init__(self):
        """Initialize DHCP Server"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.name = ""
        self.msg = ""

    def start_dhcp(self):
        """Start The DHCP Server"""

        print("DHCP Server started!!")
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((HOST, DHCP_PORT))
            print("Listening for a connection on its own port....")
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            print("Connection by : {}".format(addr))
            self.msg = conn.recv(1024).decode("utf-8")
            self.name = conn.recv(1024).decode("utf-8")
            print("{} received from {} named {}".format(self.msg, addr, self.name))
            conn.send(bytes(str(addr), "utf-8"))
            conn.close()
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.connect((HOST, BGP_PORT))
            self.sock.send(bytes("Request to add host to the log!", "utf-8"))
            self.msg = self.sock.recv(1024).decode("utf-8")
            print("Message received : {}".format(self.msg))
            self.sock.send(bytes(self.name, "utf-8"))
            self.msg = self.sock.recv(1024).decode("utf-8")
            print("Message received : {}".format(self.msg))
            self.sock.send(bytes(str(addr), "utf-8"))
            print("{} added to the log!".format(self.name))
            print("DHCP Server still running!")


if __name__ == "__main__":
    dhcp_server = DHCPServer()
    dhcp_server.start_dhcp()
