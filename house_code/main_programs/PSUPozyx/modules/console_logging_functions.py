import time as time
from .data_functions import DataFunctions as DataFunctions
import sys
sys.stdout.flush()

class ConsoleLoggingFunctions:

    @staticmethod
    def get_time():
        """
        Gets processor time

        :return float current_time: the current processor time
        """
        current_time = time.time()
        return current_time

    @staticmethod
    def get_elapsed_time(self, start_time):
        """
        Gets elapsed time since start_time

        :param self:
        :param float start_time: time to count from, set at program start
        :return float elapsed_time: time passed since start_time
        """
        elapsed_time = self.get_time() - start_time
        return elapsed_time

    @staticmethod
    def single_cycle_time_difference(previous_time, current_time):
        """
        Calculates the time it took to get to the current cycle

        :param float previous_time: the point of time of the previous cycle
        :param float current_time: the point of time of the current cycle
        :return:
            :time_difference: the difference in time between cycles
            :new_previous_time: used as previous_time in next cycle
        :rtype: float, float
        """
        time_difference = current_time - previous_time
        new_previous_time = current_time
        return time_difference, new_previous_time

    @staticmethod
    def log_sensor_data_to_console(index, elapsed, data_dictionary):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param dict data_dictionary: a dictionary where the keys are the
            labels for each data type to log (e.g. acceleration, magnetic)
            and the values are lists of labels and values (for example,
            ['x', 2, 'y', 3, 'z', 5] )
        """
        output = ConsoleLoggingFunctions.create_sensor_data_output(
            index, elapsed, data_dictionary)
        print(output, flush=True)

    @staticmethod
    def create_sensor_data_output(index, elapsed, data_dictionary):
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(data_dictionary) == str:
            output += data_dictionary
        else:
            for key in data_dictionary:
                output += " | " + key
                for item in data_dictionary[key]:
                    output += " " + str(item)
        return output

    @staticmethod
    def log_position_to_console(index, elapsed, position):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))

        print(output, flush=True)

    @staticmethod
    def log_position_and_velocity_to_console(index, elapsed, position, velocity_x, velocity_y, velocity_z):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))

        output += (" | Vel: " + "X: " + DataFunctions.str_append_length(velocity_x, 7)
                   + " Y: " + DataFunctions.str_append_length(velocity_y, 7)
                   + " Z: " + DataFunctions.str_append_length(velocity_z, 7))

        print(output, flush=True)

    @staticmethod
    def log_position_to_console_1d(index, elapsed, position):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.distance))

        print(output, flush=True)

    @staticmethod
    def log_position_and_velocity_to_console_1d(index, elapsed, position, velocity):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.distance))

        output += (" | Vel: " + "X: " + DataFunctions.str_append_length(velocity, 7))

        print(output, flush=True)

    @staticmethod
    def log_range_motion_and_velocity(
            index, elapsed, position, data_dictionary, velocity):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        output += ConsoleLoggingFunctions.create_sensor_data_output(
            index, elapsed, data_dictionary)

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.distance))

        output += (" | Vel: " + "X: " + DataFunctions.str_append_length(velocity, 7))

        print(output, flush=True)

    @staticmethod
    def log_range_and_motion(
            index, elapsed, position, data_dictionary):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position: position data
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        output += ConsoleLoggingFunctions.create_sensor_data_output(
            index, elapsed, data_dictionary)

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.distance))

        print(output, flush=True)

    @staticmethod
    def log_multitag_position_to_console(index, elapsed, position_array):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position_array: position data with tags in array
        """
        output = str(index)
        output += " Time "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        output += " | "

        for idx, element in enumerate(position_array):
            i = position_array.index(element)
            val = idx % 4
            mod = idx % 4 != 0
            nmod = i % 4
            nval = i % 4 != 0
            if idx % 4 == 0:
                output += hex(element) + " "
            elif idx % 4 != 0:
                output += str(element) + " "
        print(output, flush=True)

    @staticmethod
    def log_multitag_1D_to_console(index, elapsed, position_array):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position_array: position data with tags in array
        """
        output = str(index)
        output += " Time "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        output += " | "

        for idx, element in enumerate(position_array):
            i = position_array.index(element)
            val = idx % 2
            mod = idx % 2 != 0
            nmod = i % 2
            nval = i % 2 != 0
            if idx % 2 == 0:
                output += hex(element) + " "
            elif idx % 2 != 0:
                output += str(element) + " "
        print(output, flush=True)

    @staticmethod
    def log_position_and_sensor_data_to_console(index, elapsed, data_dictionary, position):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param dict data_dictionary: a dictionary where the keys are the
            labels for each data type to log (e.g. acceleration, magnetic)
            and the values are lists of labels and values (for example,
            ['x', 2, 'y', 3, 'z', 5] )
        :param position: position data from device
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(data_dictionary) == str:
            output += data_dictionary
        elif type(position) == str:
            output += position
        else:
            for key in data_dictionary:
                output += " | " + key
                for item in data_dictionary[key]:
                    output += " " + str(item)
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))

        print(output, flush=True)

    @staticmethod
    def log_position_and_velocity_and_sensor_data_to_console(index, elapsed, data_dictionary, position, velocity_x, velocity_y, velocity_z):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param dict data_dictionary: a dictionary where the keys are the
            labels for each data type to log (e.g. acceleration, magnetic)
            and the values are lists of labels and values (for example,
            ['x', 2, 'y', 3, 'z', 5] )
        :param position: position data from device
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(data_dictionary) == str:
            output += data_dictionary
        elif type(position) == str:
            output += position
        else:
            for key in data_dictionary:
                output += " | " + key
                for item in data_dictionary[key]:
                    output += " " + str(item)
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))
            output += (" | Vel: " + "X: " + DataFunctions.str_append_length(velocity_x, 6)
                       + " Y: " + DataFunctions.str_append_length(velocity_y, 6)
                       + " Z: " + DataFunctions.str_append_length(velocity_z, 6))
        print(output, flush=True)

    @staticmethod
    def format_sensor_data(sensor_data, multiple_attributes_to_log):
        """
        :param sensor_data:
        :param multiple_attributes_to_log:
        :return: formatted data dictionary
        """
        # if the sensor data was returned as an error string
        try:
            data_dictionary = {}
            for attribute_to_log in multiple_attributes_to_log:
                line_of_data = []
                if attribute_to_log == "pressure":
                    attribute_to_log += ":"  # add a colon in the output
                    line_of_data.append(DataFunctions.exp_notation_str_set_length(
                        DataFunctions, sensor_data.pressure, 10))
                elif attribute_to_log == "acceleration":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.acceleration.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.acceleration.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.acceleration.z, 8))
                elif attribute_to_log == "magnetic":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.z, 8))
                elif attribute_to_log == "angular velocity":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.z, 8))
                elif attribute_to_log == "euler angles":
                    line_of_data.append("heading:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.heading, 8))
                    line_of_data.append("roll:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.roll, 8))
                    line_of_data.append("pitch:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.pitch, 8))
                elif attribute_to_log == "quaternion":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.z, 8))
                    line_of_data.append("w:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.w, 8))
                elif attribute_to_log == "linear acceleration":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.linear_acceleration.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.linear_acceleration.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.linear_acceleration.z, 8))
                elif attribute_to_log == "gravity":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.gravity_vector.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.gravity_vector.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.gravity_vector.z, 8))
                data_dictionary[attribute_to_log.title()] = line_of_data
            return data_dictionary
        except AttributeError:
            return " Error in data"

    @staticmethod
    def print_data_error_message(index, elapsed_time, message="Error, no data"):
        output = (str(index) + " Time: "
                  + DataFunctions.str_append_length(elapsed_time, 10) + " "
                  + message)
        print(output, flush=True)


class CondensedConsoleLogging:
    @staticmethod
    def get_time():
        """
        Gets processor time

        :return float current_time: the current processor time
        """
        current_time = time.time()
        return current_time

    @staticmethod
    def get_elapsed_time(self, start_time):
        """
        Gets elapsed time since start_time

        :param self:
        :param float start_time: time to count from, set at program start
        :return float elapsed_time: time passed since start_time
        """
        elapsed_time = self.get_time() - start_time
        return elapsed_time

    @staticmethod
    def single_cycle_time_difference(previous_time, current_time):
        """
        Calculates the time it took to get to the current cycle

        :param float previous_time: the point of time of the previous cycle
        :param float current_time: the point of time of the current cycle
        :return:
            :time_difference: the difference in time between cycles
            :new_previous_time: used as previous_time in next cycle
        :rtype: float, float
        """
        time_difference = current_time - previous_time
        new_previous_time = current_time
        return time_difference, new_previous_time

    @staticmethod
    def build_timestamp(index, elapsed):
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_append_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_append_length(ave_hertz, 5)
        output += ave_hertz_str
        return output

    @staticmethod
    def build_tag(single_device):
        return " | " + hex(single_device.tag)

    @staticmethod
    def build_range(single_device):
        output = " | Dist "
        output += DataFunctions.str_prepend_length(
            single_device.device_range.distance, 5)
        output += " | Smooth "
        output += DataFunctions.str_prepend_length(
            int(single_device.smoothed_range + 0.5), 5)
        output += " | Vel "
        try:
            output += DataFunctions.str_prepend_length(
                int(single_device.velocity + 0.5), 5)
        except TypeError:
            output += "     "
        return output

    @staticmethod
    def build_position(single_device):
        output = " | Pos "
        output += DataFunctions.str_prepend_length(
            single_device.position.x, 5) + " "
        output += DataFunctions.str_prepend_length(
            single_device.position.y, 5) + " "
        output += DataFunctions.str_prepend_length(
            single_device.position.z, 5)

        output += " | Smooth "
        output += DataFunctions.str_prepend_length(
            int(single_device.smoothed_x + 0.5), 5) + " "
        output += DataFunctions.str_prepend_length(
            int(single_device.smoothed_y + 0.5), 5) + " "
        output += DataFunctions.str_prepend_length(
            int(single_device.smoothed_z + 0.5), 5)

        output += " | Vel "
        try:
            output += DataFunctions.str_prepend_length(
                int(single_device.velocity_x + 0.5), 5) + " "
            output += DataFunctions.str_prepend_length(
                int(single_device.velocity_y + 0.5), 5) + " "
            output += DataFunctions.str_prepend_length(
                int(single_device.velocity_z + 0.5), 5)
        except TypeError:
            output += " " * 15
        return output

    @staticmethod
    def format_sensor_data(sensor_data, multiple_attributes_to_log):
        """
        :param sensor_data:
        :param multiple_attributes_to_log:
        :return: formatted data dictionary
        """
        # if the sensor data was returned as an error string
        try:
            data_dictionary = {}
            for attribute_to_log in multiple_attributes_to_log:
                line_of_data = []
                if attribute_to_log == "pressure":
                    attribute_to_log = "Press"
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.pressure, 8))
                elif attribute_to_log == "acceleration":
                    attribute_to_log = "Acc"
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.acceleration.x, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.acceleration.y, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.acceleration.z, 6))
                elif attribute_to_log == "magnetic":
                    attribute_to_log = "Mag"
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.x, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.y, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.magnetic.z, 6))
                elif attribute_to_log == "angular velocity":
                    attribute_to_log = "Ang Vel"
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.x, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.y, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.angular_vel.z, 6))
                elif attribute_to_log == "euler angles":
                    attribute_to_log = ""
                    line_of_data.append("Heading")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.heading, 6))
                    line_of_data.append("Roll")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.roll, 6))
                    line_of_data.append("Pitch")
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.euler_angles.pitch, 6))
                elif attribute_to_log == "quaternion":
                    attribute_to_log = "Quat"
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.x, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.y, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.z, 6))
                    line_of_data.append(DataFunctions.str_append_length(
                        sensor_data.quaternion.w, 6))
                elif attribute_to_log == "linear acceleration":
                    attribute_to_log = "Lin Acc"
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.linear_acceleration.x, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.linear_acceleration.y, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.linear_acceleration.z, 6))
                elif attribute_to_log == "gravity":
                    attribute_to_log = "Grav"
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.gravity_vector.x, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.gravity_vector.y, 6))
                    line_of_data.append(DataFunctions.str_prepend_length(
                        sensor_data.gravity_vector.z, 6))
                data_dictionary[attribute_to_log.title()] = line_of_data
            return data_dictionary
        except AttributeError:
            return " Error in data"

    @staticmethod
    def build_sensor_data(single_device_data, attributes_to_log):
        """
        Builds motion data output for a tag
        """
        if not attributes_to_log:
            return ""

        motion_data = single_device_data.sensor_data
        data_dictionary = CondensedConsoleLogging.format_sensor_data(
            motion_data, attributes_to_log)
        output = ""
        if type(data_dictionary) == str:
            output += data_dictionary
        else:
            for key in data_dictionary:
                output += " | " + key
                for item in data_dictionary[key]:
                    output += " " + str(item)
        return output

    @staticmethod
    def print_1d_ranging_output(index, elapsed, ranging_loop_array, attributes_to_log):
        output = CondensedConsoleLogging.build_timestamp(index, elapsed)
        for single_device in ranging_loop_array:
            output += CondensedConsoleLogging.build_tag(single_device)
            output += CondensedConsoleLogging.build_sensor_data(
                single_device, attributes_to_log)
            output += CondensedConsoleLogging.build_range(single_device)
        print(output, flush=True)

    @staticmethod
    def print_3d_positioning_output(index, elapsed, position_loop_array, attributes_to_log):
        output = CondensedConsoleLogging.build_timestamp(index, elapsed)
        for single_device in position_loop_array:
            output += CondensedConsoleLogging.build_tag(single_device)
            output += CondensedConsoleLogging.build_sensor_data(
                single_device, attributes_to_log)
            output += CondensedConsoleLogging.build_position(single_device)
        print(output, flush=True)

    @staticmethod
    def print_motion_data_output(index, elapsed, loop_array, attributes_to_log):
        output = CondensedConsoleLogging.build_timestamp(index, elapsed)
        for single_device in loop_array:
            output += CondensedConsoleLogging.build_tag(single_device)
            output += CondensedConsoleLogging.build_sensor_data(
                single_device, attributes_to_log)
        print(output, flush=True)
