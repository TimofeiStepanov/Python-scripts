import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",4446))
server.listen(1)
print("waiting, for client...")
client, address = server.accept()  # здесь ждем подключения от клиента
print(f"accepted connection from {address}")
while True:
    print("waiting for data...")
    data = client.recv(1024)  # bytes!!!
    if not data:
        break
    print("received: ", data.decode())
    msg = f"Hello, I'm got it!!! OK {data.decode()}"
    # msg = b"Hello, I'm got it!!! OK"
    client.sendall(msg.encode())

server.close()

# asyncio
# select