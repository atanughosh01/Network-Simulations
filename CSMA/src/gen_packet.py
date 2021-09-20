'''module for creating data frames, extraction of data and decoding addresses'''

import checker


class Packet:
    '''Packet Class to create packets from input data and decode each invidual component of the generated packet'''

    def __init__(self, _type, seq_no, segment_data, sender, dest) -> None:
        self.type = _type
        self.seq_no = seq_no
        self.segment_data = segment_data
        self.sender = sender
        self.dest = dest
        self.packet = None


    ########################  PACKET STRUCTURE  ########################
    #  preamble + sfd + dest + source + seq_no + len + data + cksum
    #     7     +  1  +  8   +   8    +    1   +  1  +  36  +   2  =  64
    ####################################################################


    def make_pkt(self):
        '''
        segment data need to be in string
        byte = file.read(1)...segmentdata += str(byte)
        everythong has to be in string
        returns packet obj
        '''
        preamble = '01'*28      # 7 bytes of alternating 01
        sfd = '10101011'        # start frame delimeter
        seq_to_bits = '{0:08b}'.format(int(self.seq_no))
        dest_address = '{0:064b}'.format(int(self.dest))
        length_to_bits = '{0:008b}'.format(len(self.segment_data))
        src_address = '{0:064b}'.format(int(self.sender))
        data = ""
        # print(len(self.segment_data))
        for i in range(len(self.segment_data)):
            character = self.segment_data[i]
            data_byte = '{0:08b}'.format(ord(character))
            data = data + data_byte
        # print(len(src_address))
        packet = preamble + sfd + dest_address + src_address + seq_to_bits + length_to_bits + data
        ck_sum = checker.check_sum(packet)
        packet = packet + ck_sum
        self.packet = packet
        return self

    def __str__(self) -> str:
        return str(self.packet)

    def extract_data(self) -> str:
        '''Extracts the original raw data from the generated packets'''
        text = ""
        length = len(self.segment_data)
        data = self.packet[208:(208+(8*length))]
        ascii_data = [data[i:i+8] for i in range(0, len(data), 8)]
        for letter in ascii_data:
            text += chr(int(letter, 2))
        return text

    def decode_length(self) -> int:
        '''Decodes length of segment data'''
        return len(self.segment_data)

    def decode_dest_address(self) -> int:
        '''Decodes Destination Address from the generated packet'''
        dest = self.packet[64:128]
        dest_address = int(dest, 2)
        return dest_address

    def decode_src_address(self) -> int:
        '''Decodes Source Address from the generated packet'''
        src = self.packet[128:192]
        src_address = int(src, 2)
        return src_address

    def check_for_error(self) -> bool:
        '''Checks for error in the packets (based on CheckSum Error Detection technique)'''
        return checker.check_error(self.packet)

    def check_type(self):
        '''Checks type of generated packet'''
        return self.type

    def decode_seq_no(self) -> int:
        '''Decodes sequence number from the generated packet'''
        seq_no = self.packet[192:200]
        return int(seq_no, 2)
