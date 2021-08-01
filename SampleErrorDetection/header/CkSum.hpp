#pragma once

#include "Constant.hpp"

class CkSum {
public:
     cksum_t calc(byte_t data[], len_t len) {
        uint32_t sum = 0;

        while(len > 1) {
            sum += *(uint16_t *)(data);
            data += sizeof(uint16_t);
            len -= sizeof(uint16_t);
        }

        if(len > 0) {
            sum += *data;
        }

        while(sum>>16) {
            sum = (sum&0xffff)+(sum>>16);
        }

        return ~(uint16_t)(sum);
    }

     void insert(byte_t* data, cksum_t cksum) {
        *(cksum_t *)data = cksum; 
    }

     bool isOk(byte_t data[], len_t len) {
        if (calc(data, len) == 0) {
            return true;
        }

        return false;
    }
};