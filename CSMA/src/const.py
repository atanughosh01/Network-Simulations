'''module for defining values that remain constant throughout the flow during execution'''
import random

total_sender_number = 8
total_receiver_number = 8

default_datapacket_size = 46
window_size = 2

vulnerable_time = 0.1   # data length / bandwidth
propagation_time = 1
non_persistant_waiting_time = random.randint(1, 4)
time_slot = 0.25
collision_wait_time = 0.1

outfile_path = "/Users/2001a/Documents/GitHub/Network-Simulations/CSMA/src/textfiles/output/"

channel_propagation_time = 0.8  # channel remains busy this time
collision_wait_time = 0.03


'''
segment_data = [12, 234, 451, 90, 7]

if __name__ == "__main__":

    for i in range(len(segment_data)):
        print(segment_data[i])

    print("\n---------------------------\n")

    for tup in enumerate(segment_data):
        print(tup[0], '\t', tup[1])
'''
