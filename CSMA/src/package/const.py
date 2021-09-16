'''values that remain constant throughout the flow of code are defined here'''
import random

total_sender_number = 8
total_receiver_number = 8

default_datapacket_size = 46
window_size = 2

vulnerable_time = 0.1   # data length / bandwidth
channel_propagation_time = 1
non_persistant_waiting_time = random.randint(1, 4)
time_slot = 0.25
collision_wait_time = 0.1

out_file_path = "/c/Users/2001a/Documents/GitHub/Network-Simulations/CSMA/src/textfiles/output/"

propagation_time = 0.8  # channel remains busy this time
collision_wait_time = 0.03
