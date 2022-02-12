import sys
import time
import socket
import random


def wait_random_time():
    x = random.randint(0, 5)
    if x <= 1: time.sleep(2)


def check_error(frame):
    count_ones = 0
    for ch in frame:
        if ch == '1': count_ones += 1
    return count_ones % 2


def Main(senderno):
    print('Initiating Receiver #', senderno)
    host = '127.0.0.2'
    port = 9090
    receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_side_socket.connect((host, port))

    while True:
        print()
        data = receiver_side_socket.recv(1024).decode('utf-8')
        if not data: break
        if data == 'q0': break
        print('Received from channel :', str(data))
        wait_random_time()
        if check_error(data) == 0: rdata = 'ACK'
        else:
            time.sleep(2)
            rdata = 'TIMEOUT'
        print('Sending to channel :', str(rdata))
        receiver_side_socket.send(rdata.encode())

    receiver_side_socket.close()


if __name__ == '__main__':
    if len(sys.argv) > 1: senderno = int(sys.argv[1])
    else: senderno = 1
    Main(senderno)
