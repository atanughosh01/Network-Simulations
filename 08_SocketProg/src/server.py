"""Multithreaded server for listening to clients and send appropriate responses"""

# import sys
# import time
import socket
from threading import Thread


class Server:
    """Server Class to listen to multiple client over threads"""

    def __init__(self):
        self.server_host = "127.0.0.1"
        self.sever_port = "8000"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.auth_dict = {}
        self.key_val = {}


    def start_thread(self, conn, addr, name):
        """Accepts each client connections via threads from the threadpool"""
        thread = Thread(target=self.handle_clients, args=(conn, addr, name))
        thread.start()
        thread.join()


    def handle_clients(self, conn, addr, user_name):
        """Accepts client requests and sends responses based on them"""
        while True:
            name = conn.recv(1024).decode("utf-8")
            type_of_user = conn.recv(1024).decode("utf-8")
            type_of_operation = conn.recv(1024).decode("utf-8")

            if(type_of_user == "g" and type_of_operation == "get"):
                attribute = conn.recv(1024).decode("utf-8")
                if name != user_name:
                    conn.send("Access Denied! You need Manager privilage for this!".encode("utf-8"))
                else:
                    user_data = self.key_val.get(name, "null")
                    if user_data == "null":
                        self.key_val[name] = []
                        response = "\n"
                        conn.send(response.encode("utf-8"))
                    else:
                        result = user_data.get(attribute,"null")
                        response = result if result != "null" else "\n"
                        conn.send(response.encode("utf-8"))

            elif type_of_user == "g" and type_of_operation == "put":
                attribute = conn.recv(1024).decode("utf-8")
                value = conn.recv(1024).decode("utf-8")
                if name != user_name:
                    conn.send("Sorry! You need manager privilages for doing this!".encode("utf-8"))
                else:
                    user_data = self.key_val.get(name, "null")
                    if user_data == "null":
                        self.key_val[name] = {}

                    self.key_val[name][attribute] = value
                    conn.send('Data added successfully!'.encode("utf-8"))

            elif(type_of_user == "g" and type_of_operation == "u"):
                print("------------------------------------------------")
                print(f"{name} now has manager privillages!")
                print("------------------------------------------------")
                type_of_user = "m"

            elif(type_of_user == "m" and type_of_operation == "put"):
                attribute = conn.recv(1024).decode("utf-8")
                value = conn.recv(1024).decode("utf-8")
                user_data = self.key_val.get(name, "null")
                if user_data == "null":
                    self.key_val[name] = {}

                self.key_val[name][attribute] = value
                conn.send('Data added successfully!'.encode("utf-8"))

            elif(type_of_user == "m" and type_of_operation == "get"):
                attribute = conn.recv(1024).decode("utf-8")
                user_data = self.key_val.get(name, "null")
                if user_data == "null":
                    self.key_val[name] = {}
                    response = "\n"
                    conn.send(response.encode("utf-8"))
                else:
                    result = user_data.get(attribute,"null")
                    response = result if result != "null" else "\n"
                    conn.send(response.encode("utf-8"))

            elif type_of_operation == "end":
                conn.close()
                print(addr)
                print(f"{name} has logged out from the server")
                print("-------------------------------------------------------------------------")
                break


    def run(self):
        """Run the server"""
        self.socket.bind(('localhost', 8000))
        self.socket.listen(10)
        print("The server is running on 127.0.0.1 and port 8000!")
        print("-------------------------------------------------------------------------")
        thread_pool = []
        while True:
            conn , addr = self.socket.accept()
            conn.send("Welcome to the server!".encode("utf-8"))
            name = conn.recv(1024).decode("utf-8")

            if self.auth_dict.get(name, 0) == 0:
                self.auth_dict[name] = 1
                conn.send("Registration successful!".encode("utf-8"))
            else:
                conn.send("Welcome back!".encode("utf-8"))
            print(f"{name} has logged into the server!! ")
            print("-------------------------------------------------------------------------")
            thread = Thread(target=self.handle_clients, args=(conn, addr, name))
            thread_pool.append(thread)
            thread.start()

        # for thread in thread_pool:
        #     thread.join()


if __name__ == "__main__":
    server = Server()
    server.run()
