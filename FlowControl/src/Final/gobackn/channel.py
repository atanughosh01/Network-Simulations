import time
import socket
import random


def inject_random_error(frame):
    pos = random.randint(0, len(frame)-1)
    frame = frame[:pos]+'1'+frame[pos+1:]
    return frame


def extract_message(frame):
    endidx = -1
    for i in range(len(frame)-1):
        if frame[i] == '/' and endidx == -1:
            endidx = i
            break
    return frame[:endidx]


def extract_count(frame):
    startidx = -1
    endidx = -1
    for i in range(len(frame)-1):
        if frame[i] == '/':
            if startidx == -1: startidx = i+1
            else: endidx = i
    cnt = frame[startidx:endidx]
    return int(cnt)


def extract_status(frame):
    count = 0
    startidx = -1
    for i in range(len(frame)-1):
        if frame[i] == '/': count += 1
        if count == 2 and startidx == -1:
            startidx = i+1
            break
    return frame[startidx:]


class Channel():

    def __init__(self, totalsender, totalreceiver, windowsize):
        self.totalsender = totalsender
        self.senderhost = '127.0.0.1'
        self.senderport = 8080
        self.senderconn = []

        self.totalreceiver = totalreceiver
        self.receiverhost = '127.0.0.2'
        self.receiverport = 9090
        self.receiverconn = []

        self.windowsize = windowsize
        self.slidingwindow = []
        self.currentcount = 0

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
                prevtime = time.time()
                data = str(data)
                origmsg = extract_message(data)
                if not origmsg: break
                if origmsg == 'q0': break
                print('Received from Sender', i+1, ':', str(data))

                recvno = random.randint(0, len(self.receiverconn)-1)
                print('Sending to Receiver', recvno+1)
                rconn = self.receiverconn[recvno]
                cnt = extract_count(data)
                msg = inject_random_error(origmsg)
                newdata = msg + '/' + str(cnt) + '/'
                rconn[0].sendto(newdata.encode(), rconn[1])

                # received from receiver
                rdata = rconn[0].recv(1024).decode('utf-8')
                rdata = str(rdata)
                time.sleep(0.5)
                curtime = time.time()
                if curtime-prevtime > 2: newdata += 'TIMEOUT'
                else: newdata += rdata
                self.slidingwindow.append([data, newdata, i, recvno])

                msg = extract_message(newdata)
                cnt = extract_count(newdata)
                status = extract_status(newdata)
                print(msg, str(cnt), status)
                print('Round trip time: ', str(curtime-prevtime))
                print('Current frame no:', str((self.currentcount % windowsize)+1))
                if (self.currentcount % windowsize)+1 == self.windowsize:
                    idx = 0
                    flag = 1
                    while flag == 1:
                        idx = 0
                        flag = 0
                        while idx < self.windowsize:
                            currframe = self.slidingwindow[idx][1]
                            msg = extract_message(currframe)
                            cnt = extract_count(currframe)
                            status = extract_status(currframe)

                            if status == 'NAK' or status == 'TIMEOUT':
                                flag = 1
                                break
                            idx += 1

                        print(' ------------------------------ ')
                        if flag == 1: print('RESEND FROM FRAME NO:', str(idx+1))
                        else: print('BLOCK OF WINDOW SIZE', self.windowsize, 'SUCCESSFULLY SENT')
                        print(' ------------------------------ ')

                        while flag == 1 and idx < self.windowsize:
                            print()
                            prevtime = time.time()
                            prevframe = self.slidingwindow[idx][0]
                            currframe = self.slidingwindow[idx][1]
                            sendno = self.slidingwindow[idx][2]
                            recvno = self.slidingwindow[idx][3]
                            conn = self.senderconn[sendno]
                            rconn = self.receiverconn[recvno]

                            # sending all frames to its sender from first NAK
                            print('Current frame no:', str(idx+1))
                            print('Again Sending to Receiver', recvno+1)

                            msg = extract_message(prevframe)
                            msg = inject_random_error(msg)
                            data = msg + '/' + str(cnt) + '/'
                            rconn[0].sendto(data.encode(), rconn[1])

                            # receiving ACK or NAK from receiver
                            rdata = rconn[0].recv(1024).decode('utf-8')
                            rdata = str(rdata)
                            data += rdata

                            msg = extract_message(data)
                            cnt = extract_count(data)
                            stat = extract_status(data)
                            curtime = time.time()
                            print(msg, str(cnt), stat)
                            print('Round trip time: ', str(curtime-prevtime))
                            self.slidingwindow[idx][1] = data
                            idx += 1

                self.currentcount += 1
            if origmsg == 'q0':
                break
        return


if __name__ == '__main__':
    totalsen = int(input('Enter number of senders: '))
    totalrecv = int(input('Enter number of receivers: '))
    windowsize = int(input('Enter window size: '))

    ch = Channel(totalsen, totalrecv, windowsize)
    ch.initialize_senders()
    ch.initialize_receivers()
    ch.process_data()
    ch.terminate_senders()
    ch.terminate_receivers()
