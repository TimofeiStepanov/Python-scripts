#!/usr/bin/env python3
import socket
import argparse
import os

GREEN = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[91m'
ENDC = '\033[0m'

CLOSE_CONNECTION = "close"
TRANSFER = "transfer"
FILE_NOT_FOUND = "file not found789"
TRANSFER_COMPLETE = "transfer completed456"
SEP = "*"


def args():
    parser = argparse.ArgumentParser("ups server on port")
    parser.add_argument("-p", "--port", default=8080, type=int, help="port of server")
    parser.add_argument("-ip", default='', help="ip, default is ''")
    return parser.parse_args()


def print_error(s, **kwargs):
    print(f"{ERROR}{s}{ENDC}", **kwargs)


def print_ok(s, **kwargs):
    print(f"{GREEN}{s}{ENDC}", **kwargs)


def print_warn(s, **kwargs):
    print(f"{WARNING}{s}{ENDC}", **kwargs)


def transfer_data(connection: socket.socket, command: str):
    if SEP not in command:
        print_error(f"add separator '{SEP}' before path")
        return
    name = command.split(SEP) # []
    if len(name) != 2:
        print_error(f"wrong transfer command")
        return
    name = os.path.basename(name[1]) + "_loaded"  # transfer*file.txt
    # file.txt_loaded
    connection.send(command.encode())

    file = open(name, "wb")
    while True:
        data = connection.recv(1024)
        print_warn(f"\t\treceived data: {data}")
        if FILE_NOT_FOUND.encode() in data:
            print_error("\t\tUnable to find the file")
            file.close()
            break
        if TRANSFER_COMPLETE.encode() in data:
            print_ok("\t\tTransfer completed")
            file.close()
            break
        file.write(data)


def connect(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print_ok(f"\t\tlisten for incoming TCP on port {port}...")
    connection, address = server.accept()
    print_ok(f"\t\treceived connection from: {address}")
    while True:
        command = input(">>").strip()
        if CLOSE_CONNECTION in command:  # terminate connection
            connection.send(CLOSE_CONNECTION.encode())
            connection.close()
            break
        elif TRANSFER in command:  # transfer files
            transfer_data(connection, command)
        else:
            print_warn(f"\t\tsend command:{command}")
            connection.send(command.encode())  # simple command
            print(connection.recv(1024).decode())


if __name__ == "__main__":
    option = args()
    while 1:
        try:
            connect(option.ip, option.port)
        except Exception as e:
            print_error(f"error: {e}")
            continue
