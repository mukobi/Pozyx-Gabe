import numpy as np


class DataFunctions:
    @staticmethod
    def median(data_list):
        """
        This function takes the median of a list of data.

        :param list list: this is a list of numbers that the user provides for calculation
        :return float median: this is the median of the data provided
        """
        median = np.median(data_list)
        return median

    @staticmethod
    def find_total_distance1D(
            __pos_x, __pos_y, __pos_z, prev_pos_x, velocity_x, velocity_y, velocity_z, total_distance):
        """
        WARNING - This function looks very broken, and is currently not implemented anywhere.
        Gabe suggests to delete it or seriously revise it.

        Function to determine the total distance travelled by the Pozyx device

        :param float pos_*: the current x, y or z position data based on mean calculation
        :param float prev_pos_*: the previous x, y or z position stored from last iterate_file
        :param float velocity_*: the calculated x, y or z velocity
        :param float total_distance: the variable storing the total distance travelled

        :return float total_distance: updates the total distance travelled
        :return float total_velocity: the velocity of all directions combined for use in velocity_bins function

        Notes:
        The baseline velocity for adding to the total distance was roughly determined based on one test of 75 seconds of
        taking data with a still device to see what the maximum possible velocity could be.
        """
        from math import sqrt

        total_velocity = (velocity_x + velocity_y + velocity_z)
        # Getting TypeError: cannot perform reduce with flexible type
        pos_x = Velocity.position_mean_calculation(__pos_x)
        pos_y = Velocity.position_mean_calculation(__pos_y)
        pos_z = Velocity.position_mean_calculation(__pos_z)

        if total_velocity > 2500:
            total_distance += sqrt((pos_x - prev_pos_x)**2 + (pos_x - prev_pos_x)**2 + (pos_x - prev_pos_x)**2)

        return total_distance, total_velocity


    @staticmethod
    def find_total_distance(__pos_x, __pos_y, __pos_z, prev_pos_x, prev_pos_y, prev_pos_z, velocity_x, velocity_y, velocity_z, total_distance):
        """
        Function to determine the total distance travelled by the Pozyx device

        :param float pos_*: the current x, y or z position data based on mean calculation
        :param float prev_pos_*: the previous x, y or z position stored from last iterate_file
        :param float velocity_*: the calculated x, y or z velocity
        :param float total_distance: the variable storing the total distance travelled

        :return float total_distance: updates the total distance travelled
        :return float total_velocity: the velocity of all directions combined for use in velocity_bins function

        Notes:
        The baseline velocity for adding to the total distance was roughly determined based on one test of 75 seconds of
        taking data with a still device to see what the maximum possible velocity could be.
        """
        from math import sqrt

        total_velocity = (velocity_x + velocity_y + velocity_z)
        #Getting TypeError: cannot perform reduce with flexible type
        pos_x = Velocity.position_mean_calculation(__pos_x)
        pos_y = Velocity.position_mean_calculation(__pos_y)
        pos_z = Velocity.position_mean_calculation(__pos_z)

        if total_velocity > 2500:
            total_distance += sqrt((pos_x - prev_pos_x)**2 + (pos_x - prev_pos_x)**2 + (pos_x - prev_pos_x)**2)

        return total_distance, total_velocity


    @staticmethod
    def velocity_bins(total_velocity, time_between_2500_and_4500, time_between_4500_and_6500, time_between_6500_and_8500, time_above_8500, timeDifference):
        """
        Function to determine how long the device has been at different velocity intervals.
        """
        if total_velocity > 2500 and total_velocity <= 4500:
            time_between_2500_and_4500 += timeDifference
        elif total_velocity > 4500 and total_velocity <= 6500:
            time_between_4500_and_6500 += timeDifference
        elif total_velocity > 6500 and total_velocity <= 8500:
            time_between_6500_and_8500 += timeDifference
        elif total_velocity > 8500:
            time_above_8500 += timeDifference

        return time_between_2500_and_4500, time_between_4500_and_6500, time_between_6500_and_8500, time_above_8500

    @staticmethod
    def str_append_length(number, length):
        """
        Make a data value have a set character length.

        :param float number: the data point, probably a number, that you want to round
        :param int length: the length of characters you want the output to be
        :return: a string representation of the input number with set length
        :rtype: str

        This function takes a number and rounds it off/adds zeros to
        return a string of the number with a set character length.
        This is to make it easier to read the data from the console
        since every row will have the same number of data points.
        """
        num_string = str(number)
        # remove trailing .0
        if num_string[-2:] == ".0":
            num_string = num_string[:-2]
        # add spaces
        while len(num_string) < length:
            num_string += " "
        while len(num_string) > length:
            num_string = num_string[:-1]
        return num_string

    @staticmethod
    def str_prepend_length(number, length):
        """
        Make a data value have a set character length.

        :param int number: the data point, probably a number, that you want to round
        :param int length: the length of characters you want the output to be
        :return: a string representation of the input number with set length
        :rtype: str

        This function takes a number and adds zeros to the beginning
        as necessary to return a string of the number with a set
        character length. This is to make it easier to read the data
        from the console since every row will have the same number
        of data points.
        """
        num_string = str(number)
        # remove trailing .0
        if num_string[-2:] == ".0":
            num_string = num_string[:-2]
        # add decimal place if nonexistent
        if len(num_string) >= length:
            return num_string
        while len(num_string) < length:
            num_string = " " + num_string
        return num_string

    @staticmethod
    def convert_hertz(time_difference):
        """
        Finds the instantaneous frequency of the data in hertz

        :param float time_difference: the difference in time between two data points
        :return: instantaneous frequency in hertz
        :rtype: float

        The average hertz is calculated with the number of data points and the total time elapsed
        """
        try:
            hertz = 1 / time_difference
        except ZeroDivisionError:
            hertz = 0
        return hertz

    @staticmethod
    def find_average_hertz(index, elapsed):
        """
        Finds the average frequency of the data in hertz

        :param int index: the index of the data point
        :param float elapsed: the total elapsed time since function began
        :return: average frequency in hertz
        :rtype: float
        The average hertz is calculated with the number of data points and the total time elapsed
        """
        try:
            average_hertz = index / elapsed
        except ZeroDivisionError:
            average_hertz = 0
        return average_hertz

    @staticmethod
    def bin_input():
        """
        This function determines the amount of data points that the user would like to bin.

        :return integer bin_input: the number of data points the user will bin.
        """
        try:
            bin_input = int(input("How many data points would you like to bin?\n"))
        except ValueError:
            print("Invalid input, bin size set to 10 by default.")
            bin_input = 10
        return bin_input

