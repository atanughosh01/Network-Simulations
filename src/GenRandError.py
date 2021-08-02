
import random


def gen_rand_error(data, count):
    length = len(data)
    digit_list = list(data)
    k = random.sample(range(0, length), count)
    for index in k:
        # This will replace digits at the specified index with 0 or 1
        if digit_list[index] == '1':
            digit_list[index] = digit_list[index].replace('1', '0')
        elif digit_list[index] == '0':
            digit_list[index] = digit_list[index].replace('0', '1')
    return ("" . join(digit_list))


def main():
    string_to_modify = str(input("Enter the string to be modified : "))
    total_places = int(input("Enter number of digits to be modified : "))
    new_string = gen_rand_error(string_to_modify, total_places)
    print("The modified String is : " + new_string)


if __name__ == "__main__":
    main()
