#!/usr/bin/env python3.9

"""Host for connecting to the servers"""

import socket

HOST = "127.0.0.1"      # Standard loopback interface address (localhost)
BGP_PORT = 54400        # Port to listen on (non-privileged ports are > 1023)
DHCP_PORT = 54100
FTP_PORT = 54200


class Host:
    """Host Class for implementing connections"""

    def __init__(self):
        "Initialize The Hosts"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.own_address = ""
        self.file_name = ""
        self.receiver = ""
        self.name = ""
        self.data = ""
        self.msg = ""

    def connect_hosts(self):
        """Connects The Hosts To Specific Servers"""

        print("Host started!!")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((HOST, DHCP_PORT))
        self.sock.send(bytes("Requesting port number of the host!!", "utf-8"))
        self.name = input("Enter the name of the host : ")
        self.sock.send(bytes(self.name, "utf-8"))
        self.own_address = self.sock.recv(1024).decode("utf-8")
        print("The host address : {}".format(self.own_address))
        self.sock.close()

        while True:

            print("\n")
            print("+---------------------------------------------+")
            print("|    You want to >>                           |")
            print("|    1. Request file from FTP server          |")
            print("|    2. Send a msg to another HOST            |")
            print("|    3. Receive a msg from another HOST       |")
            print("|    4. Exit!!!!                              |")
            print("+---------------------------------------------+")
            choice = input("Enter Your Choice (1/2/3/4) : ")
            print("\n")

            if choice == "1":
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.connect((HOST, FTP_PORT))
                self.sock.send(bytes(self.name, "utf-8"))
                self.file_name = input("Enter filename to be searched : ")
                self.sock.send(bytes(self.file_name, "utf-8"))
                self.data = self.sock.recv(1024).decode("utf-8")
                print("The contents of the file : {}".format(self.data))
                self.sock.close()
                continue

            if choice == "2":
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.connect((HOST, BGP_PORT))
                self.sock.send(bytes("Requesting file transfer to another host!", "utf-8"))
                self.msg = self.sock.recv(1024).decode("utf-8")
                print("Message received : {}".format(self.msg))
                self.receiver = input("Enter name of receiver : ")
                self.sock.send(bytes(self.receiver, "utf-8"))
                self.data = input("Enter data to be transferred : ")
                self.sock.send(bytes(self.data, "utf-8"))
                self.sock.close()
                continue

            if choice == "3":
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.sock.bind((HOST, int(self.own_address[13:-2])))
                self.sock.listen(5)
                print("Listening for a connection on its own port....")
                conn, addr = self.sock.accept()
                print("Connection established!!")
                print("Connected to address : {}".format(addr))
                self.msg = conn.recv(1024).decode("utf-8")
                print("Message received : {}".format(self.msg))
                conn.send(bytes("Request granted! Send data!", "utf-8"))
                self.data = conn.recv(1024).decode("utf-8")
                print("Data received : {}".format(self.data))
                print("Transmission successful!")
                conn.close()
                self.sock.close()
                continue

            if choice == "4":
                print("Host has been terminated!")
                break

            if choice not in ["1", "2", "3", "4"]:
                print("Invalid choice! Reselect 1/2/3/4.")
                continue


if __name__ == "__main__":
    host = Host()
    host.connect_hosts()
