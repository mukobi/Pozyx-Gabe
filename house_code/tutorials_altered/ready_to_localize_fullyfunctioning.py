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

from pypozyx import *
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import time as t

def strSetLength(number, length):
    numString = str(number);
    numLength = len(numString);
    while len(numString) < length:
        numString += "0"
    while len(numString) > length:
        numString = numString[:-1]
    return numString

def findtotaldistance(position, prev_pos, total_distance):
    """Function to determine the total distance travelled by the Pozyx device"""
    from math import sqrt
    #
    if prev_pos != 0:
        temp_dist = sqrt((position.x - prev_pos.x)**2 + (position.y - prev_pos.y)**2 +(position.z - prev_pos.z)**2)
        total_distance += temp_dist
    else:
        temp_dist = sqrt((position.x)**2 + (position.y)**2 +(position.z)**2)
        total_distance += temp_dist
#    import pdb; pdb.set_trace()
    return total_distance


def write_to_file(singleLineOutput, filename):
    """Opening the file to add the position data"""
    if filename == "":
        filename = "default_position_test.txt"
    with open(filename, "a") as f:
        f.write (singleLineOutput + '\n')

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
        print("------------POZYX POSITIONING V1.1 -------------")
        print("NOTES: ")
        print("- No parameters required.")
        print()
        print("- System will auto start configuration")
        print()
        print("- System will auto start positioning")
        print("------------POZYX POSITIONING V1.1 --------------")
        print()
        print("START Ranging: ")
        self.pozyx.clearDevices(self.remote_id)
        self.setAnchorsManual()
        self.printPublishConfigurationResult()

    def loop(self, elapsed, timeDifference, index = None):
        """Performs positioning and displays/exports the results."""
        singleLineOutput = ""
        position = Coordinates()
        status = self.pozyx.doPositioning(
            position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
        if status == POZYX_SUCCESS:
            singleLineOutput = self.printPublishPosition(position, elapsed, timeDifference)
            return singleLineOutput, position, status
        else:
            self.printPublishErrorCode("positioning")
            return singleLineOutput, position, status

    def printPublishPosition(self, position, elapsed, timeDifference):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        network_id = self.remote_id
        if network_id is None:
            network_id = 0
        print("POS ID {}, x(mm): {pos.x} y(mm): {pos.y} z(mm): {pos.z}".format(
            "0x%0.4x" % network_id, pos=position))

        hertz = 1 / timeDifference
        elapsed = strSetLength(elapsed, 20)
        timeDifference = strSetLength(timeDifference, 20)
        hertz = strSetLength(hertz, 5)
        output = str(index) + " Total: " + elapsed + " Diff: " + timeDifference + " Hz: " + hertz + " Pos: " + "{pos.x} {pos.y} {pos.z}".format("0x%0.4x" % network_id, pos=position)

        return output

        """Sending data to OSC packet"""
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
                    "/anchor", [anchor.network_id, int(anchor_coordinates.x), int(anchor_coordinates.y), int(anchor_coordinates.z)])
                sleep(0.025)

if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[0].device

    remote_id = 0x614e                 # remote device network ID
    remote = True                   # whether to use a remote device
    if not remote:
        remote_id = None

    index = 0
    start = t.time()
    oldTime = 0
    newTime = 0


    use_processing = False             # enable to send position data through OSC
    ip = "127.0.0.1"                   # IP for the OSC UDP
    network_port = 8888                # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)
    # necessary data for calibration, change the IDs and coordinates yourself
    anchors = [DeviceCoordinates(0x605d, 1, Coordinates(0, 1669, 1016)),
               DeviceCoordinates(0x6020, 1, Coordinates(3024, 5886, 1535)),
               DeviceCoordinates(0x604f, 1, Coordinates(3545, 0, 2595)),
               DeviceCoordinates(0x6129, 1, Coordinates(5182, 3052, 198))]

    algorithm = POZYX_POS_ALG_UWB_ONLY  # positioning algorithm to use
    dimension = POZYX_3D               # positioning dimension
    height = 1000                      # height of device, required in 2.5D positioning

    filename = input("Please enter a filename: ")
    filename = filename + ".txt"

    total_distance = 0
    prev_pos = 0

    pozyx = PozyxSerial(serial_port)
    r = ReadyToLocalize(pozyx, osc_udp_client, anchors, algorithm, dimension, height, remote_id)
    r.setup()
    while True:
        elapsed = (t.time() - start)
        oldTime = newTime
        newTime = elapsed
        timeDifference = newTime - oldTime



        singleLineOutput, pos, status = r.loop(elapsed, timeDifference)
        total_distance = findtotaldistance(pos, prev_pos, total_distance)
        prev_pos = pos
        singleLineOutput = singleLineOutput + " Dist: " + strSetLength(total_distance, 15)

        write_to_file(singleLineOutput, filename)
        print(singleLineOutput)


        index += 1
        #firstplane, secondplace, thirdplane, status = r.iterate_file()
        #print(firstplane)
