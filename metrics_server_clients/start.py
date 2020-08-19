from client import Client

client = Client("127.0.0.1", 8888, timeout=15)

client.put("palm.cpu", 0.5, timestamp=1150864247)
client.put("palm.cpu1", 0.4, timestamp=1150964247)
client.put("palm.cpu3", 3.5, timestamp=1150264247)
client.put("palm.cpu", 0.34, timestamp=1150864248)
client.put("palm.cpu", 0.54, timestamp=1140864247)
client.put("palm.cpu", 0.12154, timestamp=1140864247)
print(client.get("*"))
print(client.get("palm.cpu"))
print(client.get("palmas.cpu"))

client.close()

