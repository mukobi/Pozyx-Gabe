from constants import definitions


class FileReading:
    @staticmethod
    def get_header_list(file):
        header_line = file.readline()
        header_list = header_line.split(",")
        # get rid of \n
        header_list[-1] = header_list[-1][:-1]
        return header_list

    @staticmethod
    def determine_data_file_type(header_list):
        position = False
        motion_data = True
        multidevice = True
        try:
            header_list.index("Pressure")
            motion_data = True
        except ValueError:
            # no sensor data
            motion_data = False
        if any("0x" in element[:2] and "-X" in element[-2:] for element in header_list):
            multidevice = True
            position = False
        else:
            # no multidevice
            multidevice = False
            try:
                header_list.index("Position-X")
                position = True
                multidevice = False
            except ValueError:
                # multidevice or positioning
                position = False
                multidevice = False
        if motion_data and position:
            return definitions.DATA_TYPE_POSITIONING_AND_MOTION_DATA
        elif multidevice and position:
            return definitions.DATA_TYPE_MULTIDEVICE_POSITIONING_AND_MOTION_DATA
        elif position and not motion_data:
            return definitions.DATA_TYPE_POSITIONING
        elif multidevice and not motion_data:
            return definitions.DATA_TYPE_MULTIDEVICE_POSITIONING
        elif motion_data and not position and not multidevice:
            return definitions.DATA_TYPE_MOTION_DATA
        else:
            return definitions.DATA_TYPE_DATA_IDENTIFICATION_ERROR

    @staticmethod
    def get_time_difference_index(header_list):
        return header_list.index("Difference")

    @staticmethod
    def get_timestamp_indices(header_list):
        try:
            i_index = header_list.index("Index")
            i_time = header_list.index("Time")
            i_difference = header_list.index("Difference")
            i_hz = header_list.index("Hz")
            i_avehz = header_list.index("AveHz")
        except ValueError:
            return 0, 1, 2, 3, 4
        return i_index, i_time, i_difference, i_hz, i_avehz

    @staticmethod
    def get_data_list(line):
        numbers = line.split(",")
        if numbers[-1] is "\n":
            numbers = numbers[:-1]
        if numbers[-1][-1:] is "\n":
            numbers[-1] = numbers[-1][:-1]
        return numbers
