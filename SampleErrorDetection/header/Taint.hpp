#pragma once
#include "Constant.hpp"

#include "random"

using namespace std;

class Taint {
     static const len_t bitTaintTableLen = 8;
     static const len_t burstTaintTableLen = 247;

     byte_t bitTaintTable[bitTaintTableLen];
     byte_t burstTaintTable[burstTaintTableLen];

     minstd_rand0 generator;
public:
    Taint() {
        byte_t tmp = 1;
        for (indx_t i = 0; i < bitTaintTableLen; i++) {
            bitTaintTable[i] = tmp;
            tmp <<= 1;
        }

        bool isPresent;
        indx_t i = 0;
        byte_t val = 1;

        while (i < burstTaintTableLen) {
            isPresent = false;

            for (indx_t j = 0; j < bitTaintTableLen; j++) {
                if(bitTaintTable[j] == val) {
                    isPresent = true;
                    break;
                }
            }

            if (!isPresent) {
                burstTaintTable[i] = val;
                i++;
            }

            val++;
        }

        minstd_rand0 gnrtr(time(NULL));
        generator = gnrtr;
    }

     void taintBit(byte_t data[], len_t len) {
        indx_t i = generator();
        indx_t j = generator()%bitTaintTableLen;

        data[i] ^= bitTaintTable[j];
    }

     void taintBurst(byte_t data[], len_t len) {
        indx_t i = generator()%len;
        indx_t j = generator()%burstTaintTableLen;

        data[i] ^= burstTaintTable[j];
    }
};
