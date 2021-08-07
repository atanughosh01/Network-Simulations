
import random
import packages.GenRandError as gre

with open("input.txt", "r") as file:
    data = file.read()

print("DATA = " + str(data))
string_length = len(data)
packet_count = 10
packet_length = int(string_length/packet_count)
print("\nLength of data = " + str(string_length))
print("Number of packets = " + str(packet_count))
print("Length of each packet = " + str(packet_length))

packet_list = []
for i in range(packet_count):
    k = packet_length
    packet = data[i*k: (i+1)*k]
    packet_list.append(packet)

print("\nOriginal Packet List :", packet_list)
# for i in packet_list:
#     print(len(i))

corrupt_packet_list = []
for packet in packet_list:
    corrupt_packet = gre.gen_rand_error(packet, random.randint(1, len(packet_list)))
    corrupt_packet_list.append(corrupt_packet)
    
print("\nCorrupted Packet List :", corrupt_packet_list)
