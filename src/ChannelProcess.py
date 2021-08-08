import sys
import socket
import random
import packages.GenRandError as gre
# import packages.VRC as vrc
# import packages.LRC as lrc
# import packages.CRC as crc
# import packages.senderCheckSum as scs
# import packages.receiverCheckSum as rcs
# from _thread import start_new_thread


def listen_to_sender():
    host = '127.0.0.1'
    sender_port = 65400
    # receiver_port = 65432
    channel_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: channel_side_socket.bind((host, sender_port))
    except socket.error as se:
        print("\nConnection Failed!\n\nError Caught : " + str(sys.exc_info()))
        print("\n[EXCEPTION] Error Caught : " + str(se))
        sys.exit(1)

    while True:
        channel_side_socket.listen(1)
        sender, address = channel_side_socket.accept()
        ip, sender_port = str(address[0]), str(address[1])
        print("\nConnected to Sender via address : " + ip + ':' + sender_port)
        sender_process(sender)


def sender_process(connection: socket.socket):
    try:
        connection.send(str.encode("\nChannel is working. Waiting for Sender to transfer data-packets."))
        while True:
            sender_request = connection.recv(2048)
            code_word, choice = [str(i) for i in sender_request.decode("utf-8").split("\n")]

            if choice == '0':
                print("\nSender has been disconnected\nChannel is exiting....")
                print("\nChannel is disconnecing... Exiting System... Exited")
                connection.close()
                sys.exit(1)

            elif choice == '1' or choice == '2' or choice == '3' or choice == '4':
                corrupt_code_word = gre.gen_rand_error(code_word, random.randint(1, len(code_word)))
                connection.close()
                host, receiver_port = ('127.0.0.1', 65432)
                connection.connect((host, receiver_port))
                print("\nConnected to : " + host + ':' + receiver_port)
                connection.sendall(str.encode("\n".join(str(corrupt_code_word), str(choice))))
                connection.close()

            # elif choice == '2':
            #     lrc_data = lrc.gen_LRC(code_word)
            #     code_word = code_word + lrc_data
            #     connection.close()
            #     host, receiver_port = ('127.0.0.1', 65432)
            #     connection.bind((host, receiver_port))
            #     connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
            #     connection.close()

            # elif choice == '3':
            #     packet_count = 4
            #     packet_length = int(len(code_word)/packet_count)
            #     sender_check_sum = scs.gen_CheckSum(code_word, packet_length)
            #     code_word = code_word + sender_check_sum
            #     connection.close()
            #     host, receiver_port = ('127.0.0.1', 65432)
            #     connection.bind((host, receiver_port))
            #     connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
            #     connection.close()

            # elif choice == '4':
            #     key = input("Enter key for calculating CRC : ")
            #     crc_data = crc.gen_CRC(code_word, key)
            #     code_word = code_word + crc_data
            #     connection.close()
            #     host, receiver_port = ('127.0.0.1', 65432)
            #     connection.bind((host, receiver_port))
            #     connection.sendall(str.encode("\n".join(str(code_word), str(choice))))
            #     connection.close()

    except socket.error as e:
        print("Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\n[EXCEPTION] Error Caught : " + str(e))
        sys.exit()


def main():
    listen_to_sender()


if __name__ == "__main__":
    main()
