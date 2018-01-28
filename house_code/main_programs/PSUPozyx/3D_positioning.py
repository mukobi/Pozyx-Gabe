#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs

Modified by Gabriel Mukobi for use with the PSU Pozyx Configurator Graphical
User Interface and incorporating the sensor data and multitag localization
scripts. That is, this file smartly collects 3D position and optionally sensor
data at the same time for 1 or more remote devices based on the active settings
in the PSUPozyx GUI.

"""
import time
import sys
import pythonosc
from pypozyx import *
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pythonosc.udp_client import SimpleUDPClient
from modules.console_logging_functions import CondensedConsoleLogging as Console
from modules.configuration import Configuration as Configuration
from modules.file_writing import FileOpener
from modules.file_writing import PositioningFileWriting as FileIO
from modules.pozyx_osc import PozyxUDP
sys.path.append(sys.path[0] + "/..")
from constants import definitions


class PositionOutputContainer:
    def __init__(self, i_tag, i_position, i_smoothed_x, i_smoothed_y, i_smoothed_z,
                 i_sensor_data, i_loop_status):
        self.tag = i_tag
        self.position = i_position
        self.sensor_data = i_sensor_data
        self.loop_status = i_loop_status
        self.smoothed_x = i_smoothed_x
        self.smoothed_y = i_smoothed_y
        self.smoothed_z = i_smoothed_z
        self.velocity_x = ""
        self.velocity_y = ""
        self.velocity_z = ""


class Positioning(object):
    """Continuously performs multitag positioning"""
    def __init__(self, i_pozyx, i_tags, i_anchors, i_to_get_sensor_data,
                 i_algorithm=POZYX_POS_ALG_UWB_ONLY, i_dimension=POZYX_3D, i_height=1000):
        self.pozyx = i_pozyx
        self.tags = i_tags
        self.anchors = i_anchors
        self.algorithm = i_algorithm
        self.dimension = i_dimension
        self.height = i_height
        self.to_get_sensor_data = i_to_get_sensor_data

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        self.set_anchors_manual()

    def loop(self, loop_position_data_array):
        """Performs positioning and prints the results."""
        for idx, loop_tag in enumerate(self.tags):
            # get device position
            position = Coordinates()
            loop_status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=loop_tag)

            # get motion data
            sensor_data = SensorData()
            calibration_status = SingleRegister()
            if self.to_get_sensor_data:
                sensor_data.data_format = 'IhhhhhhhhhhhhhhhhhhhhhhB'
                if loop_tag is not None or self.pozyx.checkForFlag(
                        POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
                    loop_status = self.pozyx.getAllSensorData(sensor_data, loop_tag)
                    loop_status &= self.pozyx.getCalibrationStatus(calibration_status, loop_tag)

            single = loop_position_data_array[idx]
            single.tag = loop_tag
            single.position = position
            single.sensor_data = sensor_data
            single.loop_status = loop_status

    def set_anchors_manual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for anchor_manual_tag in self.tags:
            status = self.pozyx.clearDevices(anchor_manual_tag)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, anchor_manual_tag)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(
                    POZYX_ANCHOR_SEL_AUTO, len(anchors), remote_id=anchor_manual_tag)
            self.print_configuration_result(status, anchor_manual_tag)

    def print_configuration_result(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.print_error_code("configuration", tag_id)

    def print_error_code(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, None)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))


def apply_ema_filter(loop_position_data_array, loop_alpha_pos, loop_alpha_vel):
    for single_device_data in loop_position_data_array:
        # EMA filter calculations
        if type(single_device_data.position.x) is int:
            old_smoothed_x, old_smoothed_y, old_smoothed_z = (
                single_device_data.smoothed_x, single_device_data.smoothed_y, single_device_data.smoothed_z)

            single_device_data.smoothed_x = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_x
                + loop_alpha_pos * single_device_data.position.x)
            new_smoothed_x = single_device_data.smoothed_x
            single_device_data.smoothed_y = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_y
                + loop_alpha_pos * single_device_data.position.y)
            new_smoothed_y = single_device_data.smoothed_y
            single_device_data.smoothed_z = (
                (1 - loop_alpha_pos) * single_device_data.smoothed_z
                + loop_alpha_pos * single_device_data.position.z)
            new_smoothed_z = single_device_data.smoothed_z

            if not (time_difference == 0) and not (elapsed <= 0.001):
                if single_device_data.velocity_x == "":
                    single_device_data.velocity_x = 0.0
                    single_device_data.velocity_y = 0.0
                    single_device_data.velocity_z = 0.0
                measured_velocity_x = (new_smoothed_x - old_smoothed_x) / time_difference
                measured_velocity_y = (new_smoothed_y - old_smoothed_y) / time_difference
                measured_velocity_z = (new_smoothed_z - old_smoothed_z) / time_difference
                if not smooth_velocity:
                    single_device_data.velocity_x = measured_velocity_x
                    single_device_data.velocity_y = measured_velocity_y
                    single_device_data.velocity_z = measured_velocity_z
                    continue
                # smooth velocity
                single_device_data.velocity_x = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_x
                    + loop_alpha_vel * measured_velocity_x)
                single_device_data.velocity_y = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_y
                    + loop_alpha_vel * measured_velocity_y)
                single_device_data.velocity_z = (
                    (1 - loop_alpha_vel) * single_device_data.velocity_z
                    + loop_alpha_vel * measured_velocity_z)


class ContinueI(Exception):
    pass


continue_i = ContinueI()


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = Configuration.get_correct_serial_port()

    # import properties from saved properties file
    config = Configuration.get_properties()
    tags = config.tags
    anchors = config.anchors
    attributes_to_log = config.attributes_to_log
    to_use_file = config.use_file
    filename = config.data_file
    to_get_sensor_data = not attributes_to_log == []
    alpha_pos = config.position_smooth
    alpha_vel = config.velocity_smooth
    smooth_velocity = alpha_vel < 1.00

    position_data_array = []
    for tag in tags:
        position_data_array.append(PositionOutputContainer(None, None, 0, 0, 0, None, None))
    if not tags:
        sys.exit("Please add at least one remote device for 1D ranging.")

    logfile = None
    if to_use_file:
        logfile = FileOpener.create_csv(filename)
        FileIO.write_position_headers_to_file(logfile, tags, attributes_to_log)

    pozyx = PozyxSerial(serial_port)
    r = Positioning(pozyx, tags, anchors, to_get_sensor_data)
    r.setup()

    # wait for motion data to work before running main loop
    if to_get_sensor_data:
        not_started = True
        while not_started:
            r.loop(position_data_array)
            not_started = position_data_array[0].sensor_data.pressure == 0
            for single_data in position_data_array:
                # Initialize EMA filter
                if type(single_data.position.x) is int:
                    single_data.smoothed_x = single_data.position.x
                    single_data.smoothed_y = single_data.position.y
                    single_data.smoothed_y = single_data.position.y

    try:
        # update message client after data working - don't send initial 0 range over osc
        ip, network_port = "127.0.0.1", 8888
        osc_udp_client = SimpleUDPClient(ip, network_port)
        pozyxOSC = PozyxUDP(osc_udp_client)

        index = 0
        start = time.time()
        new_time = 0.0
        time.sleep(0.00001)

        while True:
            try:
                elapsed = time.time() - start
                old_time = new_time
                new_time = elapsed
                time_difference = new_time - old_time

                r.loop(position_data_array)
                for dataset in position_data_array:
                    if dataset.position.x == 0 and dataset.position.y == 0 and dataset.position.z == 0:
                        raise continue_i

                apply_ema_filter(position_data_array, alpha_pos, alpha_vel)

                Console.print_3d_positioning_output(
                    index, elapsed, position_data_array, attributes_to_log)

                if to_use_file:
                    FileIO.write_position_data_to_file(logfile, index, elapsed, time_difference,
                                                       position_data_array, attributes_to_log)

                if position_data_array[0].loop_status == POZYX_SUCCESS:
                    data_type = ([definitions.DATA_TYPE_POSITIONING, definitions.DATA_TYPE_MOTION_DATA] if attributes_to_log
                                 else [definitions.DATA_TYPE_POSITIONING])
                    try:
                        pozyxOSC.send_message(elapsed, tags, position_data_array, data_type)
                    except pythonosc.osc_message.ParseError:
                        pass

                index = index + 1

            except ContinueI:
                continue

    except KeyboardInterrupt:
        pass

    finally:
        if to_use_file:
            logfile.close()
