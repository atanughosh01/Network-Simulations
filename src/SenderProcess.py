import sys
import socket
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
import packages.GenRandError as gre
from _thread import start_new_thread


def send_data():
    host = '127.0.0.1'
    sender_port = 65432
    sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: sender_side_socket.connect((host, sender_port))
    except socket.error as e:
        print("Channel is Currently Inactive. Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

    print("Channel is Currently Active.\nSend Request to Get Response From Receiver.")

    receiver_response = sender_side_socket.recv(1024)

    while True:
        try:
            with open("input.txt", "r") as file:
                data = file.read()
        except FileNotFoundError as fnfe:
            print("\nFILE_ERR : " + str(fnfe))
            sys.exit(1)

        print("\nDATA = " + str(data))
        string_length = len(data)
        try: packet_length = int(input("\nEnter length of each packet : "))     # ENTER 32
        except Exception as ve:
            print("\nEXCEPTION : " + str(ve) + "\nExiting System.... Exited")
            sys.exit(1)

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
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))
                code_word_list.append(code_word)

        elif choice == 2:
            code_word_list = []
            for packet in packet_list:
                lrc_data = lrc.gen_LRC(packet)
                code_word = packet + lrc_data
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))
                code_word_list.append(code_word)

        elif choice == 3:
            code_word_list = []
            for packet in packet_list:
                sub_packet_count = 4
                sub_packet_length = int(len(packet)/sub_packet_count)
                sender_check_sum = scs.gen_CheckSum(packet, sub_packet_length)
                code_word = packet + sender_check_sum
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))
                code_word_list.append(code_word)

        elif choice == 4:
            # key = input("\nEnter the key for CRC-bit generation : ")
            key = "10110"
            code_word_list = []
            for packet in packet_list:
                crc_data = crc.gen_CRC(packet, key)
                code_word = packet + crc_data
                # code_word = gre.gen_rand_error(code_word, len(code_word))
                sender_side_socket.sendall(str.encode("\n".join([str(code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024)
                print(receiver_response.decode("utf-8"))
                code_word_list.append(code_word)

        else:
            print("\nWRONG INPUT! Input must be an integer b/w 1, 2, 3 and 4")
            print("Enter your choice once again")


def main():
    send_data()


if __name__ == "__main__":
    main()
