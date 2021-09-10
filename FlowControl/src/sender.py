import os
import sys
import time
import socket
import random
import threading
import packages.const as const
from packages.template import *
from _thread import start_new_thread
import packages.go_back_N as go_back_N
import packages.stop_and_wait as stop_and_wait
import packages.selective_repeat as selective_repeat


class Sender:

    def __init__(self) -> None:
        self.port = 65432
        self.host = '127.0.0.1'
        self.sndr_thread_count = 0
        self.MAX = const.total_sender_number

    def gen_pkt(self) -> list[str]:
        self.data = read_file("textfiles/input.txt")
        self.packet_list = create_pkt(self.data)
        return self.packet_list

    def send_pkt(self, pkt: str, conn: socket.socket):
        conn.sendall(pkt)

    def recv_ack(self, conn: socket.socket):
        ack = conn.recv(1024).decode("utf-8")
        return ack

    def initiate_sender_process(self):
        self.sender_side_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender_side_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try: self.sender_side_socket.connect((self.host, self.port))
        except socket.error as se:
            print("\nChannel is currently inactive. Connection failed!\n\n[Error 1] : " + str(sys.exc_info()))
            print("\n[EXCEPTION 1] SOCK_ERR Caught : " + str(se) + "\nConnection has been closed")
            self.sender_side_socket.close()
            sys.exit(1)

        print("\nChannel is currently active.\nSend data to get response from receiver.")
        self.packet_list = self.gen_pkt()
        while True:
            print("Choose the Data Link Layer Protocol:\n1. Stop and Wait\n2. Go Back N\n3. Selective Repeat")
            try: choice = int(input("\nEnter Your Choice (1, 2, 3 or 4 (Enter 0 to exit system)) : "))
            except ValueError as ve:
                print("[EXCEPTION 4] ValueError Caught : " + str(ve) + "\nOnly integer inputs are allowed. Try again -->")
                continue

            if choice == 0:
                print("\nExiting system.... Exited")
                self.sender_side_socket.close()
                sys.exit(1)

            elif choice == 1:
                for packet in self.packet_list:
                    encoded_data = str(stop_and_wait.encode(packet))
                    self.send_pkt(encoded_data, self.sender_side_socket)
                    self.ack = self.recv_ack(self.sender_side_socket)

            elif choice == 2:
                for packet in self.packet_list:
                    encoded_data = str(go_back_N.encode(packet))
                    self.send_pkt(encoded_data, self.sender_side_socket)
                    self.ack = self.recv_ack(self.sender_side_socket)

            elif choice == 3:
                for packet in self.packet_list:
                    encoded_data = str(selective_repeat.encode(packet))
                    self.send_pkt(encoded_data, self.sender_side_socket)
                    self.ack = self.recv_ack(self.sender_side_socket)

            else:
                print("\nINVALID INPUT! Input must be an integer b/w 1, 2 and 3")
                print("Enter your choice once again")


if __name__ == "__main__":
    sndr = Sender()
    print(sndr.gen_pkt())
