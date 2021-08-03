import sys
import socket
import packages.CRC as crc
import packages.VRC as vrc
import packages.LRC as lrc
import packages.receiverCheckSum as rcs
from _thread import start_new_thread


def receive_data():

    host = '127.0.0.1'
    port = 2021                                # arbitrary non-privileged port
    ThreadCount = 0
    ReceiverSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ReceiverSideSocket.bind((host, port))
        n = int(input("Enter No. of Sender(s) You Want to Keep Waiting : "))
        max = int(input("Enter Max No. of Senders Allowed to send Request : "))
        ReceiverSideSocket.listen(n)                # queue up to 'n' requests
        print("Socket Has Been Created." + "\Receiver is Now Listening...." +
              "\nWaiting For Sender(s) to Connect....")

    except socket.error as e:
        print("Bind Failed! Error : " + str(sys.exc_info()))
        print("Exception Caught : " + str(e))
        ReceiverSideSocket.close()
        sys.exit()

    except ValueError as v:
        print("Exception Caught : " + str(v))
        print("Receiver Has Been Terminated." +
              "\nEnter Integer Only From Next Time.")
        ReceiverSideSocket.close()
        sys.exit()

    while ThreadCount <= max:
        Sender, address = ReceiverSideSocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("\nConnected to : " + ip + ':' + port)
        start_new_thread(Sender_thread, (Sender, ))
        ThreadCount += 1
        print("Thread Number = Sender Number : " + str(ThreadCount))

    # ReceiverSideSocket.close()
    print(f"\nMore Than ({max}) Senders aren't allowed to send request(s).")
    print("Receiver has been closed.")


def Sender_thread(connection):
    connection.send(str.encode("Receiver is Working : "))
    while True:
        Sender_request = connection.recv(2048)
        Receiver_data, choice = [str(i) for i in Sender_request.decode("utf-8").split("\n")]
        print(Receiver_data)
        print(choice)

        if choice == '1':
            vrc_data = vrc.gen_VRC(Receiver_data)
            if vrc_data == '0':
                Receiver_response = "Error Checking Complete\nNo Error found in Receiver-data"
            else:
                Receiver_response = "Error Checking Complete\nError found in Receiver-data"
            connection.sendall(str.encode(Receiver_response))

        elif choice == '2':
            lrc_data = lrc.gen_LRC(Receiver_data)
            if lrc_data == '0':
                Receiver_response = "Error Checking Complete\nNo Error found in Receiver-data"
            else:
                Receiver_response = "Error Checking Complete\nError found in Receiver-data"
            connection.sendall(str.encode(Receiver_response))

        elif choice == '3':
            packet_count = 5
            packet_length = int(len(Receiver_data)/packet_count)
            receiver_check_sum = rcs.gen_CheckSum(Receiver_data, packet_length)
            connection.sendall(str.encode(receiver_check_sum))

        elif choice == '4':
            key = input("Enter key for calculating CRC \n(Must be same as Sender's Key to get authentic results) : ")
            crc_data = crc.gen_CRC(Receiver_data, key)
            Receiver_response = crc_data
            connection.sendall(str.encode(Receiver_response))
    # connection.close()


def main():
    receive_data()


if __name__ == "__main__":
    main()
