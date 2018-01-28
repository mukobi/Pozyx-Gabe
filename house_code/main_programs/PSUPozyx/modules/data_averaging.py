class DataAveraging:

    @staticmethod
    def add_sensor_data_to_total(sensor_data, previous_total):
        new_total = previous_total
        for i in range(0,len(sensor_data)):
            data_point = sensor_data[i]
            if type(data_point) == int or type(data_point) == float:
                new_total[i] = sensor_data[i]

        return new_total

    @staticmethod
    def get_average_sensor_data(total_sensor_data, index):
        averaged_sensor_data = total_sensor_data
        for i in range(0, len(averaged_sensor_data)):
            data_point = averaged_sensor_data[i]
            if type(data_point) == int or type(data_point) == float:
                averaged_sensor_data[i] = averaged_sensor_data[i] / index

        return averaged_sensor_data

    def update_prev_points(pos, index):
        """
        We are using deque objects instead of this function.

        This function will be used to update the variables that can be used for calculations.
        For this function to work, prev_pos must be set to 0 in main function.

        Ideas: utilize if statements with the index variable to determine when to define the previous position points.
        """
        """
        try:
            prev_fifth = prev_fourth
            prev_fourth = prev_third
            prev_third = prev_second
            prev_second = prev_pos
            prev_pos = pos
            return prev_pos, prev_second, prev_third, prev_fourth, prev_fifth
            import pdb; pdb.set_trace()
        except NameError:
            try:
                prev_fourth = prev_third
                prev_third = prev_second
                prev_second = prev_pos
                prev_pos = pos
                return prev_pos, prev_second, prev_third, prev_fourth
            except NameError:
                try:
                    #This code is always causing an error
                    prev_third = prev_second

                    prev_second = prev_pos
                    prev_pos = pos
                    return prev_pos, prev_second, prev_third
                except NameError:
                    if prev_pos != 0:
                        prev_second = prev_pos
                        prev_pos = pos
                        return prev_pos, prev_second
                    else:
                        prev_pos = pos
                        return prev_pos
        """
        if index == 0:
            prev_pos = pos
            return prev_pos
        elif index == 1:
            prev_second = prev_pos
            prev_pos = pos
            return prev_pos, prev_second
        elif index == 2:
            prev_third = prev_second
            prev_second = prev_pos
            prev_pos = pos
            return prev_pos, prev_second, prev_third
        elif index == 3:
            prev_fourth = prev_third
            prev_third = prev_second
            prev_second = prev_pos
            prev_pos = pos
            return prev_pos, prev_second, prev_third, prev_fourth
        elif index >= 4:
            prev_fifth = prev_fourth
            prev_fourth = prev_third
            prev_third = prev_second
            prev_second = prev_pos
            prev_pos = pos
            pos_data_list = [pos, prev_pos, prev_second, prev_third, prev]
            return prev_pos, prev_second, prev_third, prev_fourth, prev_fifth

from collections import deque           #deque is a useful data storing tool


class BinData:
    """
    This class is used for taking previous data points and making them available, in a list, for calculation.

    Notes:
    For use, the object must be defined in the main function.

    All the imports needed are:
    from modules.data_functions import DataFunctions as DataFunctions
    from collections import deque
    from modules.data_averaging import BinData as BinData
    import numpy as np
    """
    def __init__(self, bin_size = 5):
        self.num = deque(maxlen=bin_size)

    def add(self, new_data):
        """
        This function appends new data to the list and pops out old data.

        :param self: the object being used for this class
        :param float new_data: the data to be inserted into the list
        """
        import numpy as np

        if new_data == 0:
            new_data = np.nan
        else:
            self.num.append(new_data)

    def return_data(self):
        """
        This function allows the user to store the list by returning it back to them.

        :param self: the object being used for this class
        :return list self.data: this returns the list created by deque
        """
        return self.num
