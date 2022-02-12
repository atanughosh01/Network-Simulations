import os
import sys
import time
import socket
import random


def inject_random_error(frame):
    pos = random.randint(0, len(frame)-1)
    frame = frame[:pos]+'1'+frame[pos+1:]
    return frame


class Channel():

    def __init__(self, totalsender, totalreceiver):
        self.totalsender = totalsender
        self.senderhost = '127.0.0.1'
        self.senderport = 8080
        self.senderconn = []

        self.totalreceiver = totalreceiver
        self.receiverhost = '127.0.0.2'
        self.receiverport = 9090
        self.receiverconn = []


    def initialize_senders(self):
        sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sender_side_socket.bind((self.senderhost, self.senderport))
        sender_side_socket.listen(self.totalsender)
        for _ in range(1, self.totalsender+1):
            conn = sender_side_socket.accept()
            self.senderconn.append(conn)
        print('Initiated all sender connections')


    def terminate_senders(self):
        for conn in self.senderconn: conn[0].close()
        print('Closed all sender connections')


    def initialize_receivers(self):
        receiver_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver_side_socket.bind((self.receiverhost, self.receiverport))
        receiver_side_socket.listen(self.totalreceiver)
        for _ in range(1, self.totalreceiver+1):
            conn = receiver_side_socket.accept()
            self.receiverconn.append(conn)
        print('Initiated all receiver connections')


    def terminate_receivers(self):
        for conn in self.receiverconn: conn[0].close()
        print('Closed all receiver connections')


    def process_data(self):
        while True:
            for i in range(len(self.senderconn)):
                print()
                conn = self.senderconn[i]
                data = conn[0].recv(1024).decode('utf-8')
                if not data: break
                if data == 'q0': break
                print('Received from Sender', i+1, ':', str(data))

                recvno = random.randint(0, len(self.receiverconn)-1)
                print('Sending to Receiver', recvno+1)
                rconn = self.receiverconn[recvno]
                data = inject_random_error(data)
                rconn[0].sendto(data.encode(), rconn[1])

                # received from receiver
                rdata = rconn[0].recv(1024).decode('utf-8')
                print('Received from Receiver', recvno+1, ':', str(rdata))
                
                print('Sending to Sender', i+1)
                conn[0].send(rdata.encode())

                time.sleep(0.002)
                try: 
                    with open('checktime.txt', 'r') as filein:
                        timeout = int(filein.read())
                    os.remove('checktime.txt')
                except: 
                    print('Timeout -->>', timeout)
                    break

                while timeout == 1:
                    print()
                    data = conn[0].recv(1024).decode('utf-8')
                    print('Again Received from Sender', i+1, ':', str(data))
                    data = inject_random_error(data)
                    print('Again Sending to Receiver', recvno+1)
                    rconn[0].sendto(data.encode(), rconn[1])
                    rdata = rconn[0].recv(1024).decode('utf-8')
                    print('Again Received from Receiver', recvno+1, ':', str(rdata))
                    print('Again Sending to Sender', i+1)
                    conn[0].send(rdata.encode())

                    time.sleep(0.002)
                    try: 
                        with open('checktime.txt', 'r') as filein:
                            timeout = int(filein.read())
                        os.remove('checktime.txt')
                    except: 
                        print('Timeout -->>', timeout)
                        break
                    print('Timeout -->>', timeout)

            if data == 'q0':
                break
        return


if __name__ == '__main__':
    totalsen = int(input('Enter number of senders: '))
    totalrecv = int(input('Enter number of receivers: '))

    ch = Channel(totalsen, totalrecv)
    ch.initialize_senders()
    ch.initialize_receivers()
    ch.process_data()
    ch.terminate_senders()
    ch.terminate_receivers()
