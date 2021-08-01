
def binary_sum(x1, x2, x3, x4, k):
    bin_sum = bin(int(x1, 2) + int(x2, 2) + int(x3, 2) + int(x4, 2))[2:]

    if len(bin_sum) > k:
        c = len(bin_sum) - k
        carry = bin_sum[0:c]
        bin_sum = bin_sum[c:]
        bin_sum = bin(int(bin_sum, 2) + int(carry, 2))[2:]

    elif len(bin_sum) < k:
        c = k - len(bin_sum)
        bin_sum = '0'*c + bin_sum

    return bin_sum


def gen_CheckSum(data, k):
    b1 = data[0:k]
    b2 = data[k:2*k]
    b3 = data[2*k:3*k]
    b4 = data[3*k:4*k]

    cksum = binary_sum(b1, b2, b3, b4, k)
    return cksum


def main():
    data = "10010101011000111001010011101100"
    packet_count = 4
    packet_length = int(len(data)/packet_count)
    check_sum = gen_CheckSum(data, packet_length)
    data_word = data + check_sum
    print("\nData = " + str(data) +
          "\nLength of sent data = " + str(len(data)) +
          "\nNumber of packets = " + str(packet_count) +
          "\nLength of each packet = " + str(packet_length) +
          "\nGenerated CheckSum = " + str(check_sum) +
          "\nLength of CheckSum = " + str(len(check_sum)) +
          "\nDataWord = " + str(data_word) + "\n")


if __name__ == "__main__":
    main()
