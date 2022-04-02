#!/usr/bin/env python3
import ftplib
import argparse
import getpass

help = """1. enter command with args (default)
2. upload file to server
3. download file from server"""


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
    parser = argparse.ArgumentParser("ftp client")
    parser.add_argument("-u", "--user", help="user name (login)")
    parser.add_argument("--ip", help="ftp server ip", required=True)
    parser.add_argument("-p", "--port", help="port", default=21, type=int)
    parser.add_argument("-t", "--timeout", help="timeout to wait server", default=5, type=int)
    return parser.parse_args()


def connect(user, psw, host, port, timeout):
    try:
        server.connect(host, port, timeout=timeout)
        server.login(user, psw)
    except Exception as e:
        cprint("error:", e, color="r")
        return False
    cprint(f"connected, OK: {user},{'*' * len(psw)}", color="g")
    return True


if __name__ == '__main__':
    options = args()
    if not options.user:
        options.user = input("username:")
    print("enter password")
    password = getpass.getpass()
    server = ftplib.FTP()
    # server.set_debuglevel(1)
    if not connect(options.user, password, options.ip, options.port, options.timeout):
        print("Error on connect")
        exit(0)
    # cprint("=" * 60, color="y")
    cprint("=" * 60, "DIR", "=" * 60, color="g")
    server.dir()
    while server:
        try:
            print(help)

            cmd = input("command >>")
            if cmd == "2":
                path = input("\tinput file name to upload:")
                code = server.storbinary("STOR " + path, open(path, 'rb'), 1024)
                cprint("done, answer is " + code, color="g")
                continue
            elif cmd == "3":
                filename = input("\tinput file name to download:")
                with open(filename, 'wb') as file:
                    code = server.retrbinary("RETR " + filename, file.write)
                    cprint("done, answer is " + code, color="g")
                    continue

            cargs = input("\t\t args via space:").split(" ")
            print(getattr(server, cmd)(*cargs))
        except Exception as e:
            cprint(e, color="r")
