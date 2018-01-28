from .data_functions import DataFunctions as DataFunctions


class FileOpener:
    @staticmethod
    def create_csv(filename):
        try:
            f = open(filename, 'r')
            f.close()
        except FileNotFoundError:
            # doesn't already exist
            return open(filename, 'w')
        # file does exist
        if filename.endswith(".csv"):
            filename = filename[:-4]
        index = 1
        while True:
            numbered_file = filename + " (" + str(index) + ").csv"
            try:
                f = open(numbered_file, 'r')
                f.close()
            except FileNotFoundError:
                # doesn't already exist
                return open(numbered_file, 'w')
            index += 1


class MotionDataFileWriting:
    @staticmethod
    def write_headers_to_file(file, tags, attributes_to_log):
        header = "Index,Time,Difference,Hz,AveHz,"
        for tag in tags:
            if "pressure" in attributes_to_log:
                header += (hex(tag) + " Pressure,")
            if "acceleration" in attributes_to_log:
                header += (hex(tag) + " Acceleration-X,")
                header += (hex(tag) + " Acceleration-Y,")
                header += (hex(tag) + " Acceleration-Z,")
            if "magnetic" in attributes_to_log:
                header += (hex(tag) + " Magnetic-X,")
                header += (hex(tag) + " Magnetic-Y,")
                header += (hex(tag) + " Magnetic-Z,")
            if "angular velocity" in attributes_to_log:
                header += (hex(tag) + " Angular-Vel-X,")
                header += (hex(tag) + " Angular-Vel-Y,")
                header += (hex(tag) + " Angular-Vel-Z,")
            if "euler angles" in attributes_to_log:
                header += (hex(tag) + " Heading,")
                header += (hex(tag) + " Roll,")
                header += (hex(tag) + " Pitch,")
            if "quaternion" in attributes_to_log:
                header += (hex(tag) + " Quaternion-X,")
                header += (hex(tag) + " Quaternion-Y,")
                header += (hex(tag) + " Quaternion-Z,")
                header += (hex(tag) + " Quaternion-W,")
            if "linear acceleration" in attributes_to_log:
                header += (hex(tag) + " Linear-Acceleration-X,")
                header += (hex(tag) + " Linear-Acceleration-Y,")
                header += (hex(tag) + " Linear-Acceleration-Z,")
            if "gravity" in attributes_to_log:
                header += (hex(tag) + " Gravity-X,")
                header += (hex(tag) + " Gravity-Y,")
                header += (hex(tag) + " Gravity-Z,")
        header += "\n"
        file.write(header)

    @staticmethod
    def write_line_of_data_to_file(file, index, elapsed_time, time_difference, loop_output_array, attributes_to_log):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        for single_output in loop_output_array:
            motion = single_output.sensor_data
            if "pressure" in attributes_to_log:
                output += (str(motion.pressure) + ",")
            if "acceleration" in attributes_to_log:
                output += (str(motion.acceleration.x) + ",")
                output += (str(motion.acceleration.y) + ",")
                output += (str(motion.acceleration.z) + ",")
            if "magnetic" in attributes_to_log:
                output += (str(motion.magnetic.x) + ",")
                output += (str(motion.magnetic.y) + ",")
                output += (str(motion.magnetic.z) + ",")
            if "angular velocity" in attributes_to_log:
                output += (str(motion.angular_vel.x) + ",")
                output += (str(motion.angular_vel.y) + ",")
                output += (str(motion.angular_vel.z) + ",")
            if "euler angles" in attributes_to_log:
                output += (str(motion.euler_angles.heading) + ",")
                output += (str(motion.euler_angles.roll) + ",")
                output += (str(motion.euler_angles.pitch) + ",")
            if "quaternion" in attributes_to_log:
                output += (str(motion.quaternion.x) + ",")
                output += (str(motion.quaternion.y) + ",")
                output += (str(motion.quaternion.z) + ",")
                output += (str(motion.quaternion.w) + ",")
            if "linear acceleration" in attributes_to_log:
                output += (str(motion.linear_acceleration.x) + ",")
                output += (str(motion.linear_acceleration.y) + ",")
                output += (str(motion.linear_acceleration.z) + ",")
            if "gravity" in attributes_to_log:
                output += (str(motion.gravity_vector.x) + ",")
                output += (str(motion.gravity_vector.y) + ",")
                output += (str(motion.gravity_vector.z) + ",")
        output += "\n"
        file.write(output)


