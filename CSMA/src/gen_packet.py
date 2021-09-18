'''module for creating data frames, extraction of data and decoding addresses'''
# import checker
import checker


class Packet:

    def __init__(self, _type, seq_no, segment_data, sender, dest) -> None:
        self.type = _type
        self.segment_data = segment_data
        self.sender = sender
        self.dest = dest
        self.seq_no = seq_no
        self.packet = None

    #  preamble + sfd + dest + source + seqNo + len + data + cksum
    #     7     +  1  +  6   +   6    +  1    +  1  +  46  +   4  =  72

    def make_pkt(self):
        preamble = '01'*28
        sfd = '10101011'
        seq_to_bits = '{0:08b}'.format(int(self.seq_no))
        dest_address = '{0:048b}'.format(int(self.dest))
        length = '{0:008b}'.format(len(self.segment_data))
        src_address = '{0:048b}'.format(int(self.sender))
        data = ""
        for i in range(len(self.segment_data)):
            character = self.segment_data[i]
            data_byte = '{0:08b}'.format(ord(character))
            data = data + data_byte
        packet = preamble + sfd + dest_address + src_address + seq_to_bits + length + data
        ck_sum = checker.check_sum(packet)
        packet = packet + ck_sum
        self.packet = packet
        return self

    def __str__(self) -> str:
        return str(self.packet)

    def extract_data(self) -> str:
        text = ""
        data = self.packet[176:544]
        ascii_data = [data[i:i+8] for i in range(0, len(data), 8)]
        for letter in ascii_data:
            text += chr(int(letter, 2))
        return text

    def decode_length(self) -> int:
        return len(self.segment_data)

    def decode_dest_address(self) -> int:
        dest = self.packet[64:112]
        dest_address = int(dest, 2)
        return dest_address

    def decode_src_address(self) -> int:
        src = self.packet[112:160]
        src_address = int(src, 2)
        return src_address

    def check_for_error(self) -> bool:
        return checker.check_error(self.packet)

    def check_type(self):
        return self.type

    def decode_seq_no(self) -> int:
        seq_no = self.packet[160:168]
        return int(seq_no, 2)
