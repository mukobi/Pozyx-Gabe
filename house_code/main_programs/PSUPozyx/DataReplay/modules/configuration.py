from pypozyx import *
import os

MASTER_CONFIG_NAME = "MASTER_ACTIVE_CONFIG.properties"


class Configuration:

    @staticmethod
    def get_properties():
        configurations_file = os.path.dirname(os.path.dirname(__file__)) + "\\Configurations\\" + MASTER_CONFIG_NAME
        P = dict(line.strip().split('=') for line in open(configurations_file)
                 if not line.startswith('#') and not line.startswith('\n'))
        number_remote_devices = int(P["number_remotes"])

        remote_id = None
        tags = []
        if number_remote_devices == 0:
            use_remote = False
        else:
            use_remote = True
            remote_id = int(P["remote_1_id"], 16)
        if not use_remote:
            remote_id = None
            remote_1_id = int(P["remote_1_id"], 16)
            remote_2_id = int(P["remote_2_id"], 16)
            remote_3_id = int(P["remote_3_id"], 16)
            remote_4_id = int(P["remote_4_id"], 16)
            remote_5_id = int(P["remote_5_id"], 16)
            remote_6_id = int(P["remote_6_id"], 16)
            tags = [remote_1_id, remote_2_id, remote_3_id,
                    remote_4_id, remote_5_id, remote_6_id]

        number_anchors = int(P["number_anchors"])
        anchor_1_id = int(P["anchor_1_id"], 16)
        anchor_1_x = int(float(P["anchor_1_x"]) * 1000)
        anchor_1_y = int(float(P["anchor_1_y"]) * 1000)
        anchor_1_z = int(float(P["anchor_1_z"]) * 1000)
        anchor_2_id = int(P["anchor_2_id"], 16)
        anchor_2_x = int(float(P["anchor_2_x"]) * 1000)
        anchor_2_y = int(float(P["anchor_2_y"]) * 1000)
        anchor_2_z = int(float(P["anchor_2_z"]) * 1000)
        anchor_3_id = int(P["anchor_3_id"], 16)
        anchor_3_x = int(float(P["anchor_3_x"]) * 1000)
        anchor_3_y = int(float(P["anchor_3_y"]) * 1000)
        anchor_3_z = int(float(P["anchor_3_z"]) * 1000)
        anchor_4_id = int(P["anchor_4_id"], 16)
        anchor_4_x = int(float(P["anchor_4_x"]) * 1000)
        anchor_4_y = int(float(P["anchor_4_y"]) * 1000)
        anchor_4_z = int(float(P["anchor_4_z"]) * 1000)
        anchor_5_id = int(P["anchor_5_id"], 16)
        anchor_5_x = int(float(P["anchor_5_x"]) * 1000)
        anchor_5_y = int(float(P["anchor_5_y"]) * 1000)
        anchor_5_z = int(float(P["anchor_5_z"]) * 1000)
        anchor_6_id = int(P["anchor_6_id"], 16)
        anchor_6_x = int(float(P["anchor_6_x"]) * 1000)
        anchor_6_y = int(float(P["anchor_6_y"]) * 1000)
        anchor_6_z = int(float(P["anchor_6_z"]) * 1000)
        anchor_7_id = int(P["anchor_7_id"], 16)
        anchor_7_x = int(float(P["anchor_7_x"]) * 1000)
        anchor_7_y = int(float(P["anchor_7_y"]) * 1000)
        anchor_7_z = int(float(P["anchor_7_z"]) * 1000)
        anchor_8_id = int(P["anchor_8_id"], 16)
        anchor_8_x = int(float(P["anchor_8_x"]) * 1000)
        anchor_8_y = int(float(P["anchor_8_y"]) * 1000)
        anchor_8_z = int(float(P["anchor_8_z"]) * 1000)

        attributes_to_log = []
        if P["log_pressure"] == "true":
            attributes_to_log.append("pressure")
        if P["log_acceleration"] == "true":
            attributes_to_log.append("acceleration")
        if P["log_magnetic"] == "true":
            attributes_to_log.append("magnetic")
        if P["log_angular_velocity"] == "true":
            attributes_to_log.append("angular velocity")
        if P["log_euler_angles"] == "true":
            attributes_to_log.append("euler angles")
        if P["log_quaternion"] == "true":
            attributes_to_log.append("quaternion")
        if P["log_linear_acceleration"] == "true":
            attributes_to_log.append("linear acceleration")
        if P["log_gravity"] == "true":
            attributes_to_log.append("gravity")

        use_file = P["use_file"] == "true"
        filename = P["filename"]
        if not filename.endswith(".csv"):
            filename += ".csv"
        pozyx_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        data_file = pozyx_folder + "/Data/" + filename
        use_processing = P["use_processing"] == "true"
        anchors = [DeviceCoordinates(anchor_1_id, 1, Coordinates(anchor_1_x, anchor_1_y, anchor_1_z)),
                   DeviceCoordinates(anchor_2_id, 1, Coordinates(anchor_2_x, anchor_2_y, anchor_2_z)),
                   DeviceCoordinates(anchor_3_id, 1, Coordinates(anchor_3_x, anchor_3_y, anchor_3_z)),
                   DeviceCoordinates(anchor_4_id, 1, Coordinates(anchor_4_x, anchor_4_y, anchor_4_z)),
                   DeviceCoordinates(anchor_5_id, 1, Coordinates(anchor_5_x, anchor_5_y, anchor_5_z)),
                   DeviceCoordinates(anchor_6_id, 1, Coordinates(anchor_6_x, anchor_6_y, anchor_6_z)),
                   DeviceCoordinates(anchor_7_id, 1, Coordinates(anchor_7_x, anchor_7_y, anchor_7_z)),
                   DeviceCoordinates(anchor_8_id, 1, Coordinates(anchor_8_x, anchor_8_y, anchor_8_z))]
        anchors = anchors[0:number_anchors]

        return use_remote, remote_id, tags, anchors, attributes_to_log, use_file, data_file, use_processing

    @staticmethod
    def get_correct_serial_port():
        port = None
        try:
            port = get_serial_ports()[2].device
        except IndexError:
            try:
                port = get_serial_ports()[1].device
            except IndexError:
                try:
                    port = get_serial_ports()[0].device
                except IndexError:
                    pass
        return port
