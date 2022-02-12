"""Multithreaded server for listening to clients and sending appropriate responses"""

import socket
from threading import Thread
from datetime import datetime


class Server:
    """Server Class to listen to multiple client over threads"""

    def __init__(self):
        self.server_host = "127.0.0.1"   #localhost
        self.sever_port = "5050"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.auth_dict = {} # stores the username and their count as K-V pair
        self.key_val = {} # stores username and (dict of attributes and values) as K-V pair


    def start_thread(self, conn, addr, name):
        """Accepts each client connections via threads from the threadpool"""
        thread = Thread(target=self.synchronize_clients, args=(conn, addr, name))
        thread.start()
        thread.join()


    def synchronize_clients(self, conn, addr, user_name):
        """Accepts client requests and sends responses based on them"""
        while True:
            name = conn.recv(1024).decode("utf-8")
            type_of_user = conn.recv(1024).decode("utf-8")
            type_of_operation = conn.recv(1024).decode("utf-8")


            ###########################################################
            # If the type 0f the user is 'GUEST' and the query is 'GET'
            # we need 2 attributes in total, e.g. GET(1) city_name(2)
            ###########################################################
            if(type_of_user == "g" and type_of_operation == "get"):
                attribute = conn.recv(1024).decode("utf-8")

                # Name should be equal to sent userName
                if name != user_name:
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || ", end=" ")
                    conn.send("Access Denied! You need Manager privilage for this!".encode("utf-8"))
                else:
                    user_data = self.key_val.get(name, "null")
                    if user_data == "null": # Means the user's attribute is not in key-val dict
                        self.key_val[name] = {}
                        response = "\n"     # Prints a blank line in client
                        conn.send(response.encode("utf-8"))
                    else:
                        result = user_data.get(attribute,"null")
                        response = result if result != "null" else "\n"
                        conn.send(response.encode("utf-8"))


            #################################################################
            # If the type 0f the user is 'GUEST' and the query is 'PUT'
            # we need 3 attributes in total, e.g. PUT(1) city(2) city_name(3)
            #################################################################
            elif type_of_user == "g" and type_of_operation == "put":
                attribute = conn.recv(1024).decode("utf-8")
                value = conn.recv(1024).decode("utf-8")
                if name != user_name:
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || ", end=" ")
                    conn.send("Access Denied! You need Manager privilage for this!".encode("utf-8"))
                else:
                    user_data = self.key_val.get(name, "null")
                    if user_data == "null":  # Means the user's attribute is not in key-val dict
                        self.key_val[name] = {}

                    self.key_val[name][attribute] = value
                    conn.send("Data added successfully!".encode("utf-8"))


            ########################################################################
            # If an user tries to switch from 'GUEST' mode to 'MANAGER' mode a
            # password prompt is shown for 'AUTHENTICATION' purpose and upon valid
            # authentication user is given manager access, else warning is displayed
            ########################################################################
            elif(type_of_user == "g" and type_of_operation == "u"):
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("---------------------------------------------------------------")
                print(f"{curr_datetime} || {name} now has manager privillages!")
                print("---------------------------------------------------------------")
                type_of_user = "m"


            ###########################################################################
            # If the type 0f the user is 'MANAGER' and the query is 'PUT' we
            # need 4 attributes in total, e.g. PUT(1) user_name(2) city(3) city_name(4)
            ###########################################################################
            elif(type_of_user == "m" and type_of_operation == "put"):
                attribute = conn.recv(1024).decode("utf-8")
                value = conn.recv(1024).decode("utf-8")
                user_data = self.key_val.get(name, "null")
                if user_data == "null":     # Means the user's attribute is not in key-val dict
                    self.key_val[name] = {}

                self.key_val[name][attribute] = value
                conn.send("Data added successfully!".encode("utf-8"))


            ###################################################################
            # If the type 0f the user is 'MANAGER' and the query is 'GET' we
            # need 3 attributes in total, e.g. GET(1) user_name(2) city_name(3)
            ###################################################################
            elif(type_of_user == "m" and type_of_operation == "get"):
                attribute = conn.recv(1024).decode("utf-8")
                user_data = self.key_val.get(name, "null")
                if user_data == "null":       # Means the user's attribute is not in key-val dict
                    self.key_val[name] = {}
                    response = "\n"           # Prints a blank line in client
                    conn.send(response.encode("utf-8"))
                else:
                    result = user_data.get(attribute,"null")
                    response = result if result != "null" else "\n"
                    conn.send(response.encode("utf-8"))


            #########################################################
            # If user requestes for logging out, server gets the user
            # details and the loop is exited, the connection is freed
            #########################################################
            elif type_of_operation == "logout":
                conn.close()
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print(f"{curr_datetime} || ", end=" ")
                print(f"{name} [ IP => {addr[0]}:{addr[1]} ] has logged out from the server!!")
                print("---------------------------------------------------------------")
                break


    def run(self):
        """Run the server"""
        self.socket.bind(("localhost", 5050))
        self.socket.listen(10)
        print("\n\t+-----------------------------------------------------------------+")
        print("\t|    The server is running on host 127.0.0.1 and port 5050 !!     |")
        print("\t+-----------------------------------------------------------------+\n")
        thread_pool = []
        while True:
            conn, addr = self.socket.accept()
            conn.send("Welcome to the server !!".encode("utf-8"))
            name = conn.recv(1024).decode("utf-8")

            # Means if any new user logs in to the server
            if self.auth_dict.get(name, 0) == 0:
                self.auth_dict[name] = 1
                conn.send("Registration successful!".encode("utf-8"))
            # Means if any pre-existing user logs in again after logging out
            else:
                conn.send(f"Welcome back {name} !!!".encode("utf-8"))

            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{curr_datetime} || {name} has logged into the server!! ")
            print("---------------------------------------------------------------")
            thread = Thread(target=self.synchronize_clients, args=(conn, addr, name))
            thread_pool.append(thread)
            thread.start()

        # for thread in thread_pool:
        #     thread.join()

# Driver Code
if __name__ == "__main__":
    server = Server()
    server.run()
