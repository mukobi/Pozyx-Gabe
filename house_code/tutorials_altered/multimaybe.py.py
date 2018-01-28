#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python
This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!
"""
from time import sleep, time
import time as t

from pypozyx import *
from pypozyx.definitions.registers import POZYX_EUL_HEADING
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
from modules.file_writing import PositionFileWriting as PositionFileWriting
from modules.console_logging_functions import ConsoleLoggingFunctions as ConsoleLogging

class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, pozyx, osc_udp_client, tags, anchors, algorithm=POZYX_POS_ALG_UWB_ONLY, dimension=POZYX_3D, height=1000, remote_id=None):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.tags = tags
        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.remote_id = remote_id

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V1.1 - -----------\nNOTES: \n- Parameters required:\n\t- Anchors for calibration\n\t- Tags to work with\n\n- System will manually calibration\n\n- System will auto start positioning\n- -----------POZYX MULTITAG POSITIONING V1.1 ------------\nSTART Positioning: ")
        self.setAnchorsManual()
        self.printPublishAnchorConfiguration()

    def loop(self):
        """Performs positioning and prints the results."""
        for tag in self.tags:
            position = Coordinates()
            status = self.pozyx.doPositioning(
                position, self.dimension, self.height, self.algorithm, remote_id=tag)
            if status == POZYX_SUCCESS:
                self.printPublishPosition(position, tag)
                return position
            else:
                self.printPublishErrorCode("positioning", tag)
                return position

    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}, time difference:".format("0x%0.4x" % network_id, position.x, position.y, position.z, timeDifference)
        print(s)
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def setAnchorsManual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag in self.tags:
            status = self.pozyx.clearDevices(tag)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors), remote_id=tag)
            # enable these if you want to save the configuration to the devices.
            # self.pozyx.saveAnchorIds(tag)
            # self.pozyx.saveRegisters([POZYX_ANCHOR_SEL_AUTO], tag)
            self.printPublishConfigurationResult(status, tag)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % network_id, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error_%s" % operation, [0, error_code[0]])

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.pos.x, anchor.pos.y, anchor.pos.z])
                sleep(0.025)


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[0].device

    remote_id = 0x1000                     # remote device network ID
    remote = False                         # whether to use a remote device
    if not remote:
        remote_id = None

    index = 0
    oldTime = 0
    newTime = 0

    use_processing = True               # enable to send position data through OSC
    ip = "127.0.0.1"                       # IP for the OSC UDP
    network_port = 8888                    # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    tags = [0x6120]
    #tags = [0x684f, 0x610c, 0x614e]
    # tags = [0x6055, 0x607a]        # remote tags
    # necessary data for calibration
    anchors = [DeviceCoordinates(0x605d, 1, Coordinates(0, 1669, 1016)),
               DeviceCoordinates(0x6020, 1, Coordinates(3024, 5886, 1535)),
               DeviceCoordinates(0x604f, 1, Coordinates(3545, 0, 2595)),
               DeviceCoordinates(0x6129, 1, Coordinates(5182, 3052, 198))]

    algorithm = POZYX_POS_ALG_UWB_ONLY     # positioning algorithm to use
    dimension = POZYX_3D                   # positioning dimension
    height = 1000                          # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = MultitagPositioning(pozyx, osc_udp_client, tags, anchors,
                            algorithm, dimension, height, remote_id)

    #Quickly made code to make the program write to a file on user input.
    use_file = input("Do you want to write to a file? (y / n)\n")
    if (use_file[0] == "T"
            or use_file[0] == "t"
            or use_file[0] == "y"
            or use_file[0] == "Y"):
        to_use_file = True
        filename = input("What would you like to name your file?\n")
        filename += ".csv"

    logfile = None
    if to_use_file:
        logfile = open(filename, 'a')
        PositionFileWriting.write_position_header_to_file(logfile)

    r.setup()
    start = t.time()
    while True:
        elapsed=(t.time()-start)                              # elapsed time since the program started
        oldTime = newTime                                     # oldTime is the time of previous cycle. It is set to newTime here since newTime has not been updated and still is the old cycle
        newTime = elapsed                                     # newTime is the time of the current cycle.
        timeDifference = newTime - oldTime                    # timeDifference is the differece in time between each subsequent cycle

        one_cycle_position = r.loop()    # the iterate_file method of r prints data to the console and returns what is printed

        ConsoleLogging.log_position_to_console(index, elapsed, one_cycle_position)
        if to_use_file:
            PositionFileWriting.write_position_data_to_file(index, elapsed, timeDifference, logfile, one_cycle_position)              # writes the data returned from the iterate_file method to the file
        index += 1
