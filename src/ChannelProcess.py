import sys
import socket
import packages.CRC as crc
import packages.VRC as vrc
import packages.LRC as lrc
import packages.senderCheckSum as scs
import packages.receiverCheckSum as rcs
from _thread import start_new_thread

def listen_to_sender():

    host = '127.0.0.1'
    port = 2021
    ChannelSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ChannelSideSocket.bind((host, port))
    except socket.error as e:
        print("Connection Failed!\n\nError : " + str(sys.exc_info()))
        print("\nException Caught : " + str(e))
        sys.exit()

        while True:
            pass