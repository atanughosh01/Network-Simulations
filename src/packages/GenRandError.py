
# Generates error by flipping bits at specified number of indices of input string
import random


def gen_rand_error(data: str, count: int) -> str:
    length = len(data)
    digit_list = list(data)
    k = random.sample(range(0, length), count)
    for index in k:
        # This will replace 0-s at some positions with 1-s or 1-s with 0-s
        # Number of flipped bits = count
        if digit_list[index] == '1':
            digit_list[index] = digit_list[index].replace('1', '0')
        elif digit_list[index] == '0':
            digit_list[index] = digit_list[index].replace('0', '1')
    return ("".join(digit_list))


def main():
    string_to_modify = str(input("Enter the string to be modified : "))
    flip_count = int(input("Enter number of bits to be flipped : "))
    new_string = gen_rand_error(string_to_modify, flip_count)
    print("The modified String is : " + new_string)


if __name__ == "__main__":
    main()