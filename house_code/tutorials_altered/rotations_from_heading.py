#!/usr/bin/env python
"""
The pozyx ranging demo (c) Pozyx Labs
please check out https://www.pozyx.io/Documentation/Tutorials/getting_started/Python

This demo requires one (or two) pozyx shields. It demonstrates the 3D orientation and the functionality
to remotely read register data from a pozyx device. Connect one of the Pozyx devices with USB and run this script.

This demo reads the following sensor data:
- pressure
- acceleration
- magnetic field strength
- angular velocity
- the heading, roll and pitch
- the quaternion rotation describing the 3D orientation of the device. This can be used to transform from the body coordinate system to the world coordinate system.
- the linear acceleration (the acceleration excluding gravity)
- the gravitational vector

The data can be viewed in the Processing sketch orientation_3D.pde
"""
from time import time

from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_writing import MotionDataFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.data_functions import DataFunctions as DataFunctions
import time as t


class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""

    def __init__(self, pozyx, osc_udp_client, remote_id=None):
        self.pozyx = pozyx
        self.remote_id = remote_id

        self.osc_udp_client = osc_udp_client

    def setup(self):
        """There is no specific setup functionality"""
        self.current_time = time()

    def loop(self):
        """Gets new IMU sensor data"""
        sensor_data = SensorData()
        calibration_status = SingleRegister()
        if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
            status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
            status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
            if status == POZYX_SUCCESS:
                self.publishSensorData(sensor_data, calibration_status)
                return sensor_data

        return "Error, no data to print for this line"

    def publishSensorData(self, sensor_data, calibration_status):
        """Makes the OSC sensor data package and publishes it"""
        self.msg_builder = OscMessageBuilder("/sensordata")
        self.msg_builder.add_arg(int(1000 * (time() - self.current_time)))
        current_time = time()
        self.addSensorData(sensor_data)
        self.addCalibrationStatus(calibration_status)
        self.osc_udp_client.send(self.msg_builder.build())

    def addSensorData(self, sensor_data):
        """Adds the sensor data to the OSC message"""
        self.msg_builder.add_arg(sensor_data.pressure)
        self.addComponentsOSC(sensor_data.acceleration)
        self.addComponentsOSC(sensor_data.magnetic)
        self.addComponentsOSC(sensor_data.angular_vel)
        self.addComponentsOSC(sensor_data.euler_angles)
        self.addComponentsOSC(sensor_data.quaternion)
        self.addComponentsOSC(sensor_data.linear_acceleration)
        self.addComponentsOSC(sensor_data.gravity_vector)

    def addComponentsOSC(self, component):
        """Adds a sensor data component to the OSC message"""
        for data in component.data:
            self.msg_builder.add_arg(float(data))

    def addCalibrationStatus(self, calibration_status):
        """Adds the calibration status data to the OSC message"""
        self.msg_builder.add_arg(calibration_status[0] & 0x03)
        self.msg_builder.add_arg((calibration_status[0] & 0x0C) >> 2)
        self.msg_builder.add_arg((calibration_status[0] & 0x30) >> 4)
        self.msg_builder.add_arg((calibration_status[0] & 0xC0) >> 6)

    def write_rotation_and_sensor_data_to_file(self, index, elapsed_time, time_difference,
                                               file, sensor_data, rotations, rps):
        hz = DataFunctions.convert_hertz(time_difference)
        ave_hz = DataFunctions.find_average_hertz(index, elapsed_time)
        output = (str(index) + " " + str(elapsed_time) + " "
                  + str(time_difference) + " " + str(hz) + " "
                  + str(ave_hz) + " ")
        try:
            output += (str(rotations) + " "
                       + str(rps) + " "
                       + str(sensor_data.pressure) + " "
                       + str(sensor_data.acceleration.x) + " "
                       + str(sensor_data.acceleration.y) + " "
                       + str(sensor_data.acceleration.z) + " "
                       + str(sensor_data.magnetic.x) + " "
                       + str(sensor_data.magnetic.y) + " "
                       + str(sensor_data.magnetic.z) + " "
                       + str(sensor_data.angular_vel.x) + " "
                       + str(sensor_data.angular_vel.y) + " "
                       + str(sensor_data.angular_vel.z) + " "
                       + str(sensor_data.euler_angles.heading) + " "
                       + str(sensor_data.euler_angles.roll) + " "
                       + str(sensor_data.euler_angles.pitch) + " "
                       + str(sensor_data.quaternion.x) + " "
                       + str(sensor_data.quaternion.y) + " "
                       + str(sensor_data.quaternion.z) + " "
                       + str(sensor_data.quaternion.w) + " "
                       + str(sensor_data.linear_acceleration.x) + " "
                       + str(sensor_data.linear_acceleration.y) + " "
                       + str(sensor_data.linear_acceleration.z) + " "
                       + str(sensor_data.gravity_vector.x) + " "
                       + str(sensor_data.gravity_vector.y) + " "
                       + str(sensor_data.gravity_vector.z) + " "
                       + "\n")
        except AttributeError:
            for i in range(0, 23):
                output += "error "
            output += "\n"
        file.write(output)

