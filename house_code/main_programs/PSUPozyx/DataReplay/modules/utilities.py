import time
from modules.data_parsing import DataParsing


class Utilities:
    @staticmethod
    def wait_for_time_difference(replay_speed, i_difference, data_list, previous_time):
        if replay_speed:
            data_difference = float(
                DataParsing.get_time_difference(i_difference, data_list))
            replay_coeff = float(replay_speed)
            while True:
                current_time = time.time()
                replay_difference = (current_time - previous_time) * replay_coeff
                if replay_difference >= data_difference:
                    break
            previous_time = current_time
        return previous_time