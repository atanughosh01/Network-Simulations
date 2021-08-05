
def gen_VRC(data: str) -> str:
    count = 0
    for i in data:
        if i == '1':
            count += 1
    if count % 2 != 0:
        VRC_BIT = '1'
    else:
        VRC_BIT = '0'
    return VRC_BIT


def main():
    data = "1001110001110"
    vrc = gen_VRC(data)
    data_word = data + vrc
    print("\nData = " + str(data) +
          "\nGenerated VRC = " + str(vrc) +
          "\nDataWord  = " + str(data_word) + "\n")


if __name__ == "__main__":
    main()
