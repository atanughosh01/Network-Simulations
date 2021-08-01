#pragma once
#include "Constant.hpp"

#include "iostream"
#include "iomanip"
#include "cstdint"

using namespace std;

class Log {
    static const cnt_t MAXERROR = 256;
    cnt_t logCnt;
    cnt_t numPackets;

    cnt_t vrcError;
    cnt_t lrcError;
    cnt_t cksumError;
    cnt_t crcError;

    byte_t skip;
public:
    static const byte_t NONE_ER = 0x0;
    static const byte_t VRC_ER = 0x1;
    static const byte_t LRC_ER = VRC_ER<<1;
    static const byte_t CKSUM_ER = LRC_ER<<1;
    static const byte_t CRC_ER = CKSUM_ER<<1;

    Log() {        
        logCnt = 0;
        numPackets = 0;
        vrcError = 0;
        crcError = 0;
        lrcError = 0;
        cksumError = 0;
        skip = 0;
    }

    cnt_t getNumPackets() {
        return numPackets;
    }

    void write(byte_t untaintedData[], byte_t taintedData[], len_t len, byte_t errorType) {
        numPackets++;
        if(errorType == NONE_ER) {
            return;
        } else if (skip > 0 && ((errorType|skip) == skip)) {
            if(errorType&VRC_ER) {
                vrcError++;
            }

            if(errorType&LRC_ER) {
                lrcError++;
            }

            if(errorType&CKSUM_ER) {
                cksumError++;
            }

            if(errorType&CRC_ER) {
                crcError++;
            }
            
            return;
        }
        
        logCnt++;
        printf("\n\n-------------------%ld--------------------\n\n", logCnt);
        
        if(VRC_ER&errorType) {
            vrcError++;
            printf("VRC Failed - %ld out of %ld\n", vrcError, numPackets);
        }

        if(vrcError == MAXERROR) {
            skip |= VRC_ER;
        }

        if(LRC_ER&errorType) {
            lrcError++;
            printf("LRC Failed - %ld out of %ld\n", lrcError, numPackets);
        }

        if(lrcError == MAXERROR) {
            skip |= LRC_ER;
        }

        if(CKSUM_ER&errorType) {
            cksumError++;
            printf("CheckSum Failed - %ld out of %ld\n", cksumError, numPackets);
        }

        if(cksumError == MAXERROR) {
            skip |= CKSUM_ER;
        }

        if(CRC_ER&errorType) {
            crcError++;
            printf("CRC Failed - %ld out of %ld\n", crcError, numPackets);
        }

        if(crcError == MAXERROR) {
            skip |= CRC_ER;
        }

        for(indx_t i = 0; i < len; i++) {
            printf("%02X", untaintedData[i]);
        }

        printf("\n");

        for(indx_t i = 0; i < len; i++) {
            printf("%02X", taintedData[i]);
        }
        printf("\n");
        byte_t tmp;

        for(indx_t i = 0; i < len; i++) {
            tmp = taintedData[i]^untaintedData[i];

            if(tmp) {
                if(tmp>>4) {
                    printf("^_");
                } else {
                    printf("_^");
                }
            } else {
                printf("__");
            }
        }

        printf("\n\n-------------------%ld--------------------\n\n", logCnt);
    }

    void endStats() {
        double vrcFailure = double(vrcError)/double(numPackets) * 100;
        double lrcFailure = double(lrcError)/double(numPackets) * 100;
        double cksumFailure = double(cksumError)/double(numPackets) * 100;
        double crcFailure = double(crcError)/double(numPackets) * 100;

        printf("\n\n######### %ld ########\n\n", numPackets);
        printf("VRC Failed - %ld out of %ld, %lf\n", vrcError, numPackets, vrcFailure);
        printf("LRC Failed - %ld out of %ld, %lf\n", lrcError, numPackets, lrcFailure);
        printf("CheckSum Failed - %ld out of %ld, %lf\n", cksumError, numPackets, cksumFailure);
        printf("CRC Failed - %ld out of %ld, %lf\n", crcError, numPackets, crcFailure);
        printf("\n\n######### %ld ########\n\n", numPackets);
    }
};