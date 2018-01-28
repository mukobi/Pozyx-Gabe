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
import time as t


#this function takes a number and rounds it off/adds zeros to return a string of the number with a set character length
#this is to make it easier to read the data from the console since every row will have the same number of data points
def strSetLength(number, length):
    numString = str(number);
    numLength = len(numString);
    while len(numString) < length:
        numString += "0"
    while len(numString) > length:
        numString = numString[:-1]
    return numString


class Orientation3D(object):
    """Reads out all sensor data from either a local or remote Pozyx"""

    def __init__(self, pozyx, osc_udp_client, remote_id=None):
        self.pozyx = pozyx
        self.remote_id = remote_id

        self.osc_udp_client = osc_udp_client

    def setup(self):
        """There is no specific setup functionality"""
        self.current_time = time()

    def loop(self, attributeToLog, elapsed, timeDifference, index=None):
        """Gets new IMU sensor data"""
        sensor_data = SensorData()
        calibration_status = SingleRegister()
        if self.remote_id is not None or self.pozyx.checkForFlag(POZYX_INT_MASK_IMU, 0.01) == POZYX_SUCCESS:
            status = self.pozyx.getAllSensorData(sensor_data, self.remote_id)
            status &= self.pozyx.getCalibrationStatus(calibration_status, self.remote_id)
            if status == POZYX_SUCCESS:
                self.publishSensorData(sensor_data, calibration_status, attributeToLog, elapsed, timeDifference, index)

    def publishSensorData(self, sensor_data, calibration_status, attributeToLog, elapsed, timeDifference, index):
        """Makes the OSC sensor data package and publishes it"""
        self.msg_builder = OscMessageBuilder("/sensordata")
        self.msg_builder.add_arg(int(1000 * (time() - self.current_time)))
        current_time = time()
        self.addSensorData(sensor_data)
        self.printSensorData(sensor_data, attributeToLog, elapsed, timeDifference)
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

    def printSensorData(self, sensor_data, attributeToLog, elapsed, timeDifference):
        """Prints the Sensor Data to the Console"""
        try:
            hertz = 1 / timeDifference
        except ZeroDivisionError:
            hertz = 0
        try:
            averageHertz = index / elapsed
        except ZeroDivisionError:
            averageHertz = 0
        averageHertz = strSetLength(averageHertz, 7)
        elapsed = strSetLength(elapsed, 10)
        timeDifference = strSetLength(timeDifference, 10)
        hertz = strSetLength(hertz, 5)
        
        #this is a longer version of the print output including the difference in time between cycles
        #output = str(index) + " Total: " + elapsed + " Diff: " + timeDifference + " Hz: " + hertz + " "
        output = str(index) + " Total: " + elapsed + " Hz: " + hertz + " AveHz: " + averageHertz + " | "

        if attributeToLog == "pressure":
            output += "Pressure: " + str(sensor_data.pressure) + " pa"
        elif attributeToLog == "acceleration":
            x = strSetLength(sensor_data.acceleration.x, 8)
            y = strSetLength(sensor_data.acceleration.y, 8)
            z = strSetLength(sensor_data.acceleration.z, 8)
            output = "Acceleration: " + " X: " + x + " Y: " + y + " Z: " + z
        elif attributeToLog == "magnetic":
            x = strSetLength(sensor_data.magnetic.x, 8)
            y = strSetLength(sensor_data.magnetic.y, 8)
            z = strSetLength(sensor_data.magnetic.z, 8)
            output += "Magnetic Field: " + " X: " + x + " Y: " + y + " Z: " + z
        elif attributeToLog == "angular velocity":
            x = strSetLength(sensor_data.angular_vel.x, 8)
            y = strSetLength(sensor_data.angular_vel.y, 8)
            z = strSetLength(sensor_data.angular_vel.z, 8)
            output += "Angular Velocity: " + " X: " + x + " Y: " + y + " Z: " + z
        elif attributeToLog == "euler angles":
            heading = strSetLength(sensor_data.euler_angles.heading, 8)
            roll    = strSetLength(sensor_data.euler_angles.roll, 8)
            pitch   = strSetLength(sensor_data.euler_angles.pitch, 8)
            output += "Euler Angles: " + " Heading: " + heading + " Roll: " + roll + " Pitch: " + pitch
        elif attributeToLog == "quaternion":
            x = strSetLength(sensor_data.quaternion.x, 16)
            y = strSetLength(sensor_data.quaternion.y, 16)
            z = strSetLength(sensor_data.quaternion.z, 16)
            w = strSetLength(sensor_data.quaternion.w, 16)
            output += "Quaternion: " + " X: " + x + " Y: " + y + " Z: " + z + " W: " + w
        elif attributeToLog == "linear acceleration":
            x = strSetLength(sensor_data.linear_acceleration.x, 8)
            y = strSetLength(sensor_data.linear_acceleration.y, 8)
            z = strSetLength(sensor_data.linear_acceleration.z, 8)
            output += "Linear Acceleration: " + " X: " + x + " Y: " + y + " Z: " + z
        elif attributeToLog == "gravity":
            x = strSetLength(sensor_data.gravity_vector.x, 8)
            y = strSetLength(sensor_data.gravity_vector.y, 8)
            z = strSetLength(sensor_data.gravity_vector.z, 8)
            output += "Gravity Vector: " + " X: " + x + " Y: " + y + " Z: " + z
        
        print(output)
        

if __name__ == '__main__':
    # shortcut to not have to find out the port yourself
    serial_port = get_serial_ports()[2].device

    remote_id = 0x6817                    # remote device network ID
    remote = True                        # whether to use a remote device
    if not remote:
        remote_id = None

    index = 0
    
    oldTime = 0
    newTime = 0

    ip = "127.0.0.1"
    network_port = 8888 

    pozyx = PozyxSerial(serial_port)
    osc_udp_client = SimpleUDPClient(ip, network_port)
    o = Orientation3D(pozyx, osc_udp_client, remote_id)
    o.setup()

    attributeToLog = ""
    possibleAttributes = ["pressure", "acceleration", "magnetic", "angular velocity", "euler angles", "quaternion", "linear acceleration", "gravity"]
    while attributeToLog not in possibleAttributes: #check if input is correct
        attributeToLog = input("What do you want to log?\n(pressure, acceleration, magnetic, angular velocity, euler angles, quaternion, linear acceleration, or gravity)\n")

    start=t.time()
    try:
        while True:
            elapsed=(t.time()-start)                              #elapsed time since the program started
            oldTime = newTime                                     #oldTime is the time of previous cycle. It is set to newTime here since newTime has not been updated and still is the old cycle
            newTime = elapsed;                                    #newTime is the time of the current cycle.
            timeDifference = newTime - oldTime                    #timeDifference is the differece in time between each subsequent cycle

            o.loop(attributeToLog, elapsed, timeDifference)
            index += 1                                            #increment data index

    except KeyboardInterrupt:  #this allows Windows users to exit the while iterate_file by pressing ctrl+c
            pass
