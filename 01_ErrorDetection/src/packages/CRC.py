# Performs XOR betwwen two binary numbers reprensented as strings
def xor(x: str, y: str) -> str:
    result = ""
    for i in range(1, len(y)):
        if x[i] == y[i]: result += "0"
        else: result += "1"
    return result


# Performs Modulo-2 division
def mod2div(dividend: str, divisor: str) -> str:
    divisor_length = len(divisor)
    tmp = dividend[0: divisor_length]
    while divisor_length < len(dividend):
        if tmp[0] == '1':
            # replace the dividend by the result of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + dividend[divisor_length]
        else:
            tmp = xor('0'*divisor_length, tmp) + dividend[divisor_length]
        divisor_length += 1

    # For the last n bits, we have to carry it out normally as increased value of
    # divisor_length will cause IndexOutOfBoundsException.
    if tmp[0] == '1': tmp = xor(divisor, tmp)
    else: tmp = xor('0'*divisor_length, tmp)
    rem = tmp
    return rem


# Generates CRC for given data and key
def gen_CRC(data: str, key: str) -> str:
    key_length = len(key)
    appended_data = data + '0'*(key_length-1)
    crc = mod2div(appended_data, key)
    return crc


# Main() method to implement functionalities
if __name__ == "__main__":
    data = "100100011110"
    key = "10011"
    crc = gen_CRC(data, key)
    data_word = data + crc
    print("\nData = " + str(data) + "\nKey = " + str(key) +
          "\nGenerated CRC = " + str(crc) + "\nDataWord  = " + str(data_word) + "\n")
