#!/usr/bin/env python
import sys
from pythonosc.udp_client import SimpleUDPClient
import time
import subprocess
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_reading import FileReading
from modules.data_parsing import DataParsing
from modules.replay_osc_message_sending import ReplayOscMessageSending
from modules.utilities import Utilities


class DataReplay:
    def __init__(self, my_file, my_osc_udp_client, my_replay_speed,
                 my_attributes_to_log_str):
        self.file = my_file
        self.osc_udp_client = my_osc_udp_client
        self.replay_speed = my_replay_speed
        self.attributes_to_log = UserInput.get_attributes_to_log_from_str(
            my_attributes_to_log_str)

    def iterate_file(self):
        with open(self.file, 'r') as f:
            header_list = FileReading.get_header_list(f)
            data_file_type = FileReading.determine_data_file_type(header_list)


            i_index, i_time, i_difference, i_hz, i_avehz = \
                FileReading.get_timestamp_indices(header_list)

            previous_time = 0.0

            print(DataParsing.build_data_file_type_string(data_file_type))

            start_time = time.time()
            for line in f:
                data_list = FileReading.get_data_list(line)
                output = ""
                timestamp = DataParsing.build_timestamp_info(
                    i_index, i_time, i_avehz, data_list)
                output += timestamp
                output += DataParsing.build_rest_of_data(
                    data_file_type, header_list, data_list, self.attributes_to_log)
                print(output)

                ReplayOscMessageSending.send_message(
                    data_file_type, header_list, data_list, osc_udp_client)

                previous_time = Utilities.wait_for_time_difference(
                    self.replay_speed, i_difference, data_list, previous_time)
            print("\nRendered Time: " + str(time.time() - start_time) + "s")

if __name__ == "__main__":
    use_processing = True
    replay_speed = 1

    ip = "127.0.0.1"
    network_port = 8888
    osc_udp_client = None

    arguments = sys.argv
    arg_length = len(arguments)

    file = ""
    attributes_to_log = "00000000"
    replay_speed = 1

    # no arguments added on, only call was to script
    if arg_length is 1:
        sys.exit("Error, please provide a file to replay after the script name")
    elif arg_length is 2:
        file = arguments[1]
    elif arg_length is 3:
        file = arguments[1]
        replay_speed = int(arguments[2])
    elif arg_length is 4:
        file = arguments[1]
        replay_speed = int(arguments[2])
        attributes_to_log = arguments[3]
    else:
        sys.exit("Error, too many arguments provided.")

    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
    replay = DataReplay(file, osc_udp_client, replay_speed, attributes_to_log)

    replay.iterate_file()
