
# Generates error by flipping bits at specified number of indices of input string
import random


def gen_rand_error(data: str, count: int) -> str:
    length = len(data)
    digit_list = list(data)
    k = random.sample(range(0, length), count)
    for index in k:
        # This will replace 0-s with 1-s & 1-s with 0-s at specified number of positions
        if digit_list[index] == '1':
            digit_list[index] = digit_list[index].replace('1', '0')
        elif digit_list[index] == '0':
            digit_list[index] = digit_list[index].replace('0', '1')
    return ("".join(digit_list))


def main():
    string_to_modify = str(input("Enter the string to be modified : "))
    flip_count = int(input("Enter number of bits to be flipped : "))
    new_string = gen_rand_error(string_to_modify, flip_count)
    print("The modified String is : " + new_string)


if __name__ == "__main__":
    main()


# import sys
# import socket
# import random
# import packages.GenRandError as gre


# def listen_to_sender():
#     host = '127.0.0.1'
#     sender_port = 34567
#     receiver_port = 65432
#     channel_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     try: channel_side_socket.bind((host, sender_port))
#     except socket.error as se:
#         print("\nConnection Failed!\n\nError Caught : " + str(sys.exc_info()))
#         print("\n[EXCEPTION] Error Caught : " + str(se))
#         sys.exit(1)

#     while True:
#         channel_side_socket.listen(1)
#         print("Socket Has Been Created.\nChannel is Now Listening...." +
#               "\nWaiting for Sender to transfer data-packets.")
#         sender, address = channel_side_socket.accept()
#         ip, sender_port = str(address[0]), str(address[1])
#         print("\nConnected to Receiver via address : " + ip + ':' + sender_port)
#         sender_process(sender)


# def sender_process(connection: socket.socket):
#     try:
#         while True:
#             sender_request = connection.recv(2048)
#             code_word, choice = [str(i) for i in sender_request.decode("utf-8").split("\n")]

#             if choice == '0':
#                 print("\nSender has been disconnected\nChannel is exiting....")
#                 print("\nChannel is disconnecing... Exiting System... Exited")
#                 connection.close()
#                 sys.exit(1)

#             elif choice == '1' or choice == '2' or choice == '3' or choice == '4':
#                 flip_count = random.randint(1, len(code_word))
#                 corrupt_code_word = gre.gen_rand_error(code_word, flip_count)
#                 print("\nDisconnecting socket from sender")
#                 connection.close()
#                 host, receiver_port = ('127.0.0.1', 65432)
#                 connection.connect((host, receiver_port))
#                 print("\nConnected to Receiver via address : " + host + ':' + receiver_port)
#                 connection.sendall(str.encode("\n".join(str(corrupt_code_word), str(choice))))
#                 connection.close()

#     except socket.error as e:
#         print("Connection Failed!\n\nError : " + str(sys.exc_info()))
#         print("\n[EXCEPTION] Error Caught : " + str(e))
#         sys.exit()


# def main():
#     listen_to_sender()


# if __name__ == "__main__":
#     main()
