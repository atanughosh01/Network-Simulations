import sys
import time
import const
import random
import threading
from gen_packet import Packet


class Sender:

    #def __init__(self, name:int, file_name:str, sender_to_channel:socket.socket, channel_to_sender, collision_technique:int):
    def __init__(self, name:int, file_name:str, sender_to_channel, channel_to_sender, collision_technique:int):
        self.name                = name
        self.file_name           = file_name
        self.packet_type         = {'data' : 0, 'ack' : 1}
        self.dest                = self.select_receiver()
        self.sender_to_channel   = sender_to_channel
        self.channel_to_sender   = channel_to_sender
        self.timeout_event       = threading.Event()
        self.end_transmitting    = False
        self.start               = 0
        self.seq_no              = 0
        self.pkt_count           = 0
        self.collision_technique = collision_technique
        self.busy                = 0
        self.collision_count     = 0
        self.recent_packet       = None

    def select_receiver(self):
        return self.name

    def open_file(self, file_name):
        try: file = open(file_name, 'r', encoding='utf-8')
        except IOError: sys.exit("No file exit with name {} !".format(file_name))
        return file

    def send_data_with_one_persistent(self, packet):
        while True:
            if self.busy == 0:
                file = self.open_file("textfiles/collision.txt")
                collision = file.read()
                file.close()

                if collision == '1':
                    self.collision_count += 1
                    print("SENDER-{} -->> COLLISION".format(self.name+1))
                    time.sleep(const.collision_wait_time)
                else:
                    print("SENDER-{} -->> PACKET {} SENT TO CHANNEL".format(self.name+1, self.pkt_count+1))
                    file = open('textfiles/collision.txt', "w", encoding='utf-8')
                    file.write(str(1))
                    file.close()
                    time.sleep(const.vulnerable_time)
                    file = open('textfiles/collision.txt', "w",  encoding='utf-8')
                    file.write(str(0))
                    file.close()
                    self.sender_to_channel.send(packet) 
                    time.sleep(const.propagation_time)
                    break

            else:
                print("SENDER-{} -->> FOUND CHANNEL BUSY".format(self.name+1))
                time.sleep(0.5)
                continue

    def send_data_with_non_persistent(self, packet):
        while True:
            if self.busy == 0:
                file = self.open_file("textfiles/collision.txt")
                collision = file.read()
                file.close()

                if collision == '1':
                    self.collision_count += 1
                    print("SENDER-{} -->> COLLISION".format(self.name+1))
                    time.sleep(const.collision_wait_time)
                else:
                    print("SENDER-{} -->> PACKET {} SENT TO CHANNEL".format(self.name+1, self.pkt_count+1))
                    file = open('textfiles/collision.txt', "w",  encoding='utf-8')
                    file.write(str(1))
                    file.close()               
                    time.sleep(const.vulnerable_time)
                    file = open('textfiles/collision.txt', "w",  encoding='utf-8')
                    file.write(str(0))
                    file.close()
                    self.sender_to_channel.send(packet)
                    time.sleep(const.propagation_time)
                    break

            else:
                print("SENDER-{} -->> FOUND CHANNEL BUSY".format(self.name+1))
                time.sleep(const.non_persistant_waiting_time)
                continue

    def send_data_with_p_persistent(self, packet):
        while True:
            if self.busy == 0:
                prob = random.random()

                if(prob <= 0.5):
                    file = self.open_file("textfiles/collision.txt")
                    collision = file.read()
                    file.close()

                    if collision == '1':
                        self.collision_count += 1
                        print("SENDER-{} -->> COLLISION OCCURED".format(self.name+1))
                        time.sleep(const.collision_wait_time)
                    else:
                        print("SENDER-{} -->> PACKET {} SENT TO CHANNEL".format(self.name+1, self.pkt_count+1))
                        file = open('textfiles/collision.txt', "w",  encoding='utf-8')
                        file.write(str(1))
                        file.close()                         
                        time.sleep(const.vulnerable_time)
                        file = open('textfiles/collision.txt', "w",  encoding='utf-8')
                        file.write(str(0))
                        file.close()
                        self.sender_to_channel.send(packet) 
                        time.sleep(const.propagation_time)
                        break

                else:
                    print("SENDER-{} -->> WAITING".format(self.name+1))
                    time.sleep(const.time_slot)

            else:
                print("SENDER-{} -->> FOUND CHANNEL BUSY".format(self.name+1))
                time.sleep(0.5)
                continue

    def data_into_frames(self):
        print("SENDER-{} starts sending data to RECEIVER{}".format(self.name+1, self.dest+1))
        self.start = time.time()
        file = self.open_file(self.file_name)
        byte = file.read(const.default_datapacket_size)
        self.seq_no = 0
        while byte:
            packet = Packet(self.packet_type['data'], self.seq_no, byte, self.name, self.dest).make_pkt()
            self.recent_packet = packet
            if(self.collision_technique == 1): self.send_data_with_one_persistent(packet)
            elif(self.collision_technique == 2): self.send_data_with_non_persistent(packet)
            else: self.send_data_with_p_persistent(packet)
            self.pkt_count += 1
            byte = file.read(const.default_datapacket_size)
            if len(byte) == 0: break
            elif len(byte) < const.default_datapacket_size:
                temp_length = len(byte)
                for _ in range(const.default_datapacket_size - temp_length): byte += '\0'
        
        self.end_transmitting = True
        file.close()
        print("\n*****************SENDER-{} -->> STATS******************".format(self.name+1))
        print("Total packets: {}".format(self.pkt_count))
        print("Total Delay:", round(time.time() - self.start, 2), "secs")
        print("Total collisions: {}".format(self.collision_count))
        print("Throughput: {}\n".format(round(self.pkt_count/(self.pkt_count + self.collision_count), 3)))

    def sense_signal(self):
        while True:
            if(self.channel_to_sender.recv() == '1'): self.busy = 1
            else: self.busy = 0

    def initiate_sender_process(self):
        sending_thread = threading.Thread(name="sending_thread", target=self.data_into_frames)
        receiving_signal_thread = threading.Thread(name="receiving_signal_thread", target=self.sense_signal)

        sending_thread.start()
        receiving_signal_thread.start()

        sending_thread.join()
        receiving_signal_thread.join()
