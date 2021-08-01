#include "../header/Channel.hpp"
#include "../header/Constant.hpp"

#include "signal.h"
#include "unistd.h"

bool stop = false;

void handle(int signal) {
    stop = true;
}

int main() try{
    signal(SIGINT, handle);

    Channel channel;
    channel.init(CHANNEL_NAME, SEMBUFFERFULL_NAME, SEMBUFFEREMPTY_NAME);

    while(!stop) {
        sleep(2);
        cout << "-[-]-";
        cout.flush();
    }

    channel.close();
    return 0;
} catch(Error e) {
    e.show();
    return -1;
}
