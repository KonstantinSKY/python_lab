import asyncio

data_storage = {}


def _get(data):
    data = data[4:-1]
    resp_str = "ok\n"

    if data == "*":
        for key, metrics in data_storage.items():
            for metric in metrics:
                resp_str += f"{key} {metric[1]} {metric[0]}\n"
        resp_str += "\n"
        print(resp_str)
        return resp_str

    if data not in data_storage:
        resp_str += "\n"
        print(resp_str)
        return resp_str

    for metrics in data_storage[data]:
        resp_str += f"{data} {metrics[1]} {metrics[0]}\n"
    resp_str += "\n"
    print(resp_str)
    return resp_str


def _put(data):
    data_list = data[4:-1].split(" ")
    print(data_list)
    if len(data_list) != 3:
        print("Error len")
        return "error\nwrong command\n\n"
    try:
        metric = [
                int(data_list[2]),
                float(data_list[1])
            ]
    except Exception:
        print("Error metric")
        return "error\nwrong command\n\n"

    if data_list[0] in data_storage:
        data_storage[data_list[0]].append(metric)
    else:
        data_storage.update({data_list[0]: [metric]})
    print(data_storage)
    return "ok\n\n"


def process_data(data):
    data = str(data)
    if data.startswith("put ") and data.endswith("\n"):
        print("put")
        return _put(data)
    elif data.startswith("get ") and data.endswith("\n"):
        print("get")
        return _get(data)
    else:
        print("Wrong command err process data")
        return "error\nwrong command\n\n"


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        print(data)
        print(resp)
        self.transport.write(resp.encode())


loop = asyncio.get_event_loop()
print(loop)
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8888
)

server = loop.run_until_complete(coro)
print(server)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