class RangingFileWriting:
    @staticmethod
    def write_range_headers_to_file(file, tags, attributes_to_log):
        header = "Index,Time,Difference,Hz,AveHz,"
        for tag in tags:
            if "pressure" in attributes_to_log:
                header += (hex(tag) + " Pressure,")
            if "acceleration" in attributes_to_log:
                header += (hex(tag) + " Acceleration-X,")
                header += (hex(tag) + " Acceleration-Y,")
                header += (hex(tag) + " Acceleration-Z,")
            if "magnetic" in attributes_to_log:
                header += (hex(tag) + " Magnetic-X,")
                header += (hex(tag) + " Magnetic-Y,")
                header += (hex(tag) + " Magnetic-Z,")
            if "angular velocity" in attributes_to_log:
                header += (hex(tag) + " Angular-Vel-X,")
                header += (hex(tag) + " Angular-Vel-Y,")
                header += (hex(tag) + " Angular-Vel-Z,")
            if "euler angles" in attributes_to_log:
                header += (hex(tag) + " Heading,")
                header += (hex(tag) + " Roll,")
                header += (hex(tag) + " Pitch,")
            if "quaternion" in attributes_to_log:
                header += (hex(tag) + " Quaternion-X,")
                header += (hex(tag) + " Quaternion-Y,")
                header += (hex(tag) + " Quaternion-Z,")
                header += (hex(tag) + " Quaternion-W,")
            if "linear acceleration" in attributes_to_log:
                header += (hex(tag) + " Linear-Acceleration-X,")
                header += (hex(tag) + " Linear-Acceleration-Y,")
                header += (hex(tag) + " Linear-Acceleration-Z,")
            if "gravity" in attributes_to_log:
                header += (hex(tag) + " Gravity-X,")
                header += (hex(tag) + " Gravity-Y,")
                header += (hex(tag) + " Gravity-Z,")
            header += hex(tag) + " Range,"
            header += hex(tag) + " Smoothed Range,"
            header += hex(tag) + " Velocity,"
        header += "\n"
        file.write(header)

    @staticmethod
    def write_range_data_to_file(file, index, elapsed_time, time_difference, loop_output_array, attributes_to_log):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        for single_output in loop_output_array:
            motion = single_output.sensor_data
            if "pressure" in attributes_to_log:
                output += (str(motion.pressure) + ",")
            if "acceleration" in attributes_to_log:
                output += (str(motion.acceleration.x) + ",")
                output += (str(motion.acceleration.y) + ",")
                output += (str(motion.acceleration.z) + ",")
            if "magnetic" in attributes_to_log:
                output += (str(motion.magnetic.x) + ",")
                output += (str(motion.magnetic.y) + ",")
                output += (str(motion.magnetic.z) + ",")
            if "angular velocity" in attributes_to_log:
                output += (str(motion.angular_vel.x) + ",")
                output += (str(motion.angular_vel.y) + ",")
                output += (str(motion.angular_vel.z) + ",")
            if "euler angles" in attributes_to_log:
                output += (str(motion.euler_angles.heading) + ",")
                output += (str(motion.euler_angles.roll) + ",")
                output += (str(motion.euler_angles.pitch) + ",")
            if "quaternion" in attributes_to_log:
                output += (str(motion.quaternion.x) + ",")
                output += (str(motion.quaternion.y) + ",")
                output += (str(motion.quaternion.z) + ",")
                output += (str(motion.quaternion.w) + ",")
            if "linear acceleration" in attributes_to_log:
                output += (str(motion.linear_acceleration.x) + ",")
                output += (str(motion.linear_acceleration.y) + ",")
                output += (str(motion.linear_acceleration.z) + ",")
            if "gravity" in attributes_to_log:
                output += (str(motion.gravity_vector.x) + ",")
                output += (str(motion.gravity_vector.y) + ",")
                output += (str(motion.gravity_vector.z) + ",")
            output += str(single_output.device_range.distance) + ","
            output += str(single_output.smoothed_range) + ","
            if elapsed_time == 0: # don't log zero velocity
                output += ","
            else:
                output += str(single_output.velocity) + ","
        output += "\n"
        file.write(output)


