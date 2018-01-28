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
from time import sleep

from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
import time as t


class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""

    def __init__(self, pozyx, osc_udp_client, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY,
                 dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id

    def setup(self):
        """There is no specific setup functionality"""
        self.current_time = time()
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX POSITIONING V1.0 -------------")
        print("NOTES: ")
        print("- No parameters required.")
        print()
        print("- System will auto start configuration")
        print()
        print("- System will auto start positioning")
        print("------------POZYX POSITIONING V1.0 --------------")
        print()
        print("START Ranging: ")
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()

    def loop(self):
        """Gets new IMU sensor data"""
        # check sensor data status
        sensor_data = SensorData()
        position = Coordinates()
        calibration_status = SingleRegister()
        if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
            status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
            status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
            if status == POZYX_SUCCESS:
                # check position status

                status = self.pozyx.doPositioning(
                    position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
                if status == POZYX_SUCCESS:
                    # self.print_publish_position(position)
                    self.publishSensorData(sensor_data, calibration_status)
                    return sensor_data, position
                else:
                    pass
                    # self.print_publish_error_code("positioning")

        return str(sensor_data) +  " " + str(position)

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

    def setAnchorsManual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        status = self.pozyx.clearDevices(self.remote_id)
        for anchor in self.anchors:
            status &= self.pozyx.addDevice(anchor, self.remote_id)
        if len(anchors) > 4:
            status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors))
        return status

    def printPublishConfigurationResult(self):
        """Prints and potentially publishes the anchor configuration result in a human-readable way."""
        list_size = SingleRegister()

        status = self.pozyx.getDeviceListSize(list_size, self.remote_id)
        print("List size: {0}".format(list_size[0]))
        if list_size[0] != len(self.anchors):
            self.printPublishErrorCode("configuration")
            return
        device_list = DeviceList(list_size=list_size[0])
        status = self.pozyx.getDeviceIds(device_list, self.remote_id)
        print("Calibration result:")
        print("Anchors found: {0}".format(list_size[0]))
        print("Anchor IDs: ", device_list)

        for i in range(list_size[0]):
            anchor_coordinates = Coordinates()
            status = self.pozyx.getDeviceCoordinates(
                device_list[i], anchor_coordinates, self.remote_id)
            print("ANCHOR,0x%0.4x, %s" % (device_list[i], str(anchor_coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [device_list[i], int(anchor_coordinates.x), int(anchor_coordinates.y), int(anchor_coordinates.z)])
                sleep(0.025)


    def printPublishErrorCode(self, operation):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        network_id = self.remote_id
        if network_id is None:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, error_code[0]])
            return
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if status == POZYX_SUCCESS:
            print("ERROR %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error", [operation, network_id, error_code[0]])
        else:
            self.pozyx.getErrorCode(error_code)
            print("ERROR %s, couldn't retrieve remote error code, local error code %s" %
                  (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error", [operation, 0, -1])
            # should only happen when not being able to communicate with a remote Pozyx.
        

if __name__ == '__main__':
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[0].device

    remote_id = 0x610c                   # remote device network ID
    remote = False                        # whether to use a remote device
    # if not remote:
    #     remote_id = None

    index = 0
    previous_cycle_time = 0
    current_cycle_time = 0

    attributes_to_log = ["acceleration"]
    to_use_file = False
    filename = None

    """User input configuration section, comment out to use above settings"""

    remote = UserInput.use_remote()
    # remote_id = UserInput.get_remote_id(remote)
    to_use_file = UserInput.use_file()
    filename = UserInput.get_filename(to_use_file)
    attributes_to_log = UserInput.get_multiple_attributes_to_log()

    use_processing = True
    ip = "127.0.0.1"
    network_port = 8888

    anchors = [DeviceCoordinates(0x605d, 1, Coordinates(0, 1669, 1016)),
               DeviceCoordinates(0x6110, 1, Coordinates(3024, 5886, 1535)),
               DeviceCoordinates(0x604f, 1, Coordinates(3545, 0, 2595)),
               DeviceCoordinates(0x684f, 1, Coordinates(5182, 3052, 198))]

    # algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    algorithm = POZYX_POS_ALG_TRACKING  # tracking positioning algorithm
    dimension = POZYX_3D  # positioning dimension
    height = 1000  # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    osc_udp_client = SimpleUDPClient(ip, network_port)
    o = Orientation3D(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    o.setup()

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        FileWriting.write_sensor_and_position_header_to_file(logfile)

    start = ConsoleLogging.get_time()
    try:
        while True:
            # updates elapsed time and time difference
            elapsed = ConsoleLogging.get_elapsed_time(ConsoleLogging, start)
            previous_cycle_time = current_cycle_time
            current_cycle_time = elapsed
            time_difference = current_cycle_time - previous_cycle_time

            # store iterate_file returns as a tuple or an error message
            loop_results = o.loop()

            if type(loop_results) == tuple:
                one_cycle_sensor_data, one_cycle_position = loop_results
                print(repr(one_cycle_sensor_data))

                formatted_data_dictionary = ConsoleLogging.format_sensor_data(
                    one_cycle_sensor_data, attributes_to_log)
                if type(formatted_data_dictionary) == dict:
                    formatted_data_dictionary["Position"] = [
                        "x:", one_cycle_position.x, "y:", one_cycle_position.y, "z:", one_cycle_position.z]
                ConsoleLogging.log_sensor_data_to_console(index, elapsed, formatted_data_dictionary)
                if to_use_file:
                    FileWriting.write_sensor_and_position_data_to_file(
                        index, elapsed, time_difference,
                        logfile, one_cycle_sensor_data, one_cycle_position)
            # if the iterate_file didn't return a tuple, it returned an error string
            else:
                error_string = loop_results
                ConsoleLogging.print_data_error_message(index, elapsed, error_string)
            index += 1                      # increment data index

    # this allows Windows users to exit the while iterate_file by pressing ctrl+c
    except KeyboardInterrupt:
        pass

    if to_use_file:
        logfile.close()
