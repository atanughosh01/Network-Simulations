#pragma once
#include "Constant.hpp"

class VRC {
public:
     vrc_t calc(byte_t data[], len_t len) {
        vrc_t vrc = 0;

        for(indx_t i = 0; i < len; i++) {
            vrc ^= data[i];
        }

        vrc = (vrc >> 0x4)^vrc;
        vrc = (vrc >> 0x2)^vrc;
        vrc = (vrc >> 0x1)^vrc;

        vrc &= 0x1;

        return vrc;
    }

     void insert(byte_t* data, vrc_t vrc) {
        *data = vrc;
    }

     bool isOk(byte_t data[], len_t len) {
        if (calc(data, len) == 0) {
            return true;
        }

        return false;
    }
};