class PositioningFileWriting:
    @staticmethod
    def write_position_headers_to_file(file, tags, attributes_to_log):
        header = "Index,Time,Difference,Hz,AveHz,"
        for tag in tags:
            if "pressure" in attributes_to_log:
                header += (hex(tag) + " Pressure,")
            if "acceleration" in attributes_to_log:
                header += (hex(tag) + " Acceleration-X,")
                header += (hex(tag) + " Acceleration-Y,")
                header += (hex(tag) + " Acceleration-Z,")
            if "magnetic" in attributes_to_log:
                header += (hex(tag) + " Magnetic-X,")
                header += (hex(tag) + " Magnetic-Y,")
                header += (hex(tag) + " Magnetic-Z,")
            if "angular velocity" in attributes_to_log:
                header += (hex(tag) + " Angular-Vel-X,")
                header += (hex(tag) + " Angular-Vel-Y,")
                header += (hex(tag) + " Angular-Vel-Z,")
            if "euler angles" in attributes_to_log:
                header += (hex(tag) + " Heading,")
                header += (hex(tag) + " Roll,")
                header += (hex(tag) + " Pitch,")
            if "quaternion" in attributes_to_log:
                header += (hex(tag) + " Quaternion-X,")
                header += (hex(tag) + " Quaternion-Y,")
                header += (hex(tag) + " Quaternion-Z,")
                header += (hex(tag) + " Quaternion-W,")
            if "linear acceleration" in attributes_to_log:
                header += (hex(tag) + " Linear-Acceleration-X,")
                header += (hex(tag) + " Linear-Acceleration-Y,")
                header += (hex(tag) + " Linear-Acceleration-Z,")
            if "gravity" in attributes_to_log:
                header += (hex(tag) + " Gravity-X,")
                header += (hex(tag) + " Gravity-Y,")
                header += (hex(tag) + " Gravity-Z,")
            header += hex(tag) + " Measured-X,"
            header += hex(tag) + " Measured-Y,"
            header += hex(tag) + " Measured-Z,"
            header += hex(tag) + " Smoothed-X,"
            header += hex(tag) + " Smoothed-Y,"
            header += hex(tag) + " Smoothed-Z,"
            header += hex(tag) + " Velocity-X,"
            header += hex(tag) + " Velocity-Y,"
            header += hex(tag) + " Velocity-Z,"
        header += "\n"
        file.write(header)

    @staticmethod
    def write_position_data_to_file(file, index, elapsed_time, time_difference, loop_output_array, attributes_to_log):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + "," + str(elapsed_time) + ","
                  + str(time_difference) + "," + str(hz) + ","
                  + str(ave_hz) + ",")
        for single_output in loop_output_array:
            motion = single_output.sensor_data
            if "pressure" in attributes_to_log:
                output += (str(motion.pressure) + ",")
            if "acceleration" in attributes_to_log:
                output += (str(motion.acceleration.x) + ",")
                output += (str(motion.acceleration.y) + ",")
                output += (str(motion.acceleration.z) + ",")
            if "magnetic" in attributes_to_log:
                output += (str(motion.magnetic.x) + ",")
                output += (str(motion.magnetic.y) + ",")
                output += (str(motion.magnetic.z) + ",")
            if "angular velocity" in attributes_to_log:
                output += (str(motion.angular_vel.x) + ",")
                output += (str(motion.angular_vel.y) + ",")
                output += (str(motion.angular_vel.z) + ",")
            if "euler angles" in attributes_to_log:
                output += (str(motion.euler_angles.heading) + ",")
                output += (str(motion.euler_angles.roll) + ",")
                output += (str(motion.euler_angles.pitch) + ",")
            if "quaternion" in attributes_to_log:
                output += (str(motion.quaternion.x) + ",")
                output += (str(motion.quaternion.y) + ",")
                output += (str(motion.quaternion.z) + ",")
                output += (str(motion.quaternion.w) + ",")
            if "linear acceleration" in attributes_to_log:
                output += (str(motion.linear_acceleration.x) + ",")
                output += (str(motion.linear_acceleration.y) + ",")
                output += (str(motion.linear_acceleration.z) + ",")
            if "gravity" in attributes_to_log:
                output += (str(motion.gravity_vector.x) + ",")
                output += (str(motion.gravity_vector.y) + ",")
                output += (str(motion.gravity_vector.z) + ",")
            output += str(single_output.position.x) + ","
            output += str(single_output.position.y) + ","
            output += str(single_output.position.z) + ","
            output += str(single_output.smoothed_x) + ","
            output += str(single_output.smoothed_y) + ","
            output += str(single_output.smoothed_z) + ","
            if elapsed_time == 0: # don't log zero velocities
                output += ",,,"
            else:
                output += str(single_output.velocity_x) + ","
                output += str(single_output.velocity_y) + ","
                output += str(single_output.velocity_z) + ","
        output += "\n"
        file.write(output)
