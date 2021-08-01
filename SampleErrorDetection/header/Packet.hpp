#pragma once
#include "Constant.hpp"
#include "VRC.hpp"
#include "LRC.hpp"
#include "CkSum.hpp"
#include "CRC.hpp"
#include "Error.hpp"
#include "Taint.hpp"
#include "Log.hpp"
#include "ctime"

using namespace std;

class Packet {
public:
    static const len_t PACKET_LEN = 64;
    static const byte_t VRC_CORRUPT = 0x01;
    static const byte_t LRC_CORRUPT = VRC_CORRUPT<<1;
    static const byte_t CKSUM_CORRUPT = LRC_CORRUPT<<1;
    static const byte_t CRC_CORRUPT = CKSUM_CORRUPT<<1;
private:
    static const indx_t CRC_INDX = PACKET_LEN - sizeof(crc_t);
    static const indx_t CKSUM_INDX = CRC_INDX - sizeof(cksum_t);
    static const indx_t LRC_INDX = CKSUM_INDX - sizeof(lrc_t);
    static const indx_t VRC_INDX = LRC_INDX - sizeof(lrc_t);

    static const len_t CRC_LEN = CRC_INDX + sizeof(crc_t);
    static const len_t CKSUM_LEN = CKSUM_INDX + sizeof(cksum_t);
    static const len_t LRC_LEN = LRC_INDX + sizeof(lrc_t);
    static const len_t VRC_LEN = VRC_INDX + sizeof(vrc_t);

    byte_t frame[PACKET_LEN];
    minstd_rand0 generator;

    VRC VRCInstance;
    CRC CRCInstance;
    CkSum CkSumInstance;
    LRC LRCInstance;
    Taint TaintInstance;
public:
    Packet() {        
        for(indx_t i = 0; i < PACKET_LEN; i++) {
            frame[i] = i;
        }
        minstd_rand0 gnrtr(time(NULL));
        generator = gnrtr;
    }

    void packFrame() {
        vrc_t vrc = VRCInstance.calc(frame, VRC_INDX);
        VRCInstance.insert(frame+VRC_INDX, vrc);

        lrc_t lrc = LRCInstance.calc(frame, LRC_INDX);
        LRCInstance.insert(frame+LRC_INDX, lrc);

        cksum_t cksum = CkSumInstance.calc(frame, CKSUM_INDX);
        CkSumInstance.insert(frame+CKSUM_INDX, cksum);

        crc_t crc = CRCInstance.calc(frame, CRC_INDX);
        CRCInstance.insert(frame+CRC_INDX, crc);
    }

    void taintFrame() {
        if (generator()%7 == 0) {
            TaintInstance.taintBurst(frame, PACKET_LEN);
        } else {
            TaintInstance.taintBit(frame, PACKET_LEN);
        }
    }

    void getFrame(byte_t buffer[], len_t len) {
        Error error;
        error.className("Packet");
        error.funcName("getFrame");

        if (len < PACKET_LEN) {
            error.problemIs("Buffer length is less than packet length");
            throw error;
        }

        for(indx_t i = 0; i < len; i++) {
            buffer[i] = frame[i];
        }
    }

    void unpackFrame(byte_t buffer[], len_t len) {
        Error error;
        error.className("Packet");
        error.funcName("unpackFrame");

        if (len < PACKET_LEN) {
            error.problemIs("Buffer length is less than packet length");
            throw error;
        }

        for(indx_t i = 0; i < len; i++) {
            frame[i] = buffer[i];
        }
    }

    byte_t checkError() {
        byte_t tmp = 0;

        if(!VRCInstance.isOk(frame, VRC_LEN)) {
            tmp |= VRC_CORRUPT;
        }

        if(!LRCInstance.isOk(frame, LRC_LEN)) {
            tmp |= LRC_CORRUPT;
        }

        if(!CkSumInstance.isOk(frame, CKSUM_LEN)) {
            tmp |= CKSUM_CORRUPT;
        }

        if(!CRCInstance.isOk(frame, CRC_LEN)) {
            tmp |= CRC_CORRUPT;
        }

        return tmp;
    }

    void printFrame() {
        printf("\n\n\n");
        for(indx_t i = 0; i < PACKET_LEN; i++) {
            printf("%02X", frame[i]);
        }
        printf("\n");
    }

    friend byte_t packetCompare(Packet& p1, Packet& p2);
};

byte_t packetCompare(Packet& untainted, Packet& tainted) {
    Error error;
    error.className("None");
    error.funcName("packetCompare");

    bool isSame = true;
    byte_t checkErrorVal = tainted.checkError();
    byte_t logErrorVal = Log::NONE_ER;
    
    for(indx_t i = 0; i < Packet::VRC_LEN; i++) {
        if(untainted.frame[i] != tainted.frame[i]) {
            isSame = false;
        }
    }

    if(isSame&& (checkErrorVal&Packet::VRC_CORRUPT)) {
        error.problemIs("VRC Algorithm not working");
        throw error;
    } else if (!isSame && !(checkErrorVal&Packet::VRC_CORRUPT)) {
        logErrorVal |= Log::VRC_ER;
    }

    for(indx_t i = Packet::VRC_LEN; i < Packet::LRC_LEN; i++) {
        if(untainted.frame[i] != tainted.frame[i]) {
            isSame = false;
        }
    }
    
    if(isSame&& (checkErrorVal&Packet::LRC_CORRUPT)) {
        error.problemIs("LRC Algorithm not working");
        throw error;
    } else if (!isSame && !(checkErrorVal&Packet::LRC_CORRUPT)) {
        logErrorVal |= Log::LRC_ER;
    }

    for(indx_t i = Packet::LRC_LEN; i < Packet::CKSUM_LEN; i++) {
        if(untainted.frame[i] != tainted.frame[i]) {
            isSame = false;
        }
    }
    
    if(isSame&& (checkErrorVal&Packet::CKSUM_CORRUPT)) {
        error.problemIs("CheckSum Algorithm not working");
        throw error;
    } else if (!isSame && !(checkErrorVal&Packet::CKSUM_CORRUPT)) {
        logErrorVal |= Log::CKSUM_ER;
    }

    for(indx_t i = Packet::CKSUM_LEN; i < Packet::CRC_LEN; i++) {
        if(untainted.frame[i] != tainted.frame[i]) {
            isSame = false;
        }
    }
    
    if(isSame&& (checkErrorVal&Packet::CRC_CORRUPT)) {
        error.problemIs("CRC Algorithm not working");
        throw error;
    } else if (!isSame && !(checkErrorVal&Packet::CRC_CORRUPT)) {
        logErrorVal |= Log::CRC_ER;
    }

    return logErrorVal;
}