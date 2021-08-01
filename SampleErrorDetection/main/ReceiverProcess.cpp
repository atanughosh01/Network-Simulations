#include "../header/Packet.hpp"
#include "../header/Channel.hpp"
#include "../header/Constant.hpp"
#include "../header/Log.hpp"

#include "signal.h"
#include "unistd.h"

bool stop = false;

void handle(int signal) {
    stop = true;
}

int main() try {
    signal(SIGINT, handle);

    Channel channel;
    channel.open(CHANNEL_NAME, SEMBUFFERFULL_NAME, SEMBUFFEREMPTY_NAME);

    Log log;
    Packet untaintedPacket, taintedPacket;

    bool tainted;
    len_t bufferLen = Packet::PACKET_LEN;
    byte_t taintedBuffer[bufferLen];
    byte_t untaintedBuffer[bufferLen];
    byte_t errorType;

    while(!stop) {
        channel.read(untaintedBuffer, bufferLen);
        untaintedPacket.unpackFrame(untaintedBuffer, bufferLen);
        // untaintedPacket.printFrame();
        errorType = packetCompare(untaintedPacket, untaintedPacket);
        log.write(untaintedBuffer, untaintedBuffer, bufferLen, errorType);

        for(indx_t i = 0; i < TAINT_TIMES; i++) {
            channel.read(taintedBuffer, bufferLen);
            taintedPacket.unpackFrame(taintedBuffer, bufferLen);
            // taintedPacket.printFrame();
            errorType = packetCompare(untaintedPacket, taintedPacket);
            log.write(untaintedBuffer, taintedBuffer, bufferLen, errorType);
        }
    }

    log.endStats();
} catch (Error e) {
    e.show();
}
