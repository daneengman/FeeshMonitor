# echo-client.py
# https://realpython.com/python-sockets/

import socket

HOST = "127.0.0.1"
PORT = 15213

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with open("logs/2023-01-16.csv", "rb") as file:
        s.connect((HOST, PORT))
        data = file.read(1024)
        while(data):
            s.send(data)
            data = file.read(1024)

print(f"Sent data :(")