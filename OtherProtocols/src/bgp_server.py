#!/usr/bin/env python3.9

"""BGP Server implementation in python"""

import socket

HOST = "127.0.0.1"      # Standard loopback interface address (localhost)
BGP_PORT = 54400        # Port to listen on (non-privileged ports are > 1023)


class BGPServer:
    """BGP Server class"""

    def __init__(self):
        """Initialize BGP Server"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.address = ""
        self.name = ""
        self.data = ""
        self.msg = ""
        self.log = {}

    def start_bgp(self):
        """Start The BGP Server"""

        print("BGP Server started!!")
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((HOST, BGP_PORT))
            print("Listening for a connection on its own port....")
            self.sock.listen(1)
            conn, addr = self.sock.accept()
            self.msg = conn.recv(1024).decode("utf-8")

            if self.msg == "Request to add host to the log!":
                conn.send(bytes("Request granted! Send host name!", "utf-8"))
                self.name = conn.recv(1024).decode("utf-8")
                conn.send(bytes("Send address!", "utf-8"))
                self.address = conn.recv(1024).decode("utf-8")
                self.log[self.name] = self.address
                conn.close()
                self.sock.close()
                print("The server log now : ", end="")
                print(self.log)
                print("BGP Server is still running!")

            else:
                conn.send(bytes("Request granted! Send host name!", "utf-8"))
                self.name = conn.recv(1024).decode("utf-8")
                conn.send(bytes("Send data to be transferred!", "utf-8"))
                self.data = conn.recv(1024).decode("utf-8")
                conn.close()
                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                addr = self.log[self.name]
                self.sock.connect((HOST, int(addr[13:-2])))
                self.sock.send(bytes("Requesting data transfer by {}".format(self.name), "utf-8"))
                self.msg = self.sock.recv(1024).decode("utf-8")
                print("Message received : {}".format(self.msg))
                self.sock.send(bytes(self.data, "utf-8"))
                self.sock.close()
                print("BGP Server still running!")


if __name__ == "__main__":
    bgp_server = BGPServer()
    bgp_server.start_bgp()
