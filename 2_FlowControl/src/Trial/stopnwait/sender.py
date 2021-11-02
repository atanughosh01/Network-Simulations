import sys
import time
import socket


def create_frame(data):
    count_ones = 0
    for ch in data:
        if ch == '1': count_ones += 1
    data += str(count_ones % 2)
    return data


def Main(senderno):
    print('Initiating Sender #', senderno)
    host = '127.0.0.1'
    port = 8080
    sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender_side_socket.connect((host, port))

    while True:
        print()
        data = input("Enter $ ")
        prevtime = time.time()
        data = create_frame(data)
        print('Sending to channel :', str(data))
        sender_side_socket.send(data.encode())
        if not data: break
        if data == 'q0': break
        rdata = sender_side_socket.recv(1024).decode('utf-8')
        print('Received from channel :', str(rdata))
        curtime = time.time()
        print('Round trip time: ', str(curtime-prevtime))
        if curtime-prevtime > 2: timeout = 1
        else: timeout = 0
        with open('checktime.txt', 'w') as fileout: fileout.write(str(timeout))
        
        while timeout == 1:
            print()
            prevtime = time.time()
            if timeout == 1: print('TIMEOUT of 2s EXPIRED !!')
            else: print('THE FRAME GOT CORRUPTED !!!')
            print('Again Sending to channel :', str(data))
            sender_side_socket.send(data.encode())
            rdata = sender_side_socket.recv(1024).decode()
            print('Again Received from channel :', str(rdata))
            curtime = time.time()
            print('Round trip time:', str(curtime-prevtime), 'seconds')
            if curtime-prevtime > 2: timeout = 1
            else: timeout = 0
            with open('checktime.txt', 'w') as fileout: fileout.write(str(timeout))

    sender_side_socket.close()


if __name__ == '__main__':
    if len(sys.argv) > 1: senderno = int(sys.argv[1])
    else: senderno = 1
    Main(senderno)
