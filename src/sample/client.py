""" Implement one multi-threaded server with socket programming in python. """

# import required pacakges / modules
import sys
import socket


def start_clients():
    host = '127.0.0.1'
    port = 2021
    ClientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ClientSideSocket.connect((host, port))
    except socket.error as e:
        print("Server is Currently Inactive. Connection Failed!\n\nError : " +
              str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

    print("Server is Currently Active.\nSend Client-Request to Get Response Fom Server.")

    server_response = ClientSideSocket.recv(1024)

    while True:
        request = input("\nClient Request (Enter 0 to Exit) : ")
        if request == '0':
            ClientSideSocket.close()
            print("\nConnection Has Been Closed.\nClient Has Exited.")
            sys.exit()

        try:
            ClientSideSocket.sendall(request.encode("utf-8"))
            server_response = ClientSideSocket.recv(1024)
            print(server_response.decode("utf-8"))

        except Exception as e:
            print("Exception Caught : " + str(e))
            print("Server Has Been Closed.")
            ClientSideSocket.close()
            sys.exit()


def main():
    start_clients()


if __name__ == "__main__":
    main()
