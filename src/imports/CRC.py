
# Performs XOR betwwen two binary numbers reprensented as String
def xor(x, y):
    result = ""
    for i in range(1, len(y)):
        if x[i] == y[i]:
            result += "0"
        else:
            result += "1"
    return result


# Performs Modulo-2 division
def mod2div(divident, divisor):
    divisor_length = len(divisor)

    # Slicing the divident to appropriate length for particular step
    tmp = divident[0: divisor_length]
    while divisor_length < len(divident):
        if tmp[0] == '1':
            # replace the divident by the result of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + divident[divisor_length]
        else:
            tmp = xor('0'*divisor_length, tmp) + divident[divisor_length]

        # increment divisor_length to move further
        divisor_length += 1

    # For the last n bits, we have to carry it out normally as increased value of
    # divisor_length will cause IndexOutOfBounds exception.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*divisor_length, tmp)

    # Returns the remainder of the division
    rem = tmp
    return rem


# Takes the dataword and key as inputs and generates CRC based on that
def gen_CRC(data, key):
    key_length = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data + '0'*(key_length-1)
    crc = mod2div(appended_data, key)
    return crc


def main():
    data = "100100011110"
    key = "10011"
    crc = gen_CRC(data, key)
    data_word = data + crc
    print("Data = " + str(data) + ", Key = " + str(key))
    print("Generated CRC = " + str(crc) + "\nDataWord  = " + str(data_word))


if __name__ == "__main__":
    main()
