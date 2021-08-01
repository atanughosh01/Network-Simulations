#include "../header/Packet.hpp"
#include "../header/Channel.hpp"
#include "../header/CRC.hpp"
#include "../header/Taint.hpp"

int main() try {
  
    Channel channel;
    Packet packet;
    channel.open(CHANNEL_NAME, SEMBUFFERFULL_NAME, SEMBUFFEREMPTY_NAME);
    len_t bufferLen = Packet::PACKET_LEN;
    byte_t buffer[bufferLen];
    bool tainted;
    while(true) {
        cout << "-[-]>";
        // cout.flush();
        packet.packFrame();
        packet.getFrame(buffer, bufferLen);
        // packet.printFrame();
        channel.write(buffer, bufferLen);
        
        for(indx_t i = 0; i < TAINT_TIMES; i++) {
            cout << "-[-]>";
            // cout.flush();
            packet.taintFrame();
            // packet.printFrame();
            packet.getFrame(buffer, bufferLen);
            channel.write(buffer, bufferLen);
        }        
    }

    return 0;
} catch (Error e) {
    e.show();
    return -1;
}
