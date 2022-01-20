import sys
import socket
from _thread import start_new_thread
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.receiverCheckSum as rcs


def receive_data():
    host = '127.0.0.1'
    port = 65432                                # arbitrary non-privileged port
    thread_count = 0
    receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        receiver_side_socket.bind((host, port))
        max_sndr = int(input("\nEnter max number of senders allowed to send request : "))
        receiver_side_socket.listen(5)
        print("\nSocket has been created.\nReceiver is now listening.\nWaiting for sender(s) to connect....")

    except ValueError as ex:
        print("\n[ERROR 1] Error Description : " + str(sys.exc_info()))
        print("[EXCEPTION 1] Exception : " + str(ex))
        receiver_side_socket.close()
        print("\nReceiver has been terminated. Socket has been closed.")
        sys.exit(1)

    # do untill thread-count is not greater than the maximum limit
    while thread_count <= max_sndr:
        sender_connection, address = receiver_side_socket.accept()
        ip, port = str(address[0]), str(address[1])
        print("\nConnected to sender via address : " + ip + ':' + port)
        start_new_thread(sender_thread, (sender_connection, ))
        thread_count += 1
        print("Thread number = Sender number = " + str(thread_count))

    print(f"\nMore than {max_sndr} senders aren't allowed to send request(s).")
    print("Receiver has been terminated. Socket has been closed.")


# senders are connected via single threads to the multithreaded receiver
def sender_thread(connection: socket.socket):
    while True:
        sender_request = connection.recv(2048)
        receiver_data, choice = [str(i) for i in sender_request.decode("utf-8").split("\n")]

        if choice == '1':
            vrc_data = vrc.gen_VRC(receiver_data)
            if int(vrc_data) == 0: receiver_response = "NO ERROR HAS BEEN FOUND"
            else: receiver_response = "ERROR HAS BEEN FOUND"
            connection.sendall(str.encode(receiver_response))

        elif choice == '2':
            lrc_data = lrc.gen_LRC(receiver_data)
            if int(lrc_data) == 0: receiver_response = "NO ERROR HAS BEEN FOUND"
            else: receiver_response = "ERROR HAS BEEN FOUND"
            connection.sendall(str.encode(receiver_response))

        elif choice == '3':
            packet_count = 5
            packet_length = int(len(receiver_data)/packet_count)
            receiver_checksum = rcs.gen_CheckSum(receiver_data, packet_length)
            if int(receiver_checksum) == 0: receiver_response = "NO ERROR HAS BEEN FOUND"
            else: receiver_response = "ERROR HAS BEEN FOUND"
            connection.sendall(str.encode(receiver_response))

        elif choice == '4':
            # key = "111010101"                                     # CRC-8 (x^8 + x^7 + x^6 + x^4 + x^2 + 1)
            key = "11000000000000101"                               # CRC-16 (x^16 + x^15 + x^2 + 1)
            crc_data = crc.gen_CRC(receiver_data, key)
            if int(crc_data) == 0: receiver_response = "NO ERROR HAS BEEN FOUND"
            else: receiver_response = "ERROR HAS BEEN FOUND"
            connection.sendall(str.encode(receiver_response))


if __name__ == "__main__":
    receive_data()
