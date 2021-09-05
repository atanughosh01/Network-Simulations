import sys
import socket
import random
import threading
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Channel:

    def __init__(self) -> None:
        pass

    def inject_error(self, packet: str, count: int) -> str:
        length = len(packet)
        digit_list = list(packet)
        k = random.sample(range(0, length), count)
        for index in k:
            if digit_list[index] == '1':
                digit_list[index] = digit_list[index].replace('1', '0')
            elif digit_list[index] == '0':
                digit_list[index] = digit_list[index].replace('0', '1')
        return ("".join(digit_list))

    def sender_packet(self, sender):
        pass

    def receiver_ack(self, receiver):
        pass

    def channel_process():
        pass
