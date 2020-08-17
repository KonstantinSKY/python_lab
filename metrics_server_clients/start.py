from solution import Client

client = Client("127.0.0.1", 8888, timeout=15)

#client.put("palm.cpu", 0.5, timestamp=1150864247)
print(client.get("*"))
client.close()
