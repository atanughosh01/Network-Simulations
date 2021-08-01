#!/bin/sh

g++ -O3 -pthread -lrt SenderProcess.cpp -o Sender
g++ -O3 -pthread -lrt ReceiverProcess.cpp -o Receiver
g++ -O3 -pthread -lrt ChannelProcess.cpp -o Channel
