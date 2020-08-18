import asyncio


class ClientServerProtocol(asyncio.Protocol):
    pass

    def connection_made(self, transport):
        self.transport = transport
    #
    def data_received(self, data):
        # resp = process_data(data.decode())
        resp = data.decode()
        print(data)
        #self.transport.write(resp.encode())


loop = asyncio.get_event_loop()
print(loop)
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8888
)

print(coro)
print(dir(coro))
# print(coro.is_serving())
server = loop.run_until_complete(coro)
print(server)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
