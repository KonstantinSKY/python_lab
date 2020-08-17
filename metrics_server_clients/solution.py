# simple tcp client
import socket
import time


class ClientError(Exception):
    def __init__(self, msg, err=None):
        self.msg = msg
        self.err = err


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self.conn = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)

    def _read(self):
        data = b""

        while not data.endswith(b"\n\n"):
            try:
                data += self.conn.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)

        return data.decode('utf-8')

    def _send(self, data):
        try:
            self.conn.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to server", err)

    def get(self, metric_name):
        self._send(f"get {metric_name}\n".encode("utf8"))
        raw_data = self._read()
        data_list = raw_data.rsplit("\n")

        if data_list[0] != 'ok':
            raise ClientError('Server returns an error')
        del data_list[0]
        data_one = [data.split(" ") for data in data_list if data != '']
        data_res = {}
        try:
            for data in data_one:
                if data[0] not in data_res:
                    data_res[data[0]] = []
                data_res[data[0]].append((int(data[2]), float(data[1])))
        except Exception as err:
            raise ClientError('Server returned invalid data', err)
        [value.sort() for key, value in data_res.items()]

        return data_res

    def put(self, metric_name, value, timestamp=None):
        timestamp = timestamp or int(time.time())

        self._send(f"put {metric_name} {value} {timestamp}\n".encode("utf8"))
        raw_data = self._read()

        if raw_data == 'ok\n\n':
            return
        raise ClientError('Server returns an error')

    def close(self):
        try:
            self.conn.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)