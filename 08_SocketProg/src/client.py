"""Client Module implemented for communicating to the server as guest/manager"""

import sys
import time
import socket
import getpass


class Client():
    """Client class with support for guestmode access and managermode access"""

    def __init__(self):
        self.server_host = "127.0.0.1"
        self.server_port = "8000"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.admin_password = 'changeadmin'


    def start_client_thread(self):
        """Starts a client thread and connects to the server through threads"""

        name = input("Enter your name: ")
        type_of_user = "g"      # guest user
        symbol = "Guest$  "

        inp = input("Enter the host and port (WhiteSpace Separated): ")
        host_port = inp.split()

        if(host_port[0] == self.server_host and host_port[1] == self.server_port):
            self.socket.connect(('localhost', 8000))
        else: sys.exit("Entered Server address is Incorrect !!!")

        welcome_msg = self.socket.recv(1024).decode("utf-8")
        print(welcome_msg)
        time.sleep(0.05)

        self.socket.send(name.encode("utf-8"))
        time.sleep(0.05)
        welcome_msg = self.socket.recv(1024).decode("utf-8")
        print(welcome_msg)

        while True:
            if type_of_user.lower() == "m":
                symbol = "Manager#  "
            else: symbol = "Guest$  "
            user_input = input(symbol)
            user_input = user_input.split()
            length = len(user_input)

            if user_input[0] == "end":
                self.socket.send(name.encode("utf-8"))
                time.sleep(0.05)
                self.socket.send(type_of_user.encode("utf-8"))
                time.sleep(0.05)
                self.socket.send("end".encode("utf-8"))
                break

            count = 0

            while length > count:

                if(type_of_user == "g" and user_input[count].lower() == "get"):
                    assert length >= count+2, "Invalid input format!"
                    count += 1
                    attribute = user_input[count]
                    count += 1

                    self.socket.send(name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("get".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))

                    response = self.socket.recv(1024).decode("utf-8")
                    print(response)

                elif type_of_user == "g" and user_input[count].lower() == "put":
                    assert length >= count+3, "Invalid input format!"
                    count += 1
                    attribute = user_input[count]
                    count += 1
                    value = user_input[count]
                    count += 1

                    #send to server
                    self.socket.send(name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("put".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(value.encode("utf-8"))

                    ans = self.socket.recv(1024).decode("utf-8")
                    print(ans)

                elif type_of_user == "g" and user_input[count].lower() == "makemanager":
                    password = getpass.getpass(prompt="Enter your manager password: ")

                    if password == self.admin_password:
                        type_of_user = "m"
                        count += 1
                        self.socket.send(name.encode("utf-8"))
                        time.sleep(0.05)
                        self.socket.send('g'.encode("utf-8"))
                        time.sleep(0.05)
                        self.socket.send('u'.encode("utf-8"))
                        time.sleep(0.05)

                    elif password == "exit":
                        print("Exiting...")
                        break

                    else: print("You have entered a wrong password !!!")


                elif(type_of_user == "m" and user_input[count].lower() == "put"):
                    assert length >= count + 4, "Invalid input format!"
                    count += 1
                    user_name = user_input[count]
                    count += 1
                    attribute = user_input[count]
                    count += 1
                    value = user_input[count]
                    count += 1
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

                    ans = self.socket.recv(1024).decode("utf-8")
                    print(ans)

                elif(type_of_user == "m" and user_input[count].lower() == "get"):
                    assert length >= count + 3, "Invalid input format!"
                    count += 1
                    user_name = user_input[count]
                    count += 1
                    attribute = user_input[count]
                    count += 1

                    self.socket.send(user_name.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(type_of_user.encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send("get".encode("utf-8"))
                    time.sleep(0.05)
                    self.socket.send(attribute.encode("utf-8"))
                    time.sleep(0.05)

                    ans = self.socket.recv(1024).decode("utf-8")
                    print(ans)

                else:
                    print("Invalid input format!")
                    break


if __name__ == "__main__":
    c = Client()
    c.start_client_thread()
