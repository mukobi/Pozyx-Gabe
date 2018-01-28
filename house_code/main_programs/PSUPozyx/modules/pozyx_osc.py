import sys
sys.path.append(sys.path[0] + "/..")
from constants import definitions
from modules import udp


class PozyxUDP:
    def __init__(self, osc_udp_client_in=None):
        self.producer = udp.Producer()

    def send_message(self, elapsed_time, tags, data_array, data_types):
        message_array = [elapsed_time]
        for idx, tag in enumerate(tags):
            message_array.append(tag)
            data_for_tag = data_array[idx]
            message_array = message_array + self.add_range_data(data_for_tag, data_types)
            message_array = message_array + self.add_position_data(data_for_tag, data_types)
            message_array = message_array + self.add_motion_data(data_for_tag, data_types)
        self.producer.send(message_array)

    @staticmethod
    def add_range_data(data_for_tag, data_types):
        if definitions.DATA_TYPE_RANGING not in data_types:
            return [0] * 2
        range = data_for_tag.smoothed_range
        velocity = data_for_tag.velocity
        return [range, velocity]

    @staticmethod
    def add_position_data(data_for_tag, data_types):
        if definitions.DATA_TYPE_POSITIONING not in data_types:
            return [0] * 6
        pos_x = data_for_tag.smoothed_x
        pos_y = data_for_tag.smoothed_y
        pos_z = data_for_tag.smoothed_z

        vel_x = data_for_tag.velocity_x
        vel_y = data_for_tag.velocity_y
        vel_z = data_for_tag.velocity_z

        return [pos_x, pos_y, pos_z, vel_x, vel_y, vel_z]

    @staticmethod
    def add_motion_data(data_for_tag, data_types):
        if definitions.DATA_TYPE_MOTION_DATA not in data_types:
            return [0] * 23
        return [data_for_tag.sensor_data.pressure,
                data_for_tag.sensor_data.acceleration.x,
                data_for_tag.sensor_data.acceleration.y,
                data_for_tag.sensor_data.acceleration.z,
                data_for_tag.sensor_data.magnetic.x,
                data_for_tag.sensor_data.magnetic.y,
                data_for_tag.sensor_data.magnetic.z,
                data_for_tag.sensor_data.angular_vel.x,
                data_for_tag.sensor_data.angular_vel.y,
                data_for_tag.sensor_data.angular_vel.z,
                data_for_tag.sensor_data.euler_angles.heading,
                data_for_tag.sensor_data.euler_angles.roll,
                data_for_tag.sensor_data.euler_angles.pitch,
                data_for_tag.sensor_data.quaternion.w,
                data_for_tag.sensor_data.quaternion.x,
                data_for_tag.sensor_data.quaternion.y,
                data_for_tag.sensor_data.quaternion.z,
                data_for_tag.sensor_data.linear_acceleration.x,
                data_for_tag.sensor_data.linear_acceleration.y,
                data_for_tag.sensor_data.linear_acceleration.z,
                data_for_tag.sensor_data.gravity_vector.x,
                data_for_tag.sensor_data.gravity_vector.y,
                data_for_tag.sensor_data.gravity_vector.z]
