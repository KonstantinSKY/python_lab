# asyncio, tcp клиент

import asyncio


async def tcp_echo_client(msg, loop):
    reader, writer = await asyncio.open_connection("127.0.0.1", 10001, loop=loop)

    print("send: %r" % msg)
    writer.write(msg.encode())
    writer.close()

loop = asyncio.get_event_loop()
msg = "Test word"
loop.run_until_complete(tcp_echo_client(msg, loop))
loop.close()
