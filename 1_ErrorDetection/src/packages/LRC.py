# generates even-parity for given string of 1-s and 0-s
def gen_VRC(data: str) -> str:
    count = 0
    for i in data:
        if i == '1': count += 1
    if count % 2 != 0: vrc_bit = '1'
    else: vrc_bit = '0'
    return vrc_bit

# generates 2-D parity for given data string
def gen_LRC(data: str) -> str:
    packet_list = []
    for count in range(0, 32, 8):
        packet = data[count: count+8]
        if len(packet) < 8:
            packet = '0'*(8-len(packet)) + packet
        packet_list.append(packet)

    lrc_bit = ""
    for i in range(0, 8):
        temp = ""
        for j in range(0, 4): temp += packet_list[j][i]
        lrc_bit += gen_VRC(temp)

    return lrc_bit


if __name__ == "__main__":
    # data = "1000011001111100001111000010001"
    data = "11111111111100001010101010010010"
    lrc = gen_LRC(data)
    data_word = data + lrc
    print("\nData = " + str(data) +
          "\nGenerated LRC = " + str(lrc) +
          "\nDataWord  = " + str(data_word) + "\n")
 