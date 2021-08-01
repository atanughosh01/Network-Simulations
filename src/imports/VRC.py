sent_data = "1001110001110"


def VRC(data):
    count = 0
    for i in data:
        if i == '1':
            count += 1

    if count % 2 != 0:
        VRC_BIT = 1
        data += str(VRC_BIT)
        count += 1
    else:
        VRC_BIT = 0

    print("New Data Frame = " + str(data) + "\nCount of 1-s = " + str(count) + ", VRC_BIT = "+str(VRC_BIT))


def main():
    VRC(sent_data)

if __name__ == "__main__":
    main()
