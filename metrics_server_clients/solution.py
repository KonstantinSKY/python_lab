# simple tcp client
import socket
import time


class ClientError(Exception):
    def __init__(self):
        super().__init__()


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
        try:
            self.sock.sendall(f"get {metric_name}\n".encode("utf8"))
            data = self.sock.recv(1024).decode()
        except ClientError:
            raise ClientError()
        data_list = data.rsplit("\n")

        if data_list[0] == 'error':
            raise ClientError()
        print(f"Data got OK {data}")
        print(f"Data_list OK {data_list[0]}")
        del data_list[0]
        print(f"Data_list {data_list}")
        data_one = [data.split(" ") for data in data_list if data != '']
        res = {}
        try:
            for data in data_one:
                if data[0] not in res:
                    res[data[0]] = []
                res[data[0]].append((int(data[2]), float(data[1])))
        except Exception:
            raise ClientError()
        [value.sort() for key, value in res.items()]
        print(res)
        return res

    def put(self, metric_name, value, timestamp=None):
        print(f'This is PUT metric = {metric_name}, value = {value}, ts = {timestamp}')
        if timestamp is None:
            timestamp = time.time()
        else:
            try:
                timestamp = int(timestamp)
            except Exception:
                pass
        try:
            self.sock.sendall(f"put {metric_name} {value} {timestamp}\n".encode("utf8"))
            data = self.sock.recv(1024).decode()
        except ClientError():
            raise ClientError

        data_list = data.rsplit("\n")
        if data_list[0] == 'error':
            raise ClientError()

        print(f"Put response: {data}")
