import random
import GenRandError as gre

with open("input.txt", "r") as file:
    info = file.read()
string_length = len(info)
packet_count = 20
packet_length = int(string_length/packet_count)

packet_list = []
for i in range(packet_count):
    k = packet_length
    packet = info[i*k: (i+1)*k]
    packet_list.append(packet)

corrupt_packet_list = []
for packet in packet_list:
    corrupt_packet = gre.gen_rand_error(packet, random.randint(0, 8))
    corrupt_packet_list.append(corrupt_packet)
    
print(corrupt_packet_list)
