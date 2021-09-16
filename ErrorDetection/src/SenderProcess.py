import sys
import socket
import random
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.senderCheckSum as scs
import ChannelProcess as injerr           # module ChannelProcess is imported for injecting errors


def start_sender():
    host = '127.0.0.1'
    port = 65432                          # arbitrary non-privileged port
    sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try: sender_side_socket.connect((host, port))
    except socket.error as se:
        print("\nChannel is currently inactive. Connection failed!\n\n[Error 1] : " + str(sys.exc_info()))
        print("\n[EXCEPTION 1] SOCK_ERR Caught : " + str(se))
        sys.exit(1)

    print("\nReceiver is currently active.\nSend data to get response from receiver.")
    while True:
        try:
            with open("textfiles/input.txt", "r") as text_file:
                data = text_file.read()
        except FileNotFoundError as fnfe:
            print("\n[EXCEPTION 2] FILE_ERR Caught : " + str(fnfe))
            sys.exit(1)

        string_length = len(data)
        try: packet_length = int(input("\nEnter length of each packet (Should be greater than 16): "))    # ENTER 32
        except ValueError as ex:
            print("\n[EXCEPTION 3] Error Caught : " + str(ex) + "\nExiting System.... Exited")
            sys.exit(1)

        packet_count = int(string_length/packet_length)
        print("\nLength of data = " + str(string_length))
        print("Number of packets = " + str(packet_count))
        print("Length of each packet = " + str(packet_length))

        # generates data-packets by breaking down the data
        packet_list = []
        for i in range(packet_count):
            k = packet_length
            packet = data[i*k: (i+1)*k]
            packet_list.append(packet)

        print("\nGenerate Redundant data -> Select 1 for VRC, 2 for LRC, 3 for CheckSum, 4 for CRC ")
        try: choice = int(input("\nEnter Your Choice (1, 2, 3 or 4 (Enter 0 to exit system)) : "))
        except ValueError as ve:
            print("[EXCEPTION 4] ValueError Caught : " + str(ve) + "\nOnly integer inputs are allowed. Try again -->")
            continue

        if choice == 0:
            print("\nExiting system.... Exited")
            sender_side_socket.close()
            sys.exit(1)

        elif choice == 1:
            for packet in packet_list:
                vrc_data = vrc.gen_VRC(packet)
                code_word = packet + vrc_data
                flip_count = random.randint(1, len(code_word))
                corrupt_code_word = injerr.gen_rand_error(code_word, flip_count)
                sender_side_socket.sendall(str.encode("\n".join([str(corrupt_code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024).decode("utf-8")
                with open("textfiles/vrc.txt", "a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")                         # If file is not empty then append '\n'
                    file_object.write(receiver_response)                # Append text at the end of file

        elif choice == 2:
            for packet in packet_list:
                lrc_data = lrc.gen_LRC(packet)
                code_word = packet + lrc_data
                flip_count = random.randint(1, len(code_word))
                corrupt_code_word = injerr.gen_rand_error(code_word, flip_count)
                sender_side_socket.sendall(str.encode("\n".join([str(corrupt_code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024).decode("utf-8")
                with open("textfiles/lrc.txt", "a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")                         # If file is not empty then append '\n'
                    file_object.write(receiver_response)                # Append text at the end of file

        elif choice == 3:
            for packet in packet_list:
                sub_packet_count = 4
                sub_packet_length = int(len(packet)/sub_packet_count)
                sender_check_sum = scs.gen_CheckSum(packet, sub_packet_length)
                code_word = packet + sender_check_sum
                flip_count = random.randint(1, len(code_word))
                corrupt_code_word = injerr.gen_rand_error(code_word, flip_count)
                sender_side_socket.sendall(str.encode("\n".join([str(corrupt_code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024).decode("utf-8")
                with open("textfiles/checksum.txt", "a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")                         # If file is not empty then append '\n'
                    file_object.write(receiver_response)                # Append text at the end of file

        elif choice == 4:
            # key = "111010101"                                       # CRC-8 (x^8 + x^7 + x^6 + x^4 + x^2 + 1)
            key = "11000000000000101"                               # CRC-16 (x^16 + x^15 + x^2 + 1)
            for packet in packet_list:
                crc_data = crc.gen_CRC(packet, key)
                code_word = packet + crc_data
                flip_count = random.randint(1, len(code_word))
                corrupt_code_word = injerr.gen_rand_error(code_word, flip_count)
                sender_side_socket.sendall(str.encode("\n".join([str(corrupt_code_word), str(choice)])))
                receiver_response = sender_side_socket.recv(1024).decode("utf-8")
                with open("textfiles/crc.txt", "a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")                         # If file is not empty then append '\n'
                    file_object.write(receiver_response)                # Append text at the end of file

        else:
            print("\nINVALID INPUT! Input must be an integer b/w 1, 2, 3 and 4")
            print("Enter your choice once again")


if __name__ == "__main__":
    start_sender()