class Velocity:
    """
    This class is to be used for the calculation of velocity on the X, Y and Z axes.
    """

    @staticmethod
    def update_bins1D(bin_pos,bin_time, new_position, new_time):
        """
        This function updates the position and time bins used for calculation

        """
        from modules.data_averaging import BinData as BinData

        import pdb; pdb.set_trace()
        BinData.add(bin_pos, new_position.distance)         #creating a list of x position data points for calculation
        bin_pos = BinData.return_data(bin_pos)         #getting that list

        BinData.add(bin_time, new_time)
        bin_time = BinData.return_data(bin_time)

        return bin_pos, bin_time


    @staticmethod
    def update_bins(bin_pos_x, bin_pos_y, bin_pos_z, bin_time, elapsed, one_cycle_position):
        """
        This function updates the position and time bins used for calculation

        :param object bin_pos_x: this is the object storing x position data
        :param object bin_pos_y: this is the object storing y position data
        :param object bin_pos_z: this is the object storing z position data

        :return list binned_pos_x: the list of x position data
        :return list binned_pos_y: the list of y position data
        :return list binned_pos_z: the list of z position data
        :return list binned_time: the list of previous time data
        """
        from modules.data_averaging import BinData as BinData

        BinData.add(bin_pos_x, one_cycle_position.x)         #creating a list of x position data points for calculation
        binned_pos_x = BinData.return_data(bin_pos_x)         #getting that list

        BinData.add(bin_pos_y, one_cycle_position.y)         #creating a list of x position data points for calculation
        binned_pos_y = BinData.return_data(bin_pos_y)

        BinData.add(bin_pos_z, one_cycle_position.z)         #creating a list of x position data points for calculation
        binned_pos_z = BinData.return_data(bin_pos_z)

        BinData.add(bin_time, elapsed)
        binned_time = BinData.return_data(bin_time)

        return binned_pos_x, binned_pos_y, binned_pos_z, binned_time

    @staticmethod
    def linreg_velocity(bin_pos, bin_time):
        """
        This function uses linear regression over the binned data to get the linear slope, which is the calculated velocity.

        :param bin_pos: this is the position to use for velocity calculation
        :param bin_time: this is the binned time used in calculation
        :return float coeff: this is the slope of the calculated linear regression

        Notes:
        This calculation method returns miniscule velocity data that is only positive.
        For now, usage of only the simple method is encouraged.
        """
        from collections import deque
        import numpy as np

        try:
            coeff = np.polyfit(bin_pos, bin_time, 1)
        except ValueError:
            num_of_nans = bin_pos.count(np.nan)
            if num_of_nans >= int(len(bin_pos) - 1):
                coeff = [np.nan, np.nan]
            else:
                #fix = np.isfinite(bin_pos)
                #coeff = np.polyfit(bin_pos[fix], bin_time, 1)
                coeff = np.polyfit(bin_pos, bin_time, 1)
                print('Coeff')
                print(coeff)
        return coeff[1]

    @staticmethod
    def position_mean_calculation(binned_pos):
        """
        This function calculates the mean of the binned position data

        :param list binned_pos: this is the list of the position data for calculation
        :return mean_binned_pos: this is the mean of the position data

        Note: the mean function is preferable to median functionality due to error handling with numpy nans
        """
        import numpy as np

        mean_binned_pos = np.nanmean(binned_pos)        #Calculating the mean of the position data for smoothing

        return mean_binned_pos

    @staticmethod
    def time_mean_calculation(index, bin_input, binned_time):
        """
        Calculates the mean time of the timestamp data

        :param index: the data line
        :param bin_input: the number of data points to be binned
        :param binned_time: the type of time data to use for mean calculation

        Note: use the time difference for simple velocity calculation, not the total elapsed time
        """

        import numpy as np

        if index > bin_input:   #Calculates the mean of the binned time data for velocity calculation
            mean_bin_time = np.nanmean(binned_time)
        else:                   #Sets variable to zero until enough data is in for valid calculations
            mean_bin_time = 0

        return mean_bin_time

    @staticmethod
    def update_previous_bins1D(binned_pos):
        """
        This function updates the bins for previous position bins and returns them at the end of the iterate_file.

        :param binned_pos_x: the x position data already used in calculation
        :param binned_pos_y: the y position data already used in calculation
        :param binned_pos_z: the z position data already used in calculation
        """

        import numpy as np

        prev_bin_pos = binned_pos           #Updates the previous x position bin
        mean_prev_bin_pos = np.mean(prev_bin_pos)    #Calculates the mean of the previous x position data


        return mean_prev_bin_pos


    @staticmethod
    def update_previous_bins(binned_pos_x, binned_pos_y, binned_pos_z):
        """
        This function updates the bins for previous position bins and returns them at the end of the iterate_file.

        :param binned_pos_x: the x position data already used in calculation
        :param binned_pos_y: the y position data already used in calculation
        :param binned_pos_z: the z position data already used in calculation
        """

        import numpy as np

        prev_bin_pos_x = binned_pos_x           #Updates the previous x position bin
        mean_prev_bin_pos_x = np.mean(prev_bin_pos_x)    #Calculates the mean of the previous x position data

        prev_bin_pos_y = binned_pos_y           #Updates the previous x position bin
        mean_prev_bin_pos_y = np.mean(prev_bin_pos_y)    #Calculates the mean of the previous x position data

        prev_bin_pos_z = binned_pos_z           #Updates the previous x position bin
        mean_prev_bin_pos_z = np.mean(prev_bin_pos_z)    #Calculates the mean of the previous x position data

        return mean_prev_bin_pos_x, mean_prev_bin_pos_y, mean_prev_bin_pos_z


    @staticmethod
    def simple_velocity(position, prev_pos, time, prev_time):
        """
        This is a function to simply calculate velocity.

        :param integer position: this is the current position of the device
        :param integer prev_pos: this is the previous position of the device
        :param float time: this is the current time
        :param float prev_time: this is the previous time
        """
        import numpy as np

        if prev_pos == 0:
            return 0
        else:
            try:
                velocity = (position - prev_pos) / (time - prev_time)
            except ZeroDivisionError:
                velocity = np.nan
            return velocity

    @staticmethod
    def find_velocity(index, bin_input, position, mean_prev_pos, time, method = 'simple'):
        """
        This is a function to determine which method of finding the velocity to use.

        :param integer position: this is the current position of the device
        :param integer prev_pos: this is the previous position of the device
        :param float time: this is the current time
        :param float prev_time: this is the previous time

        Notes: Default is simple.
        The function returns 'nan' from numpy if it takes an error message.
        For improvement, we can add functionality to wait a while after receiving an error message.
        """
        from modules.data_functions import Velocity as Velocity
        import numpy as np


        if (int(len(position)) == bin_input) and (len(position) == len(time)):
            if method == 'simple':
                mean_position = Velocity.position_mean_calculation(position)

                #the time mean calculation takes the total elapsed time over delta position which causes bad data
                mean_bin_time = Velocity.time_mean_calculation(index, bin_input, time)

                velocity = Velocity.simple_velocity(mean_position, mean_prev_pos, mean_bin_time)

            elif method == 'linreg':
                velocity = Velocity.linreg_velocity(position, time)
            return velocity
        else:
            return np.nan


    @staticmethod
    def find_velocity1D(bin_input, position, previous_position, time, previous_time, method = 'simple'):
        """
        This is a function to determine which method of finding the velocity to use.

        :param deque position: this is the current position of the device
        :param integer prev_pos: this is the previous position of the device
        :param deque time: this is the current time
        :param float prev_time: this is the previous time

        Notes: Default is simple.
        The function returns 'nan' from numpy if it takes an error message.
        For improvement, we can add functionality to wait a while after receiving an error message.
        """
        from modules.data_functions import Velocity as Velocity
        import numpy as np

        #print('Position')
        #print(position)
        #print(previous_position)
        #print('Time')
        #print(time)
        #print(previous_time)

        if (int(len(position)) == bin_input):
            if method == 'simple':
                single_position = np.mean(position)
                single_previous_position = np.mean(previous_position)

                #the time mean calculation takes the total elapsed time over delta position which causes bad data
                single_time = np.mean(time)
                single_previous_time = np.mean(previous_time)

                velocity = Velocity.simple_velocity(single_position, single_previous_position, single_time, single_previous_time)

            elif method == 'linreg':
                velocity = Velocity.linreg_velocity(position, time)
            return velocity
        else:
            return np.nan

    def initialize_bins1D(bin_input):
        """
        Function to create the deque objects that are needed for easily binning the data.

        :param integer bin_input: the size of the bins

        :return object bin_pos_*: each object that will bin the data to calculate velocity
        :return integer prev_bin_*: the initialized previous bins that will be used
        :return object bin_time: the object for binning time
        """
        from .data_averaging import BinData
        bin_pos = BinData(bin_size = bin_input)   # Creating position deque objects to calculate velocity
        prev_bin_pos = BinData(bin_size = bin_input)   # Creating position deque objects to calculate velocity

        bin_time = BinData(bin_size = bin_input)
        prev_bin_time = BinData(bin_size = bin_input)

        return bin_pos, prev_bin_pos, bin_time, prev_bin_time

    @staticmethod
    def initialize_mean_prev_bins1D():
        """
        Initializing the mena previous bins for use.

        :return mean_prev_bin_pos_*: these are meant to be the means of the bins of previous data taken by Pozyx

        Note: the class ignores the functions until it gets data other than a 0
        """
        mean_prev_bin_pos = 0

        return mean_prev_bin_pos


    def initialize_bins3D(bin_input):
        """
        Function to create the deque objects that are needed for easily binning the data.

        :param integer bin_input: the size of the bins

        :return object bin_pos_*: each object that will bin the data to calculate velocity
        :return integer prev_bin_*: the initialized previous bins that will be used
        :return object bin_time: the object for binning time
        """
        from .data_averaging import BinData
        bin_pos_x = BinData(bin_size = bin_input)   # Creating position deque objects to calculate velocity
        prev_bin_pos_x = 0                          # Initializing the previous points

        bin_pos_y = BinData(bin_size = bin_input)
        prev_bin_pos_y = 0

        bin_pos_z = BinData(bin_size = bin_input)
        prev_bin_pos_z = 0

        bin_time = BinData(bin_size = bin_input)

        return bin_pos_x, bin_pos_y, bin_pos_z, prev_bin_pos_x, prev_bin_pos_y, prev_bin_pos_z, bin_time

    @staticmethod
    def initialize_mean_prev_bins3D():
        """
        Initializing the mena previous bins for use.

        :return mean_prev_bin_pos_*: these are meant to be the means of the bins of previous data taken by Pozyx

        Note: the class ignores the functions until it gets data other than a 0
        """
        mean_prev_bin_pos_x = 0
        mean_prev_bin_pos_y = 0
        mean_prev_bin_pos_z = 0

        return mean_prev_bin_pos_x, mean_prev_bin_pos_y, mean_prev_bin_pos_z

    def find_velocity3D(index, bin_input, binned_pos_x, mean_prev_bin_pos_x, binned_pos_y, mean_prev_bin_pos_y,
        binned_pos_z, mean_prev_bin_pos_z, binned_time, velocity_method):
        """
        This function simply reduces the 3D code to three lines that calculate the velocity by calling on the find_velocity function.

        :param integer index: the index
        :param integer bin_input: the size of the bin
        :param float binned_pos_*: the current binned position for each direction
        :param integer mean_prev_bin_pos_*: the mean of the previos bin of data
        :param float binned_time: the bin of time data to get the mean time
        :param string velocity_method: this is the method for calculating velocity

        :return float velocity_*: this returns each of the X, Y, and Z velocities
        """

        import numpy as np

        velocity_x = Velocity.find_velocity(index, bin_input, binned_pos_x, mean_prev_bin_pos_x, binned_time, method = velocity_method)    #Calculates x velocity
        velocity_y = Velocity.find_velocity(index, bin_input, binned_pos_y, mean_prev_bin_pos_y, binned_time, method = velocity_method)    #Calculates y velocity
        velocity_z = Velocity.find_velocity(index, bin_input, binned_pos_z, mean_prev_bin_pos_z, binned_time, method = velocity_method)    #Calculates z velocity


        return velocity_x, velocity_y, velocity_z
