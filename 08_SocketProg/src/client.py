"""Client Module implemented for communicating to the server as guest/manager"""

import sys
import time
import socket
import getpass
from datetime import datetime

# Manager access command    :   sudo-su-manager
# Manager access password   :   chmon#manager


                    #################################################################
                    #                                                               #
                    #    * 0 - 1023      : well-known ports like 80, 443, etc       #
                    #    * 1024 - 49151  : Registered ports                         #
                    #    * 49152 - 65535 : Dynamic and Private ports                #
                    #                                                               #
                    #################################################################


class Client():
    """Client class with support for guestmode access and managermode access"""

    def __init__(self):
        self.server_host = "127.0.0.1"   #localhost
        self.server_port = "5050"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.admin_password = "chmon#manager"


    def start_client_threads(self):
        """Starts a client thread and connects to the server through threads"""
        name = input("\nEnter your username: ")
        type_of_user = "g"
        symbol = f"\n>>> {name}@Guest__$  "

        ################################################################
        # Each client binds to this localhost and specified port address
        ################################################################
        inp = input("Enter the host and port (WhiteSpace Separated): ")
        host_port = inp.split()

        if(host_port[0] == self.server_host and host_port[1] == self.server_port):
            self.socket.connect(('localhost', 5050))
        else:
            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sys.exit(f"{curr_datetime} || Error!!! Entered Server address is Incorrect!")


        #######################################################################
        # If connected to the correct IP address, receives CONFIRMATION message
        #######################################################################
        welcome_msg = self.socket.recv(1024).decode("utf-8")
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{curr_datetime} || {welcome_msg}")
        time.sleep(0.05)

        self.socket.send(name.encode("utf-8"))
        time.sleep(0.05)
        welcome_msg = self.socket.recv(1024).decode("utf-8")
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"{curr_datetime} || {welcome_msg}")


        #########################################################################
        # Loops untill the user logsout of the system and performs CRUD operation
        #   * Create        * Read        * Update      * Delete
        #########################################################################
        while True:
            if type_of_user.lower() == "m":
                symbol = f"\n>>> {name}@Manager__#  "
            else: symbol = f"\n>>> {name}@Guest__$  "
            user_input = input(symbol)
            user_input = user_input.split()
            length = len(user_input)

            ##################################################################
            # If user requestes for logging out, sends the user details to the
            # server and the loop is exited, the connection is freed
            ##################################################################
            if user_input[0] == "logout":
                self.socket.send(name.encode("utf-8"))
                time.sleep(0.05)
                self.socket.send(type_of_user.encode("utf-8"))
                time.sleep(0.05)
                self.socket.send("logout".encode("utf-8"))
                break

            count = 0       # Counter is for parsing purpose
            while length > count:

                ###########################################################
                # If the type 0f the user is 'GUEST' and the query is 'GET'
                # we need 2 attributes in total, e.g. GET(1) city_name(2)
                ###########################################################
                if(type_of_user == "g" and user_input[count].lower() == "get"):
                    assert length >= count+2, "Invalid input format!"
                    count += 1
                    attribute = user_input[count]
                    count += 1

                    # Sends to the Server
                    self.socket.send(name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("get".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))

                    # Expects an answer from the Server
                    response = self.socket.recv(1024).decode("utf-8")
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || {response}")
                    # print(response)


                #################################################################
                # If the type 0f the user is 'GUEST' and the query is 'PUT'
                # we need 3 attributes in total, e.g. PUT(1) city(2) city_name(3)
                #################################################################
                elif type_of_user == "g" and user_input[count].lower() == "put":
                    assert length >= count+3, "Invalid input format!"
                    count += 1
                    attribute = user_input[count]
                    count += 1
                    value = user_input[count]
                    count += 1

                    # Sends to the Server
                    self.socket.send(name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("put".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(value.encode("utf-8"))

                    # Expects an answer from the Server
                    ans = self.socket.recv(1024).decode("utf-8")
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || {ans}")


                ####################################################################
                # If an user tries to switch from 'GUEST' mode to 'MANAGER' mode
                # a password prompt is shown for 'AUTHENTICATION' purpose and upon
                # valid authentication the loop continues, else warning is displayed
                ####################################################################
                elif type_of_user == "g" and user_input[count].lower() == "sudo-su-manager":
                    password = getpass.getpass(prompt="Enter your manager password: ")
                    if password == self.admin_password:
                        # If password matches the type of user is changed from "GUEST" to 'MANAGER
                        type_of_user = "m"
                        count += 1
                        # Sends to the Server
                        self.socket.send(name.encode("utf-8"))
                        time.sleep(0.05)
                        self.socket.send('g'.encode("utf-8"))
                        time.sleep(0.05)
                        self.socket.send('u'.encode("utf-8"))
                        time.sleep(0.05)
                    elif password == "exit":
                        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{curr_datetime} || Exiting...")
                        break
                    else:
                        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        print(f"{curr_datetime} || You have entered a wrong password !!!")
                        break


                ###########################################################################
                # If the type 0f the user is 'MANAGER' and the query is 'PUT' we
                # need 4 attributes in total, e.g. PUT(1) user_name(2) city(3) city_name(4)
                ###########################################################################
                elif(type_of_user == "m" and user_input[count].lower() == "put"):
                    assert length >= count + 4, "Invalid input format!"
                    count += 1
                    user_name = user_input[count]
                    count += 1
                    attribute = user_input[count]
                    count += 1
                    value = user_input[count]
                    count += 1

                    # Sends to the Server
                    self.socket.send(user_name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("put".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(value.encode("utf-8"))
                    time.sleep(0.05)

                    # Expects an answer from the Server
                    ans = self.socket.recv(1024).decode("utf-8")
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || {ans}")


                ###################################################################
                # If the type 0f the user is 'MANAGER' and the query is 'GET' we
                # need 3 attributes in total, e.g. GET(1) user_name(2) city_name(3)
                ###################################################################
                elif(type_of_user == "m" and user_input[count].lower() == "get"):
                    assert length >= count + 3, "Invalid input format!"
                    count += 1
                    user_name = user_input[count]
                    count += 1
                    attribute = user_input[count]
                    count += 1

                    # Sends to the Server
                    self.socket.send(user_name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("get".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))
                    time.sleep(0.05)

                    # Expects an answer from the Server
                    ans = self.socket.recv(1024).decode("utf-8")
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || {ans}")


                ##################################################
                # In all other cases an error message is displayed
                # and the loop is terminated
                ##################################################
                else:
                    curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    print(f"{curr_datetime} || Invalid input format!")
                    break


# Driver Code
if __name__ == "__main__":
    c = Client()
    c.start_client_threads()
