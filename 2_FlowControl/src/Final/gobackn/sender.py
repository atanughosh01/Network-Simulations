import sys
import socket


def create_frame(data):
    count_ones = 0
    for ch in data:
        if ch == '1': count_ones += 1
    data += str(count_ones % 2)
    return data


def extract_message(frame):
    endidx = -1
    for i in range(len(frame)-1):
        if frame[i] == '/' and endidx == -1:
            endidx = i
            break
    return frame[:endidx]

'''
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
'''

def Main(senderno):
    count = 0
    sent_frames = []
    print('Initiating Sender #', senderno)
    host = '127.0.0.1'
    port = 8080
    sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sender_side_socket.connect((host, port))

    while True:
        print()
        data = input("Enter $ ")
        data = create_frame(data) + '/' + str(count) + '/'
        msg = extract_message(data)
        print('Sending to channel :', str(msg))
        sender_side_socket.send(data.encode())
        sent_frames.append(data)
        count += 1
        if not msg: break
        if msg == 'q0': break
        
    sender_side_socket.close()


if __name__ == '__main__':
    if len(sys.argv) > 1: senderno = int(sys.argv[1])
    else: senderno = 1
    Main(senderno)
