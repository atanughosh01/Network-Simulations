import sys
import socket
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
from _thread import start_new_thread


def send_data():
    host = '127.0.0.1'
    sender_port = 2021
    sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sender_side_socket.connect((host, sender_port))
    except socket.error as e:
        print("Channel is Currently Inactive. Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

    print("Channel is Currently Active.\nSend Request to Get Response From Receiver.")

    receiver_response = sender_side_socket.recv(1024)

    while True:
        # data = input("\nEnter data to send (Enter 0 to Exit) : ")
        try:
            with open("input.txt", "r") as file:
                data = file.read()
        except FileNotFoundError as fnfe:
            print("\nFILE_ERR : " + str(fnfe))
            sys.exit()

        if data == '0':
            sender_side_socket.close()
            print("\nConnection Has Been Closed.\nSender Has Exited.")
            sys.exit()

        print("DATA = " + str(data))
        string_length = len(data)
        # packet_length = 32
        try:
            packet_length = int(input("\nEnter length of each packet : "))
        except ValueError as ve:
            print("\nVAL_ERR : " + str(ve))
            sys.exit()

        packet_count = int(string_length/packet_length)
        print("\nLength of data = " + str(string_length))
        print("Number of packets = " + str(packet_count))
        print("Length of each packet = " + str(packet_length))

        packet_list = []
        for i in range(packet_count):
            k = packet_length
            packet = data[i*k: (i+1)*k]
            packet_list.append(packet)

        print("\nOriginal Packet List :", packet_list)

        print("\nGenerate Redundant data -> Select 1 for VRC, 2 for LRC, 3 for CheckSum, 4 for CRC ")
        choice = int(input("Enter Your Choice (1, 2, 3 or 4) : "))

        if choice == 1:
            code_word_list = []
            for packet in packet_list:
                vrc_data = vrc.gen_VRC(packet)
                code_word = packet + vrc_data
                code_word_list.append(code_word)
            print("\nCode-Word List :", code_word_list)

            # vrc_data = vrc.gen_VRC(data)
            # sent_data = data + vrc_data

            for code_word in code_word_list:
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))

        elif choice == 2:
            code_word_list = []
            for packet in packet_list:
                lrc_data = lrc.gen_LRC(packet)
                code_word = packet + lrc_data
                code_word_list.append(code_word)

            # lrc_data = lrc.gen_LRC(data)
            # sent_data = data + lrc_data

            for code_word in code_word_list:
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))

        elif choice == 3:
            code_word_list = []
            for packet in packet_list:
                sub_packet_count = 4
                sub_packet_length = int(len(packet)/sub_packet_count)
                sender_check_sum = scs.gen_CheckSum(packet, sub_packet_length)
                code_word = packet + sender_check_sum
                code_word_list.append(code_word)

            # packet_count = 4
            # packet_length = int(len(data)/packet_count)
            # sender_check_sum = scs.gen_CheckSum(data, packet_length)
            # sent_data = data + sender_check_sum

            for code_word in code_word_list:
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))
                receiver_check_sum = sender_side_socket.recv(1024).decode("utf-8")
                if int(receiver_check_sum) == 0:
                    print("Error Checking Complete\nNo Error found in Receiver-data")
                else:
                    print("Error Checking Complete\nError found in Receiver-data")


        elif choice == 4:
            key = input("\nEnter the key for CRC-bit generation : ")
            code_word_list = []
            for packet in packet_list:
                CRC_DATA = crc.gen_CRC(packet, key)
                code_word = packet + CRC_DATA
                code_word_list.append(code_word)

            # key = input("Enter key for calculating CRC : ")
            # crc_data = crc.gen_CRC(data, key)
            # sent_data = data + crc_data

            for code_word in code_word_list:
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024).decode("utf-8")
                if int(receiver_response) == 0:
                    print("Error Checking Complete\nNo Error found in Receiver-data")
                else:
                    print("Error Checking Complete\nError found in Receiver-data")

        else:
            print("\nWRONG INPUT! Input must be an integer b/w 1, 2, 3 and 4")
            print("Enter your choice once again")


def main():
    send_data()


if __name__ == "__main__":
    main()
