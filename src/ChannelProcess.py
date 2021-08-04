import sys
import socket
import packages.CRC as crc
import packages.VRC as vrc
import packages.LRC as lrc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
from _thread import start_new_thread

def listen_to_sender():

    host = '127.0.0.1'
    port = 2021
    ChannelSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ChannelSideSocket.bind((host, port))
    except socket.error as e:
        print("Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

    while True:
        Sender, address = ChannelSideSocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("|Connected to : " + ip + ':' + port)
        sender_process()


def sender_process(connection):
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