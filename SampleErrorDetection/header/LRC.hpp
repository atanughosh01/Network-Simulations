#pragma once
#include "Constant.hpp"

class LRC {
public:
     lrc_t calc(byte_t data[], len_t len) {
    lrc_t lrc = 0;

    for(indx_t i = 0; i < len; i++) {
        lrc ^= data[i];
    }

    return lrc;
    }

     void insert(byte_t* data, lrc_t lrc) {
        *data = lrc;
    }

     bool isOk(byte_t data[], len_t len) {
        if (calc(data, len) == 0) {
            return true;
        }

        return false;
    }
};