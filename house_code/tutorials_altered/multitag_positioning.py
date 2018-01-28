
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
        print("------------POZYX MULTITAG POSITIONING V1.0 - -----------\nNOTES: \n- Parameters required:\n\t- Anchors for calibration\n\t- Tags to work with\n\n- System will manually calibration\n\n- System will auto start positioning\n- -----------POZYX MULTITAG POSITIONING V1.0 ------------\nSTART Positioning: ")
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
            else:
                self.printPublishErrorCode("positioning", tag)

    def setAnchorsManual(self):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag in self.tags:
            status = self.pozyx.clearDevices(tag)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag)
            if len(anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, len(anchors))
            self.printConfigurationResult(status, tag)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        print("POS ID {}, x(mm): {pos.x}, y(mm): {pos.y}, z(mm): {pos.z}".format(
            "0x%0.4x" % network_id, pos=pos))
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, anchor_coordinates.x, anchor_coordinates.y, anchor_coordinates.z])

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, self.remote_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, error code %s" %
                  (operation, "0x%0.4x" % (network_id, str(error_code))))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % [operation, network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error_%s" % operation, [0, error_code[0]])

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.coordinates)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.coordinates.x, anchor.coordinates.y, anchor.coordinates.z])
                sleep(0.025)


if __name__ == "__main__":
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[1].device

    remote_id = 0x610c                     # remote device network ID
    remote = True                         # whether to use a remote device
    if not remote:
        remote_id = None

    use_processing = True                 # enable to send position data through OSC
    ip = "127.0.0.1"                       # IP for the OSC UDP
    network_port = 8888                    # network port for the OSC UDP
    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    tags = [0x610c, 0x684f]        # remote tags
    # necessary data for calibration
    anchors = [DeviceCoordinates(0x6863, 1, Coordinates(0, 4760, 1030)),
               DeviceCoordinates(0x615a, 1, Coordinates(15280, 4760, 1030)),
               DeviceCoordinates(0x607c, 1, Coordinates(0, 0, 1730)),
               DeviceCoordinates(0x6134, 1, Coordinates(7600, 0, 2400))]

    algorithm = POZYX_POS_ALG_UWB_ONLY     # positioning algorithm to use
    dimension = POZYX_3D                   # positioning dimension
    height = 1000                          # height of device, required in 2.5D positioning

    pozyx = PozyxSerial(serial_port)
    r = MultitagPositioning(pozyx, osc_udp_client, tags, anchors,
                            algorithm, dimension, height, remote_id)
    r.setup()
    while True:
        r.loop()
