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
        data = input("\nEnter data to send (Enter 0 to Exit) : ")
        if data == '0':
            sender_side_socket.close()
            print("\nConnection Has Been Closed.\nSender Has Exited.")
            sys.exit()

        print("Generate Redundant data -> Select 1 for VRC, 2 for LRC, 3 for CheckSum, 4 for CRC ")
        choice = int(input("Enter Your Choice (1, 2, 3 or 4) : "))

        if choice == 1:
            vrc_data = vrc.gen_VRC(data)
            sent_data = data + vrc_data
            sender_side_socket.sendall(str.encode("\n".join([str(sent_data), str(choice)])))
            receiver_response = sender_side_socket.recv(1024)
            print(receiver_response.decode("utf-8"))

        elif choice == 2:
            lrc_data = lrc.gen_LRC(data)
            sent_data = data + lrc_data
            sender_side_socket.sendall(str.encode("\n".join([str(sent_data), str(choice)])))
            receiver_response = sender_side_socket.recv(1024)
            print(receiver_response.decode("utf-8"))

        elif choice == 3:
            packet_count = 4
            packet_length = int(len(data)/packet_count)
            sender_check_sum = scs.gen_CheckSum(data, packet_length)
            sent_data = data + sender_check_sum
            sender_side_socket.sendall(str.encode("\n".join([str(sent_data), str(choice)])))
            receiver_check_sum = sender_side_socket.recv(1024).decode("utf-8")
            if int(receiver_check_sum) == 0:
                print("Error Checking Complete\nNo Error found in Receiver-data")
            else:
                print("Error Checking Complete\nError found in Receiver-data")


        elif choice == 4:
            key = input("Enter key for calculating CRC : ")
            crc_data = crc.gen_CRC(data, key)
            sent_data = data + crc_data
            sender_side_socket.sendall(str.encode("\n".join([str(sent_data), str(choice)])))
            receiver_response = sender_side_socket.recv(1024).decode("utf-8")
            if int(receiver_response) == 0:
                print("Error Checking Complete\nNo Error found in Receiver-data")
            else:
                print("Error Checking Complete\nError found in Receiver-data")

        else:
            print("ERROR! You must choose b/w 1, 2. 3 and 4")


def main():
    send_data()


if __name__ == "__main__":
    main()
