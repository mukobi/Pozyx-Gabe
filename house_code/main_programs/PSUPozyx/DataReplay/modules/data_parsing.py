import time as time

from constants import definitions
from .data_functions import DataFunctions as DataFunctions


class DataParsing:
    @staticmethod
    def build_timestamp_info(i_index, i_time, i_avehz, data_list):
        index = data_list[i_index]
        time = data_list[i_time]
        avehz = data_list[i_avehz]
        return (str(index)
                + " Time " + DataFunctions.str_set_length(time, 10)
                + " Hz " + DataFunctions.str_set_length(avehz, 5))

    @staticmethod
    def build_data_file_type_string(data_type):
        if data_type is definitions.DATA_TYPE_MOTION_DATA:
            return "Motion Data"
        if data_type is definitions.DATA_TYPE_POSITIONING:
            return "Single-Device Positioning"
        if data_type is definitions.DATA_TYPE_MULTIDEVICE_POSITIONING:
            return "Multi-Device Positioning"
        if data_type is definitions.DATA_TYPE_POSITIONING_AND_MOTION_DATA:
            return "Single-Device Positioning and Motion Data"
        if data_type is definitions.DATA_TYPE_MULTIDEVICE_POSITIONING_AND_MOTION_DATA:
            return "Multi-Device Positioning and Motion Data"
        return "Unknown data file type"

    @staticmethod
    def build_rest_of_data(data_type, header_list, data_list, attributes_to_log=None):
        if attributes_to_log is None:
            attributes_to_log = []
        if data_type is definitions.DATA_TYPE_POSITIONING:
            return DataParsing.build_positioning_data(header_list, data_list)
        if data_type is definitions.DATA_TYPE_MULTIDEVICE_POSITIONING:
            return DataParsing.build_multidevice_positioning_data(header_list, data_list)
        if data_type is definitions.DATA_TYPE_MOTION_DATA:
            return DataParsing.build_motion_data(header_list, data_list, attributes_to_log)
        if data_type is definitions.DATA_TYPE_POSITIONING_AND_MOTION_DATA:
            return DataParsing.build_positioning_and_motion_data(header_list, data_list, attributes_to_log)
        if data_type is definitions.DATA_TYPE_MULTIDEVICE_POSITIONING_AND_MOTION_DATA:
            return DataParsing.build_multidevice_positioning_and_motion_data(header_list, data_list, attributes_to_log)

    @staticmethod
    def build_positioning_data(header_list, data_list):
        output = ""
        i_posx = header_list.index("Position-X")
        i_posy = header_list.index("Position-Y")
        i_posz = header_list.index("Position-Z")
        posx = data_list[i_posx]
        posy = data_list[i_posy]
        posz = data_list[i_posz]
        output += (" | Position"
                   + " X " + str(posx)
                   + " Y " + str(posy)
                   + " Z " + str(posz))
        return output

    @staticmethod
    def build_multidevice_positioning_data(header_list, data_list):
        output = ""
        for idx, tag in enumerate(header_list):
            if tag[:2] == "0x" and tag[-2:] == "-X":
                output += (" | " + tag[0:6] + " "
                           + data_list[idx + 0] + " "   # X
                           + data_list[idx + 1] + " "   # Y
                           + data_list[idx + 2] + " ")  # Z

        return output

    @staticmethod
    def build_motion_data(header_list, data_list, attributes_to_log):
        output = ""
        for attribute in attributes_to_log:
            if attribute == "pressure":
                output += "| Pressure " + DataFunctions.exp_notation_str_set_length(
                    DataFunctions, data_list[header_list.index("Pressure")], 8)
            elif attribute == "acceleration":
                output += (" | Acceleration"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Acceleration-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Acceleration-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Acceleration-Z")], 8))
            elif attribute == "magnetic":
                output += (" | Magnetic"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Magnetic-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Magnetic-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Magnetic-Z")], 8))
            elif attribute == "angular velocity":
                output += (" | Angular Velocity"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Angular-Vel-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Angular-Vel-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Angular-Vel-Z")], 8))
            elif attribute == "euler angles":
                output += (" | Angles"
                           + " Heading " + DataFunctions.str_set_length(data_list[header_list.index("Heading")], 8)
                           + " Roll " + DataFunctions.str_set_length(data_list[header_list.index("Roll")], 8)
                           + " Pitch " + DataFunctions.str_set_length(data_list[header_list.index("Pitch")], 8))
            elif attribute == "quaternion":
                output += (" | Quaternion"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Quaternion-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Quaternion-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Quaternion-Z")], 8)
                           + " W " + DataFunctions.str_set_length(data_list[header_list.index("Quaternion-W")], 8))
            elif attribute == "linear acceleration":
                output += (" | Linear Acc"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Linear-Acceleration-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Linear-Acceleration-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Linear-Acceleration-Z")], 8))
            elif attribute == "gravity":
                output += (" | Gravity"
                           + " X " + DataFunctions.str_set_length(data_list[header_list.index("Gravity-X")], 8)
                           + " Y " + DataFunctions.str_set_length(data_list[header_list.index("Gravity-Y")], 8)
                           + " Z " + DataFunctions.str_set_length(data_list[header_list.index("Gravity-Z")], 8))
        return output

    @staticmethod
    def build_positioning_and_motion_data(header_list, data_list, attributes_to_log):
        return (DataParsing.build_motion_data(header_list, data_list, attributes_to_log)
                + DataParsing.build_positioning_data(header_list, data_list))

    @staticmethod
    def build_multidevice_positioning_and_motion_data(header_list, data_list, attributes_to_log):
        return (DataParsing.build_motion_data(header_list, data_list, attributes_to_log)
                + DataParsing.build_multidevice_positioning_data(header_list, data_list))

    @staticmethod
    def get_time_difference(i_difference, data_list):
        return data_list[i_difference]


class ConsoleLoggingFunctionsOLD:

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
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(data_dictionary) == str:
            output += data_dictionary
        else:
            for key in data_dictionary:
                output += " | " + key
                for item in data_dictionary[key]:
                    output += " " + str(item)

        print(output)

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
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))

        print(output)

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
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
        output += ave_hertz_str

        # if the data passed was an error string
        if type(position) == str:
            output += position
        else:
            output += (" | Pos: " + "X: " + str(position.x)
                       + " Y: " + str(position.y)
                       + " Z: " + str(position.z))

        output += (" | Vel: " + "X: " + DataFunctions.str_set_length(velocity_x, 7)
                       + " Y: " + DataFunctions.str_set_length(velocity_y, 7)
                       + " Z: " + DataFunctions.str_set_length(velocity_z, 7))


        print(output)

    @staticmethod
    def log_multitag_position_to_console(index, elapsed, position_array):
        """
        Prints a line of data to the console

        :param int index: data index
        :param float elapsed: elapsed time since the program started
        :param position_array: position data with tags in array
        """
        output = str(index)
        output += " Time: "
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
        output += ave_hertz_str

        output += " | "
        for element in position_array:
            output += str(element) + " "
        print(output)

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
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
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
        
        print(output)

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
        elapsed_time_str = DataFunctions.str_set_length(elapsed, 10)
        output += elapsed_time_str
        output += " Hz: "
        ave_hertz = DataFunctions.find_average_hertz(index, elapsed)
        ave_hertz_str = DataFunctions.str_set_length(ave_hertz, 5)
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
            output += (" | Vel: " + "X: " + DataFunctions.str_set_length(velocity_x, 6)
                           + " Y: " + DataFunctions.str_set_length(velocity_y, 6)
                           + " Z: " + DataFunctions.str_set_length(velocity_z, 6))
        print(output)

    @staticmethod
    def format_sensor_data(sensor_data, multiple_attributes_to_log):
        """
        :param sensor_data:
        :param multiple_attributes_to_log:
        :return:
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
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.acceleration.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.acceleration.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.acceleration.z, 8))
                elif attribute_to_log == "magnetic":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.magnetic.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.magnetic.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.magnetic.z, 8))
                elif attribute_to_log == "angular velocity":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.angular_vel.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.angular_vel.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.angular_vel.z, 8))
                elif attribute_to_log == "euler angles":
                    line_of_data.append("heading:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.euler_angles.heading, 8))
                    line_of_data.append("roll:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.euler_angles.roll, 8))
                    line_of_data.append("pitch:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.euler_angles.pitch, 8))
                elif attribute_to_log == "quaternion":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.quaternion.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.quaternion.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.quaternion.z, 8))
                    line_of_data.append("w:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.quaternion.w, 8))
                elif attribute_to_log == "linear acceleration":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.linear_acceleration.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.linear_acceleration.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.linear_acceleration.z, 8))
                elif attribute_to_log == "gravity":
                    line_of_data.append("x:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.gravity_vector.x, 8))
                    line_of_data.append("y:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.gravity_vector.y, 8))
                    line_of_data.append("z:")
                    line_of_data.append(DataFunctions.str_set_length(
                        sensor_data.gravity_vector.z, 8))
                data_dictionary[attribute_to_log.title()] = line_of_data
            return data_dictionary
        except AttributeError:
            return " Error in data"

    @staticmethod
    def print_data_error_message(index, elapsed_time, message="Error, no data"):
        output = (str(index) + " Time: "
                  + DataFunctions.str_set_length(elapsed_time, 10) + " "
                  + message)
        print(output)
