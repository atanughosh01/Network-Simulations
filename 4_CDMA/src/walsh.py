'''Walsh CEncoding Function'''

def get_next_powerof2(num):
    power = 1
    while power < num:
        power *= 2
    return power


def build_walsh_table(length, i1, i2, j1, j2, is_complement):
    if length == 2:
        if not is_complement:
            wls_table[i1][j1] = 1
            wls_table[i1][j2] = 1
            wls_table[i2][j1] = 1
            wls_table[i2][j2] = -1
        else:
            wls_table[i1][j1] = -1
            wls_table[i1][j2] = -1
            wls_table[i2][j1] = -1
            wls_table[i2][j2] = 1

        return

    mid_i = (i1+i2)//2
    mid_j = (j1+j2)//2

    build_walsh_table(length/2, i1, mid_i, j1, mid_j, is_complement)
    build_walsh_table(length/2, i1, mid_i, mid_j+1, j2, is_complement)
    build_walsh_table(length/2, mid_i+1, i2, j1, mid_j, is_complement)
    build_walsh_table(length/2, mid_i+1, i2, mid_j+1, j2, not is_complement)

    return


if __name__ == "__main__":
    num_of_stations = int(input("Enter Number of Stations : "))
    NUM = get_next_powerof2(num_of_stations)
    wls_table = [[0 for _ in range(NUM)] for _ in range(NUM)]

    build_walsh_table(NUM, 0, NUM - 1, 0, NUM - 1, False)
    print(wls_table)
    print(len(wls_table[0]))
    print(NUM)
