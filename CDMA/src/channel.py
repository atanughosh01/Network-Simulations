import const
import threading
from datetime import datetime


class Channel:

    def __init__(self, name, sender_to_channel, channel_to_receiver):
        self.name                 = name
        self.sender_to_channel    = sender_to_channel
        self.channel_to_receiver  = channel_to_receiver
        self.channel_data         = [0 for i in range(const.total_sender_number)]  # channel data to be distributed
        self.sync_value           = 0


    def take_data_from_sender_and_distribute(self):

        while True:
            for _ in range(const.total_sender_number):
                data = []
                data = self.sender_to_channel.recv()
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print("{} ||| CHANNEL...   ||  {}".format(curr_datetime, str(data)))
                with open('textfiles/report.txt', 'a+', encoding='utf-8') as rep_file:
                    rep_file.write("\n{} ||| CHANNEL...   ||  {}".format(curr_datetime, str(data)))
  
                # update channel data
                for i in range(len(data)): self.channel_data[i] += data[i]
                self.sync_value += 1

                if self.sync_value == const.total_sender_number:
                    
                    # distribute over every receiver
                    for receiver in range(const.total_receiver_number):
                        self.channel_to_receiver[receiver].send(self.channel_data)

                    # reset self.value and channelData for next bit transfer
                    self.sync_value = 0
                    self.channel_data = [0 for _ in range(len(data))]


    def start_channel(self):
        channel_thread = threading.Thread(name="Channel-Thread", target=self.take_data_from_sender_and_distribute)
        channel_thread.start()
        channel_thread.join()
