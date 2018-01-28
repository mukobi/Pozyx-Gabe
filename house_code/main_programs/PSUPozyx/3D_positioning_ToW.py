#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
"""

from time import sleep
from datetime import datetime #for creating the file with date and time in title

from pypozyx import *
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time as t
from modules.user_input_config_functions import UserInputConfigFunctions as UserInput
from modules.file_writing import SensorAndPositionFileWriting as FileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging
from modules.configuration import Configuration as Configuration
from modules.data_averaging import BinData as BinData
import numpy as np
from modules.data_functions import DataFunctions as DataFunctions
from modules.data_functions import Velocity as Velocity
from collections import deque
import copy

from OpenScaleData import OpenScaleData as OS_data
"""
#RealTimePlotting
from modules.real_time_plot import RealTimePlot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
"""

class ReadyToLocalize(object):
    """Continuously calls the Pozyx positioning function and prints its position."""
    def __init__(self, pozyx, osc_udp_client, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()
        network_id = self.remote_id

    def loop(self):
        """Performs positioning and displays/exports the results."""
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
        OpenScale = OS_data()
        if status == POZYX_SUCCESS:
            self.printPublishPosition(position)
            return position, status,
        else:
            #self.printPublishErrorCode("positioning")
            position.x, position.y, position.z = "error", "", ""
            #position.x, position.y, position.z = "error", "error", "error"
            return position, status

    def printPublishPosition(self, position):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, int(position.x), int(position.y), int(position.z)])

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

    def printPublishAnchorConfiguration(self):
        """Prints and potentially publishes the anchor configuration"""
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, int(anchor.coordinates.x), int(anchor.coordinates.y), int(anchor.coordinates.z)])
                sleep(0.025)


if  __name__ == "__main__":
    serial_port = Configuration.get_correct_serial_port()
##    serial_port = get_serial_ports()[0].device

    remote = True                  # whether to use a remote device
    if not remote:
        remote_id = 0x614e

    index = 0
    oldTime = 0
    newTime = 0

    # import properties from saved properties file
    (remote, remote_id, tags, anchors, attributes_to_log, to_use_file,
        filename, use_processing) = Configuration.get_properties()

    use_processing = False

    if not remote:
        remote_id = None

    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    # algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    algorithm = POZYX_POS_ALG_TRACKING  # tracking positioning algorithm
    dimension = POZYX_3D         # positioning dimension
    height = 100000                      # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    r.setup()

    use_velocity = False
    # use_velocity = True

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        if use_velocity:
            FileWriting.write_position_and_velocity_header_to_file(logfile)
        else:
            FileWriting.write_position_header_to_file(logfile)

    """
    #RealTimePlotting
    fig,axes = plt.subplots()
    display_one = RealTimePlot(axes)
    display_one. animate(fig,lambda frame_index: ([], []))
    plt.ylabel("X Velocity")
    #To add more subplots, copy this code and change the object name
    """
    if use_velocity:
        bin_input = DataFunctions.bin_input()       #Determines how many points the user wants to bin

        #Creates the deque binning objects
        bin_pos_x, bin_pos_y, bin_pos_z, prev_bin_pos_x, prev_bin_pos_y, prev_bin_pos_z, bin_time = Velocity.initialize_bins3D(bin_input)

        #Initializing mean calculation variables
        mean_prev_bin_pos_x, mean_prev_bin_pos_y, mean_prev_bin_pos_z = Velocity.initialize_mean_prev_bins3D()

        total_distance = 0             # Initializing total distance
        time_between_2500_and_4500 = 0              # Initializing different bins for velocity intervals
        time_between_4500_and_6500 = 0
        time_between_6500_and_8500 = 0
        time_above_8500 = 0

    start = t.time()
    try:
        while True:
            elapsed=(t.time()-start)
            oldTime = newTime
            newTime = elapsed
            timeDifference = newTime - oldTime

            # Status is used for error handling
            one_cycle_position, status = r.loop()


            if use_velocity and status == POZYX_SUCCESS and one_cycle_position != 0:
                # Updates and returns the new bins
                #bin_pos, bin_time = Velocity.update_bins1D(bin_pos, bin_time, one_cycle_position, newTime)

                # Can equal either simple or linreg
                velocity_method = 'simple'
                #velocity_method = 'linreg'


                # Gets the means of the previous data for calculations
                #mean_prev_bin_pos  = Velocity.update_previous_bins1D(binned_pos)

                bin_pos_x.append(one_cycle_position.x)
                bin_pos_y.append(one_cycle_position.y)
                bin_pos_z.append(one_cycle_position.z)
                bin_time.append(newTime)

                # Calculates the directional velocities, set the method using method argument
                velocity_x = Velocity.find_velocity1D(bin_input, bin_pos_x, prev_bin_pos_x, bin_time, prev_bin_time, velocity_method)
                velocity_y = Velocity.find_velocity1D(bin_input, bin_pos_y, prev_bin_pos_y, bin_time, prev_bin_time, velocity_method)
                velocity_z = Velocity.find_velocity1D(bin_input, bin_pos_z, prev_bin_pos_z, bin_time, prev_bin_time, velocity_method)
                
 
                prev_bin_pos_x = copy.copy(bin_pos_x)
                prev_bin_pos_y = copy.copy(bin_pos_y)
                prev_bin_pos_z = copy.copy(bin_pos_z)


            else:
                velocity_x = ''
                velocity_y = ''
                velocity_z = ''



            # Logs the data to console
            if use_velocity:
                ConsoleLogging.log_position_and_velocity_to_console(index, elapsed, one_cycle_position, velocity_x, velocity_y, velocity_z)
            else:
                ConsoleLogging.log_position_to_console(index, elapsed, one_cycle_position)

            if to_use_file:             # writes the data returned from the iterate_file method to the file
                if use_velocity:
                    if index > bin_input:   # Accounts for the time it takes to get accurate velocity calculations
                        FileWriting.write_position_and_velocity_data_to_file(
                            index, elapsed, timeDifference, logfile, one_cycle_position,
                            velocity_x, velocity_y, velocity_z)
                    else:                   # Returns 0 for velocity until it provides complete calculations
                        FileWriting.write_position_and_velocity_data_to_file(
                            index, elapsed, timeDifference, logfile, one_cycle_position,
                            np.nan, np.nan, np.nan)
                else:
                    FileWriting.write_position_data_to_file(index, elapsed, timeDifference, logfile, one_cycle_position)

            index = index + 1                                     # increment data index

    except KeyboardInterrupt:  # this allows Windows users to exit the while iterate_file by pressing ctrl+c
        pass

    if to_use_file:
        logfile.close()
