import sys
import const


def read_file(filename: str) -> str:
    try:
        with open(filename, "r") as fptr:
            data_str = fptr.read()
    except FileNotFoundError as fnfe:
        print("\n[READ_EXCEPTION] FILE_ERR Caught : " + str(fnfe))
        sys.exit(1)
    return data_str


def write_into_file(info: str, filename: str):
    try:
        with open(filename, "a+") as fptr:
            fptr.seek(0)
            data_str = fptr.read(100)
            if len(data_str) > 0: fptr.write("\n")
            fptr.write(info)
    except FileNotFoundError as fnfe:
        print("\n[WRITE_EXCEPTION] FILE_ERR Caught : " + str(fnfe))
        sys.exit(1)


def create_pkt(data: str) -> list[str]:
    data_length = len(data)
    packet_length = const.default_data_packet_size
    packet_count = int(data_length/packet_length)
    print("\nLength of data = " + str(data_length))
    print("Number of packets = " + str(packet_count))
    print("Length of each packet = " + str(packet_length))
    packet_list = []
    for i in range(packet_count):
        packet = data[i*packet_length: (i+1)*packet_length]
        packet_list.append(packet)
    return packet_list


if __name__ == "__main__":
    data = read_file("textfiles/input.txt")
    packet_list = create_pkt(data)
    print(packet_list)
