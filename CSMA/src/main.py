import const
import socket
import threading
import multiprocessing
from sender import *
from channel import *
from receiver import *


def start_simulation():

    #writeFromSenderToChannel = []
    #readFromSenderToChannel = []

    write_from_channel_to_sender = []
    read_from_channel_to_sender = []

    write_from_channel_to_receiver = []
    read_from_channel_to_receiver = []

    write_from_receiver_to_channel = []
    read_from_receiver_to_channel = []

    for i in range(const.total_sender_number):

        read_head, write_head = multiprocessing.Pipe()
        write_from_channel_to_sender.append(write_head)
        read_from_channel_to_sender.append(read_head)

    for i in range(const.total_receiver_number):
        read_head, write_head = multiprocessing.Pipe()
        write_from_channel_to_receiver.append(write_head)
        read_from_channel_to_receiver.append(read_head)

    read_from_sender_to_channel, write_from_sender_to_channel = multiprocessing.Pipe()

    sender_list = []
    receiver_list = []

    technique = int(input("The CSMA technique you want to use\n1. One Persistent Method\n2. Non Persistent Method\n3. P-Persistent Method\nChoose one of the following - "))

    for i in range(const.total_sender_number):
        sender = Sender(i, 'textfiles/input/input'+str(i)+'.txt', write_from_sender_to_channel, read_from_channel_to_sender[i], technique)
        sender_list.append(sender)

    for i in range(const.total_receiver_number):
        receiver = Receiver(i, read_from_channel_to_receiver[i])
        receiver_list.append(receiver)

    channel = Channel(read_from_sender_to_channel, write_from_channel_to_sender, read_from_receiver_to_channel, write_from_channel_to_receiver)

    sender_threads = []
    receiver_threads = []

    for i in range(len(sender_list)):
        p = threading.Thread(target=sender_list[i].transmit)
        sender_threads.append(p)

    for i in range(len(receiver_list)):
        p = threading.Thread(target=receiver_list[i].initiate_receiver_process)
        receiver_threads.append(p)

    channel_thread = threading.Thread(target=channel.initiate_channel_process)

    channel_thread.start()

    for thread in receiver_threads:
        thread.start()

    for thread in sender_threads:
        thread.start()

    for thread in sender_threads:
        thread.join()

    channel_thread.join()

    for thread in receiver_threads:
        thread.join()


if __name__ == "__main__":
    start_simulation()

# python main.py
