'''module for generating check-sum and checking errors'''


def check_sum(seg_data: str) -> str:
    '''returns 32 bit checksum of given input'''
    total = 0
    data = [seg_data[i: i+32] for i in range(0, len(seg_data), 32)]
    for i in data:
        total += int(i, 2)
        if total >= 4294967295:
            total -= 4294967295

    cksum = 4294967295 - total
    cksum_bits = '{0:032b}'.format(cksum)
    return cksum_bits


def check_error(seg_data: str) -> bool:
    '''returns true if errors present else false'''
    total = 0
    data = [seg_data[i: i+32] for i in range(0, len(seg_data), 32)]
    for i in data:
        total += int(i, 2)
        if total >= 4294967295:
            total -= 4294967295
    return 1 if total == 0 else 0
