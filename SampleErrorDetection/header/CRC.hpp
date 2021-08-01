#pragma once
#include "Constant.hpp"

class CRC {
    static const len_t crcTableLen = 26;
    static const crc_t poly = 0x8005;
    crc_t crcTable[crcTableLen];

     crc_t reflect(crc_t crc) {
        crc_t reflectedCrc = 0;

        for (indx_t i = 0; i < sizeof(crc_t); i++) {
            reflectedCrc <<= 8;
            reflectedCrc |= (crc&0xff);
            crc >>= 8;
        }

        return reflectedCrc;
    }
public:
     CRC() {
        crc_t remainder;
        const crc_t topbit = (1<<(sizeof(crc_t)*8 - 1));

        for(crc_t val = 0; val < crcTableLen; val++) {
            remainder = (val<<(sizeof(crc_t)*8 - 8));

            for(byte_t bit = 8; bit > 0; bit--) {
                if (remainder&topbit) {
                    remainder = (remainder<<1)^poly;
                } else {
                    remainder <<= 1;
                }
            }

            crcTable[val] = remainder;
        }
    }

     crc_t calc(byte_t data[], len_t len) {
        crc_t crc = 0;
        byte_t byte;

        for(indx_t i = 0; i < len; i++) {
            byte = data[i]^(crc>>(sizeof(crc_t)*8 - 8));
            crc = crcTable[byte]^(crc<<8);
        }

        return crc;
    }

     void insert(byte_t* data, crc_t crc) {
        *(crc_t *)data = reflect(crc);
    }

     bool isOk(byte_t data[], len_t len) {
        if (calc(data, len) == 0) {
            return true;
        }

        return false;
    }
};
