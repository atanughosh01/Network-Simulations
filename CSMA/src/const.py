'''module for defining values that remain constant throughout the flow during execution'''

import random


# window_size = 3
total_sender_number = 2
total_receiver_number = 2
default_datapacket_size = 36


####################################
# sender constants
####################################
time_slot = 0.25
propagation_time = 1            # sender remains busy this time
vulnerable_time = 0.1           # data length / bandwidth
collision_wait_time = 0.1
non_persistant_waiting_time = random.randint(1, 4)


####################################
# receiver constants
####################################
outfile_path = "/Users/2001a/Documents/GitHub/Network-Simulations/CSMA/src/textfiles/output/"


####################################
# channel constants
####################################
channel_propagation_time = 0.8  # channel remains busy this time
