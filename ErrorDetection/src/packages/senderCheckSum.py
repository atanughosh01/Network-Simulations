# Performs binary sum betwwen 4 binary numbers with carry added back to the sum
def binary_sum(x1, x2, x3, x4, k):
    bin_sum = bin(int(x1, 2) + int(x2, 2) + int(x3, 2) + int(x4, 2))[2:]
    while len(bin_sum) > k:
        c = len(bin_sum) - k
        carry = bin_sum[0:c]
        bin_sum = bin_sum[c:]
        bin_sum = bin(int(bin_sum, 2) + int(carry, 2))[2:]

    if len(bin_sum) < k:
        c = k - len(bin_sum)
        bin_sum = '0'*c + bin_sum

    return bin_sum


# Generates CheckSum for given data and packet-length
def gen_CheckSum(data: str, k: int) -> str:
    b1 = data[0:k]
    b2 = data[k:2*k]
    b3 = data[2*k:3*k]
    b4 = data[3*k:4*k]
    bin_sum = binary_sum(b1, b2, b3, b4, k)
    s_cksum = ""
    for i in bin_sum:
        if i == '1': s_cksum += '0'
        else: s_cksum += '1'
    return s_cksum


# Main() method to implement functionalities
if __name__ == "__main__":
    data = "10010101011000111001010011101100"
    packet_count = 4
    packet_length = int(len(data)/packet_count)
    sender_check_sum = gen_CheckSum(data, packet_length)
    data_word = data + sender_check_sum
    print("\nData = " + str(data) +
          "\nLength of sent data = " + str(len(data)) +
          "\nNumber of packets = " + str(packet_count) +
          "\nLength of each packet = " + str(packet_length) +
          "\nGenerated CheckSum = " + str(sender_check_sum) +
          "\nLength of CheckSum = " + str(len(sender_check_sum)) +
          "\nDataWord = " + str(data_word) +
          "\nLength of DataWord = " + str(len(data_word)) + "\n")
