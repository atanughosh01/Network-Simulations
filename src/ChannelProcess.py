import sys
import socket
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
from _thread import start_new_thread


def listen_to_sender():
    host = '127.0.0.1'
    sender_port = 2021
    # receiver_port = 2000
    channel_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        channel_side_socket.bind((host, sender_port))
    except socket.error as e:
        print("Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

    while True:
        sender, address = channel_side_socket.accept()
        ip, sender_port = str(address[0]), str(address[1])
        print("\nConnected to Sender via address : " + ip + ':' + sender_port)
        sender_process(sender)


def sender_process(connection: socket.socket):
    try:
        connection.send(str.encode("Channel is Working : "))
        while True:
            sender_request = connection.recv(2048)
            data_word, choice = [str(i) for i in sender_request.decode("utf-8").split("\n")]

            if choice == '1':
                vrc_data = vrc.gen_VRC(data_word)
                code_word = data_word + vrc_data
                connection.close()
                host, receiver_port = ('127.0.0.1', 2000)
                connection.bind((host, receiver_port))
                connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
                connection.close()

            elif choice == '2':
                lrc_data = lrc.gen_LRC(data_word)
                code_word = data_word + lrc_data
                connection.close()
                host, receiver_port = ('127.0.0.1', 2000)
                connection.bind((host, receiver_port))
                connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
                connection.close()

            elif choice == '3':
                packet_count = 4
                packet_length = int(len(data_word)/packet_count)
                sender_check_sum = scs.gen_CheckSum(data_word, packet_length)
                code_word = data_word + sender_check_sum
                connection.close()
                host, receiver_port = ('127.0.0.1', 2000)
                connection.bind((host, receiver_port))
                connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
                connection.close()

            elif choice == '4':
                key = input("Enter key for calculating CRC : ")
                crc_data = crc.gen_CRC(data_word, key)
                code_word = data_word + crc_data
                connection.close()
                host, receiver_port = ('127.0.0.1', 2000)
                connection.bind((host, receiver_port))
                connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
                connection.close()

    except socket.error as e:
        print("Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()
