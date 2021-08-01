
def gen_CheckSum(data, k):

    b1 = data[0:k]
    b2 = data[k:2*k]
    b3 = data[2*k:3*k]
    b4 = data[3*k:4*k]

    bin_sum = bin(int(b1, 2) + int(b2, 2) + int(b3, 2) + int(b4, 2))[2:]

    # print("Length of sent data = " + str(len(data)) +
    #       "\nNumber of packets = " + str(packet_count) +
    #       "\nLength of each packet = " + str(k) +
    #       "\nBinary sum of packets = " + str(bin_sum) +
    #       "\nLength of sum of packets = " + str(len(bin_sum)))

    if len(bin_sum) > k:
        c = len(bin_sum) - k
        carry = bin_sum[0:c]
        bin_sum = bin_sum[c:]
        print("\nCarry = " + str(carry) +
              ", Initial binary sum = " + str(bin_sum))
        bin_sum = bin(int(bin_sum, 2) + int(carry, 2))[2:]
        print("Final binary sum of packets = " + str(bin_sum))

    elif len(bin_sum) < k:
        c = k - len(bin_sum)
        bin_sum = '0'*c + bin_sum
        print("Final binary sum = " + str(bin_sum))

    check_sum = ""
    for i in bin_sum:
        if int(i) == 1:
            check_sum += "0"
        elif int(i) == 0:
            check_sum += "1"
    print("CheckSum = " + str(check_sum))
    return check_sum


def main():
    data = "10010101011000111001010011101100"
    packet_count = 4
    packet_length = int(len(data)/packet_count)
    print("Length of sent data = " + str(len(data)) +
          "\nNumber of packets = " + str(packet_count) +
          "\nLength of each packet = " + str(k) +
          "\nBinary sum of packets = " + str(bin_sum) +
          "\nLength of sum of packets = " + str(len(bin_sum)))
    gen_CheckSum(data, packet_length)


if __name__ == "__main__":
    main()
