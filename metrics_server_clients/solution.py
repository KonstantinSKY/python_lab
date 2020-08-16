# simple tcp client
import socket


class Client:

    def __init__(self, ip_addr, port, timeout=None):
        self.ip_addr = ip_addr
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((ip_addr, port))
        self.sock.settimeout(timeout)
        print(f'socket is ready: {self.sock}')

    def get(self, metric_name):
        print(f'this is GET, metric name {metric_name}')
        self.sock.sendall("ping".encode("utf8"))
        data = self.sock.recv(1024)
        print(f"Data got OK {data}")


    def put(self):
        print('This is PUT')

