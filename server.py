# echo-server.py
# https://realpython.com/python-sockets/

import socket
import os
import datetime

HOST = "127.0.0.1" # local host
PORT = 15213 # sure whatever
 
# add threads? idk
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                with create_file() as file:
                    data = 1
                    while data:
                        data = conn.recv(1024)
                        file.write(data)
                print("finished receiving data :0")

def create_file():
    if not os.path.exists("server-received"):
            os.mkdir("server-received")
    return open(f"server-received/{datetime.datetime.now()}.csv", "wb")

if __name__ == "__main__":
    main()