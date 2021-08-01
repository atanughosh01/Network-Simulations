""" Implement one multi-threaded server with socket programming in python. """

# import required pacakges / modules
import sys
import socket
from _thread import start_new_thread


def start_server():

    host = '127.0.0.1'
    port = 2021                         # arbitrary non-privileged port
    ThreadCount = 0
    ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ServerSideSocket.bind((host, port))
        n = int(input("Enter No. of Client(s) You Want to Keep Waiting : "))
        max = int(input("Enter Max No. of Clients Allowed to send Request : "))
        ServerSideSocket.listen(n)      # queue up to 'n' requests
        print("Socket Has Been Created." + "\nServer is Now Listening...." +
              "\nWaiting For Client(s) to Connect....")

    except socket.error as e:
        print("Bind Failed! Error : " + str(sys.exc_info()))
        print("Exception Caught : " + str(e))
        ServerSideSocket.close()
        sys.exit()

    except ValueError as v:
        print("Exception Caught : " + str(v))
        print("Server Has Been Terminated." +
              "\nEnter Integer Only From Next Time.")
        ServerSideSocket.close()
        sys.exit()

    while ThreadCount <= max:
        client, address = ServerSideSocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("\nConnected to : " + ip + ':' + port)
        start_new_thread(client_thread, (client, ))
        ThreadCount += 1
        print("Thread Number = Client Number : " + str(ThreadCount))

    # ServerSideSocket.close()
    print(f"\nMore Than ({max}) Clients Can't Send Request(s).")
    print("Server Has Been Closed.")


def client_thread(connection):
    connection.send(str.encode("Server is Working : "))
    while True:
        client_request = connection.recv(2048)
        response = "Server Response : " + client_request.decode('utf-8')
        if not client_request:
            break
        connection.sendall(str.encode(response))
    connection.close()


def main():
    start_server()


if __name__ == "__main__":
    main()
