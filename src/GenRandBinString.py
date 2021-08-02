# Generates random binary string of given size

import sys
import random

def gen_rand_string(size):
    string = ""
    for i in range(size):
        temp = str(random.randint(0, 1))
        string += temp
    return string

try:
    # enter an integer of multiple of 8 for understanable string generation
    n = int(input("Enter length of the string to be generated : "))
    bin_str = gen_rand_string(n)
except:
    print("ERROR! Only integer inputs are accepted")
    sys.exit()

with open("input.txt", "w") as text_file:
    text_file.write(bin_str)

print("Random binary string of taken length is : " + bin_str)
