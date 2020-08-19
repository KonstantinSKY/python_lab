import asyncio

data_storage = {}
error_string = "error\nwrong command\n\n"


def run_server(host, port):
    loop = asyncio.get_event_loop()

    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


def _get(data):
    data = data[4:-1]
    resp_str = "ok\n"

    if " " in data:
        return error_string

    if data == "*":
        for key, metrics in data_storage.items():
            for ts, metric in metrics.items():
                resp_str += f"{key} {metric} {ts}\n"
        resp_str += "\n"
        return resp_str

    if data not in data_storage:
        resp_str += "\n"
        return resp_str

    for ts, metric in data_storage[data].items():
        resp_str += f"{data} {metric} {ts}\n"

    resp_str += "\n"

    return resp_str


def _put(data):
    data_list = data[4:-1].split(" ")
    if len(data_list) != 3:
        return error_string
    try:
        metric = {int(data_list[2]): float(data_list[1])}

    except Exception:
        return error_string

    if data_list[0] in data_storage:
        data_storage[data_list[0]].update(metric)
    else:
        data_storage.update({data_list[0]: metric})
    return "ok\n\n"


def process_data(data):
    data = str(data)
    if data.startswith("put ") and data.endswith("\n"):
        return _put(data)
    elif data.startswith("get ") and data.endswith("\n"):
        return _get(data)
    else:
        return "error\nwrong command\n\n"


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        pass

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())

        self.transport.write(resp.encode())
