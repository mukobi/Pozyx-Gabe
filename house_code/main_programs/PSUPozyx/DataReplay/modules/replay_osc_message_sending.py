from pythonosc.osc_message_builder import OscMessageBuilder

from constants import definitions


class ReplayOscMessageSending:
    @staticmethod
    def send_message(data_type, header_list, data_list, osc_udp_client):
        if data_type == definitions.DATA_TYPE_POSITIONING:
            ReplayOscMessageSending.send_single_position(
                header_list, data_list, osc_udp_client)
        elif data_type == definitions.DATA_TYPE_MULTIDEVICE_POSITIONING:
            ReplayOscMessageSending.send_multidevice_position(
                header_list, data_list, osc_udp_client)
        elif data_type == definitions.DATA_TYPE_MOTION_DATA:
            ReplayOscMessageSending.send_motion_data(
                header_list, data_list, osc_udp_client)

    @staticmethod
    def send_single_position(header_list, data_list, osc_udp_client):
        network_id = 0x6000
        if network_id is None:
            network_id = 0
        i_posx = header_list.index("Position-X")
        i_posy = header_list.index("Position-Y")
        i_posz = header_list.index("Position-Z")
        posx = data_list[i_posx]
        posy = data_list[i_posy]
        posz = data_list[i_posz]
        if osc_udp_client is not None:
            osc_udp_client.send_message(
                "/position", [network_id, int(posx), int(posy), int(posz)])

    @staticmethod
    def send_multidevice_position(header_list, data_list, osc_udp_client):
        for header in header_list:
            if header[:2] == "0x" and header[-2:] == "-X":
                tag = header[:6]
                network_id = int(tag, 16)
                if network_id is None:
                    network_id = 0
                i_posx = header_list.index(tag + "-X")
                i_posy = header_list.index(tag + "-Y")
                i_posz = header_list.index(tag + "-Z")
                posx = data_list[i_posx]
                posy = data_list[i_posy]
                posz = data_list[i_posz]
                if osc_udp_client is not None:
                    osc_udp_client.send_message(
                        "/position", [network_id, int(posx), int(posy), int(posz)])

    @staticmethod
    def send_motion_data(header_list, data_list, osc_udp_client):
        i_pressure = header_list.index("Pressure")
        i_acc_x = header_list.index("Acceleration-X")
        i_acc_y = header_list.index("Acceleration-Y")
        i_acc_z = header_list.index("Acceleration-Z")
        i_mag_x = header_list.index("Magnetic-X")
        i_mag_y = header_list.index("Magnetic-Y")
        i_mag_z = header_list.index("Magnetic-Z")
        i_ang_x = header_list.index("Angular-Vel-X")
        i_ang_y = header_list.index("Angular-Vel-Y")
        i_ang_z = header_list.index("Angular-Vel-Z")
        i_heading = header_list.index("Heading")
        i_roll = header_list.index("Roll")
        i_pitch = header_list.index("Pitch")
        i_quat_x = header_list.index("Quaternion-X")
        i_quat_y = header_list.index("Quaternion-Y")
        i_quat_z = header_list.index("Quaternion-Z")
        i_quat_w = header_list.index("Quaternion-W")
        i_lin_x = header_list.index("Linear-Acceleration-X")
        i_lin_y = header_list.index("Linear-Acceleration-Y")
        i_lin_z = header_list.index("Linear-Acceleration-Z")
        i_grav_x = header_list.index("Gravity-X")
        i_grav_y = header_list.index("Gravity-Y")
        i_grav_z = header_list.index("Gravity-Z")

        pressure = float(data_list[i_pressure])
        acc_x = float(data_list[i_acc_x])
        acc_y = float(data_list[i_acc_y])
        acc_z = float(data_list[i_acc_z])
        mag_x = float(data_list[i_mag_x])
        mag_y = float(data_list[i_mag_y])
        mag_z = float(data_list[i_mag_z])
        ang_x = float(data_list[i_ang_x])
        ang_y = float(data_list[i_ang_y])
        ang_z = float(data_list[i_ang_z])
        heading = float(data_list[i_heading])
        roll = float(data_list[i_roll])
        pitch = float(data_list[i_pitch])
        quat_x = float(data_list[i_quat_x])
        quat_y = float(data_list[i_quat_y])
        quat_z = float(data_list[i_quat_z])
        quat_w = float(data_list[i_quat_w])
        lin_x = float(data_list[i_lin_x])
        lin_y = float(data_list[i_lin_y])
        lin_z = float(data_list[i_lin_z])
        grav_x = float(data_list[i_grav_x])
        grav_y = float(data_list[i_grav_y])
        grav_z = float(data_list[i_grav_z])

        i_elapsed = header_list.index("Time")
        current_time = float(data_list[i_elapsed])

        calibration_status = [0xff]

        msg_builder = OscMessageBuilder("/sensordata")
        msg_builder.add_arg(int(1000 * current_time))

        msg_builder.add_arg(pressure)
        msg_builder.add_arg(acc_x)
        msg_builder.add_arg(acc_y)
        msg_builder.add_arg(acc_z)
        msg_builder.add_arg(mag_x)
        msg_builder.add_arg(mag_y)
        msg_builder.add_arg(mag_z)
        msg_builder.add_arg(ang_x)
        msg_builder.add_arg(ang_y)
        msg_builder.add_arg(ang_z)
        msg_builder.add_arg(heading)
        msg_builder.add_arg(roll)
        msg_builder.add_arg(pitch)
        msg_builder.add_arg(quat_w)
        msg_builder.add_arg(quat_x)
        msg_builder.add_arg(quat_y)
        msg_builder.add_arg(quat_z)
        msg_builder.add_arg(lin_x)
        msg_builder.add_arg(lin_y)
        msg_builder.add_arg(lin_z)
        msg_builder.add_arg(grav_x)
        msg_builder.add_arg(grav_y)
        msg_builder.add_arg(grav_z)

        msg_builder.add_arg(calibration_status[0] & 0x03)
        msg_builder.add_arg((calibration_status[0] & 0x0C) >> 2)
        msg_builder.add_arg((calibration_status[0] & 0x30) >> 4)
        msg_builder.add_arg((calibration_status[0] & 0xC0) >> 6)

        osc_udp_client.send(msg_builder.build())
