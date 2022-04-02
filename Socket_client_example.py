import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("127.0.0.1", 4446))
    print("connected to server...")
    while True:
        data = input(">>").encode()
        client.sendall(data)
        answer = client.recv(1024)
        print(f"server sent data:{answer.decode()}")

except Exception as e:
    print(e)
finally:
    client.close()
