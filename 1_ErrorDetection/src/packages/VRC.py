
# generates even-parity for given string of 1-s and 0-s
def gen_VRC(data: str) -> str:
    count = 0
    for i in data:
        if i == '1':
            count += 1
    if count % 2 != 0:
        vrc_bit = '1'
    else:
        vrc_bit = '0'
    return vrc_bit


def main():
    data = "1001110001110"
    vrc = gen_VRC(data)
    data_word = data + vrc
    print("\nData = " + str(data) +
          "\nGenerated VRC = " + str(vrc) +
          "\nDataWord  = " + str(data_word) + "\n")


if __name__ == "__main__":
    main()
