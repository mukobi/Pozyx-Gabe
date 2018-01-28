from pypozyx import *

MASTER_PROPS_LOCATION = "../../original_programs/PSUPozyx/Configuration/MASTER_ACTIVE_CONFIG.properties"


class PropertyReading:

    @staticmethod
    def getProperties():
        P = dict(line.strip().split('=') for line in open(MASTER_PROPS_LOCATION)
                 if not line.startswith('#') and not line.startswith('\n'))
        use_remote = P["use_remote"] == "true"
        remote_id = int(P["remote_id"], 16)
        anchor_1_id = int(P["anchor_1_id"], 16)
        anchor_1_x = int(P["anchor_1_x"], 16)
        anchor_1_y = int(P["anchor_1_y"], 16)
        anchor_1_z = int(P["anchor_1_z"], 16)
        anchor_2_id = int(P["anchor_2_id"], 16)
        anchor_2_x = int(P["anchor_2_x"], 16)
        anchor_2_y = int(P["anchor_2_y"], 16)
        anchor_2_z = int(P["anchor_2_z"], 16)
        anchor_3_id = int(P["anchor_3_id"], 16)
        anchor_3_x = int(P["anchor_3_x"], 16)
        anchor_3_y = int(P["anchor_3_y"], 16)
        anchor_3_z = int(P["anchor_3_z"], 16)
        anchor_4_id = int(P["anchor_4_id"], 16)
        anchor_4_x = int(P["anchor_4_x"], 16)
        anchor_4_y = int(P["anchor_4_y"], 16)
        anchor_4_z = int(P["anchor_4_z"], 16)

        attributes_to_log = []
        if P["log_pressure"] == "true": attributes_to_log += "pressure"
        if P["log_acceleration"] == "true": attributes_to_log += "acceleration"
        if P["log_magnetic"] == "true": attributes_to_log += "magnetic"
        if P["log_angular_velocity"] == "true": attributes_to_log += "angular velocity"
        if P["log_euler_angles"] == "true": attributes_to_log += "euler angles"
        if P["log_quaternion"] == "true": attributes_to_log += "quaternion"
        if P["log_linear_acceleration"] == "true": attributes_to_log += "linear acceleration"
        if P["log_gravity"] == "true": attributes_to_log += "gravity"

        use_file = P["use_file"] == "true"
        filename = P["filename"]
        use_processing = P["use_processing"] == "true"
        anchors = [DeviceCoordinates(anchor_1_id, 1, Coordinates(anchor_1_x, anchor_1_y, anchor_1_z)),
                   DeviceCoordinates(anchor_2_id, 1, Coordinates(anchor_2_x, anchor_2_y, anchor_2_z)),
                   DeviceCoordinates(anchor_3_id, 1, Coordinates(anchor_3_x, anchor_3_y, anchor_3_z)),
                   DeviceCoordinates(anchor_4_id, 1, Coordinates(anchor_4_x, anchor_4_y, anchor_4_z)),]

        return use_remote, remote_id, anchors, attributes_to_log, use_file, filename, use_processing
