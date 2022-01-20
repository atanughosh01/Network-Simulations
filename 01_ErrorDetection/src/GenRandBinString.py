# Generates random binary string of given size
import random


def gen_rand_string(size: int) -> str:
    string = ""
    for _ in range(size):
        temp = str(random.randint(0, 1))
        string += temp
    return string


if __name__ == "__main__":
    # enter a positive integer for string generation
    n = int(input("Enter length of the string to be generated : "))
    bin_str = gen_rand_string(n)

    try:
        with open("textfiles/input.txt", "w") as text_file:
            text_file.write(bin_str)
    except FileNotFoundError as fnfe: print(str(fnfe))

    count1, count2 = 0, 0
    for i in bin_str:
        if i == '1': count1 += 1
        else: count2 += 1
    print("\nLength of generated binary string = " + str(len(bin_str)))
    print("No. of 1-s present = " + str(count1) + 
          "\nNo. of 0-s present = " + str(count2))
