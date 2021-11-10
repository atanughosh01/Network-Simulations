#!/usr/bin/env python3.9

"""FTP Server implementation in python"""

import socket

HOST = "127.0.0.1"      # Standard loopback interface address (localhost)
FTP_PORT = 54200        # Port to listen on (non-privileged ports are > 1023)


class FTPServer:
    """FTP Server class"""

    def __init__(self):
        """Initialize FTP Server"""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.file_name = ""
        self.name = ""
        self.data = ""

    def start_ftp(self):
        """Start The FTP Server"""

        print("FTP Server started!!")
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((HOST, FTP_PORT))
            print("Listening for a connection on its own port....")
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            self.name = conn.recv(1024).decode("utf-8")
            self.file_name = conn.recv(1024).decode("utf-8")
            print("{} with address {}'s requesting file {}".format(self.name, addr, self.file_name))
            with open(self.file_name, "r", encoding="utf-8") as fptr:
                self.data = fptr.read()
            conn.send(bytes(self.data, "utf-8"))
            print("File sent successfully")
            conn.close()
            self.sock.close()
            print("FTP Server still running!")


if __name__ == "__main__":
    ftp_server = FTPServer()
    ftp_server.start_ftp()
