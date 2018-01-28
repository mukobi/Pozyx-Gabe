import socket
import struct
import time
import msgpack

HOST_IP = '0.0.0.0'  # all interfaces
SENDER_PORT = 2000
# 224.0.1.0 thru 224.255.255.255
# (ping 224.0.0.1 for the group mulitcast server list)
MCAST_ADDR = '224.13.39.71'
MCAST_PORT = 4000
TTL = struct.pack('b', 1)  # valid value are 1-255, <32 is local network


class Producer:
    def __init__(self, sender_ip=HOST_IP, sender_port=SENDER_PORT, ttl=TTL):
        try:
            self.sock = socket.socket(socket.AF_INET,
                                      socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.bind((sender_ip, sender_port))
            self.sock.setsockopt(socket.IPPROTO_IP,
                                 socket.IP_MULTICAST_TTL, ttl)
        except socket.error as e:
            if socket.error == 10048:
                self.__init__(sender_ip, sender_port + 1, ttl)

    def send(self, msg="", mcast_addr=MCAST_ADDR, mcast_port=MCAST_PORT, ):
        packed_message = msgpack.packb(msg)
        self.sock.sendto(packed_message, (mcast_addr, mcast_port))

    def close_socket(self):
        self.sock.close()

    @staticmethod
    def host_name():
        return socket.gethostname()


class Consumer:
    def __init__(self, client_ip=HOST_IP, mcast_addr=MCAST_ADDR,
                 mcast_port=MCAST_PORT, ttl=TTL, blocking=0):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((client_ip, mcast_port))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(mcast_addr) + socket.inet_aton(client_ip))
        self.sock.setblocking(blocking)

    def close_socket(self):
        self.sock.close()

    def receive(self, size=1024):
        try:
            packed_data, addr = self.sock.recvfrom(size)
            data = msgpack.unpackb(packed_data)
            return addr, data
        except socket.error as e:
            return None

    @staticmethod
    def host_name():
        return socket.gethostname()