if __name__ == '__main__':
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[2].device

    remote_id = 0x610c                    # remote device network ID
    remote = True                        # whether to use a remote device
    if not remote:
        remote_id = None

    index = 0
    previous_cycle_time = 0
    current_cycle_time = 0

    previous_heading = 0
    current_heading = 0

    total_rotations = 0
    current_rotation_speed = 0

    previous_rotation_time = 0
    current_rotation_time = 0

    """User input configuration section, comment out to use above settings"""
    remote = UserInput.use_remote()
    remote_id = UserInput.get_remote_id(remote)
    to_use_file = UserInput.use_file()
    filename = UserInput.get_filename(to_use_file)

    ip = "127.0.0.1"
    network_port = 8888 

    pozyx = PozyxSerial(serial_port)
    osc_udp_client = SimpleUDPClient(ip, network_port)
    o = Orientation3D(pozyx, osc_udp_client, remote_id)
    o.setup()

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        logfile.write("Index Time Difference Hz AveHz "
                      "Rotations "
                      "RPS "
                      "Pressure "
                      "Acceleration-X Acceleration-Y Acceleration-Z "
                      "Magnetic-X Magnetic-Y Magnetic-Z "
                      "Angular-Vel-X Angular-Vel-Y Angular-Vel-Z "
                      "Heading Roll Pitch "
                      "Quaternion-X Quaternion-Y Quaternion-Z Quaternion-W "
                      "Linear-Acceleration-X Linear-Acceleration-Y Linear-Acceleration-Z "
                      "Gravity-X Gravity-Y Gravity-Z \n")

    start = ConsoleLogging.get_time()
    previous_rotation_time = ConsoleLogging.get_time()

    rotation_time_difference = 0
    try:
        while True:
            # updates elapsed time and time difference
            elapsed = ConsoleLogging.get_elapsed_time(ConsoleLogging, start)
            previous_cycle_time = current_cycle_time
            current_cycle_time = elapsed
            time_difference = current_cycle_time - previous_cycle_time

            one_cycle_sensor_data = o.loop()

            previous_heading = current_heading
            if type(one_cycle_sensor_data) is not str:
                current_heading = one_cycle_sensor_data.euler_angles.heading
            else: print(one_cycle_sensor_data)

            heading_difference = current_heading - previous_heading

            if heading_difference < -2:
                total_rotations += 1
                current_rotation_time = ConsoleLogging.get_time()
                rotation_time_difference = current_rotation_time - previous_rotation_time
                previous_rotation_time = current_rotation_time

            try:
                current_rotation_speed = 1 / rotation_time_difference
            except ZeroDivisionError:
                current_rotation_speed = 0

            print("Index: " + str(index)
                  + " Time: " + DataFunctions.str_append_length(elapsed, 8)
                  + " Hz: " + DataFunctions.str_append_length(DataFunctions.find_average_hertz(index, elapsed), 5)
                  + " Heading: " + DataFunctions.str_append_length(current_heading, 7)
                  + " Rotations: " + str(total_rotations)
                  + " Rotation Speed: " + str(DataFunctions.str_append_length(current_rotation_speed, 8)) + "RPS"
                  )

            if to_use_file:
                o.write_rotation_and_sensor_data_to_file(index, elapsed, time_difference, logfile, one_cycle_sensor_data, total_rotations, current_rotation_speed)
            index += 1                      # increment data index

    # this allows Windows users to exit the while iterate_file by pressing ctrl+c
    except KeyboardInterrupt:
        pass

    if to_use_file:
        logfile.close()



