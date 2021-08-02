
def gen_LRC(data):
    lrc = data[0:4]
    return lrc


def main():
    data = "1000011001111100001111000010001"
    lrc = gen_LRC(data)
    data_word = data + lrc
    print("\nData = " + str(data) +
          "\nGenerated LRC = " + str(lrc) +
          "\nDataWord  = " + str(data_word) + "\n")


if __name__ == "__main__":
    main()
