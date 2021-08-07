
import random
import packages.VRC as vrc
import packages.LRC as lrc
import packages.CRC as crc
import packages.GenRandError as gre
import packages.senderCheckSum as scs

with open("input.txt", "r") as file:
    data = file.read()

print("DATA = " + str(data))
string_length = len(data)
packet_length = 32
packet_count = int(string_length/packet_length)
print("\nLength of data = " + str(string_length))
print("Number of packets = " + str(packet_count))
print("Length of each packet = " + str(packet_length))

packet_list = []
for i in range(packet_count):
    k = packet_length
    packet = data[i*k: (i+1)*k]
    packet_list.append(packet)

print("\nOriginal Packet List :", packet_list)

# code_word_list = []
# for packet in packet_list:
#     VRC_DATA = vrc.gen_VRC(packet)
#     code_word = packet + VRC_DATA
#     code_word_list.append(code_word)

# code_word_list = []
# for packet in packet_list:
#     LRC_DATA = lrc.gen_LRC(packet)
#     code_word = packet + LRC_DATA
#     code_word_list.append(code_word)

# key = input("\nEnter the key for CRC-bit generation : ")
# code_word_list = []
# for packet in packet_list:
#     CRC_DATA = crc.gen_CRC(packet, key)
#     code_word = packet + CRC_DATA
#     code_word_list.append(code_word)

code_word_list = []
for packet in packet_list:
    CKSUM = scs.gen_CheckSum(packet, 8)
    code_word = packet + CKSUM
    code_word_list.append(code_word)

print("\nCode-Word List :", code_word_list)

for i in code_word_list:
    l = len(i)
print("\nLength of each Code-Word = " + str(l))

corrupt_packet_list = []
for packet in packet_list:
    corrupt_packet = gre.gen_rand_error(packet, random.randint(1, len(packet_list)))
    corrupt_packet_list.append(corrupt_packet)
    
print("\nCorrupted Packet List :", corrupt_packet_list)
