import sys
import socket
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
from _thread import start_new_thread


def receive_data():
    host = '127.0.0.1'
    receiver_port = 2000                                # arbitrary non-privileged port
    thread_count = 0
    receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        receiver_side_socket.bind((host, receiver_port))
        n = int(input("Enter No. of Sender(s) You Want to Keep Waiting : "))
        max = int(input("Enter Max No. of Senders Allowed to send Request : "))
        receiver_side_socket.listen(n)                  # queue up to 'n' requests
        print("Socket Has Been Created." + "\nReceiver is Now Listening...." +
              "\nWaiting For Channel(s)/Sender(s) to Connect....")

    except socket.error as e:
        print("Bind Failed! Error : " + str(sys.exc_info()))
        print("Exception Caught : " + str(e))
        receiver_side_socket.close()
        sys.exit()

    except ValueError as v:
        print("Exception Caught : " + str(v))
        print("Receiver Has Been Terminated." + "\nEnter Integer Only From Next Time.")
        receiver_side_socket.close()
        sys.exit()

    while thread_count <= max:
        channel, address = receiver_side_socket.accept()
        ip, receiver_port = str(address[0]), str(address[1])
        print("\nConnected to : " + ip + ':' + receiver_port)
        start_new_thread(channel_thread, (channel, ))
        thread_count += 1
        print("Thread Number = Sender Number = Channel Number = " + str(thread_count))

    # ReceiverSideSocket.close()
    print(f"\nMore Than {max} Senders/Channels aren't allowed to send request(s).")
    print("Receiver has been closed.")


def channel_thread(connection: socket.socket):
    connection.send(str.encode("Receiver is Working : "))
    while True:
        sender_request = connection.recv(2048)
        receiver_data, choice = [str(i) for i in sender_request.decode("utf-8").split("\n")]
        # print(receiver_data)
        # print(choice)

        if choice == '1':
            vrc_data = vrc.gen_VRC(receiver_data)
            if vrc_data == '0':
                Receiver_response = "Error Checking Complete\nNo Error found in Receiver-data"
            else:
                Receiver_response = "Error Checking Complete\nError found in Receiver-data"
            connection.sendall(str.encode(Receiver_response))

        elif choice == '2':
            lrc_data = lrc.gen_LRC(receiver_data)
            if lrc_data == '0':
                Receiver_response = "Error Checking Complete\nNo Error found in Receiver-data"
            else:
                Receiver_response = "Error Checking Complete\nError found in Receiver-data"
            connection.sendall(str.encode(Receiver_response))

        elif choice == '3':
            packet_count = 5
            packet_length = int(len(receiver_data)/packet_count)
            receiver_check_sum = rcs.gen_CheckSum(receiver_data, packet_length)
            connection.sendall(str.encode(receiver_check_sum))

        elif choice == '4':
            key = input("Enter key for calculating CRC \n(Must be same as Sender's Key to get authentic results) : ")
            crc_data = crc.gen_CRC(receiver_data, key)
            Receiver_response = crc_data
            connection.sendall(str.encode(Receiver_response))
    # connection.close()


def main():
    receive_data()


if __name__ == "__main__":
    main()
