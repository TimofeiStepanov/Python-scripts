#!/usr/bin/python3
import re
import subprocess
import argparse


#args = sys.argv
#print(args)

def args():
    parser = argparse.ArgumentParser("this is my script to change mac")
    parser.add_argument("-m","--mac",help="mac address to change to")
    parser.add_argument("-i","--interface",help="interface to change mac to")
    return parser.parse_args()

if __name__=='__main__':
    res = subprocess.check_output(f"ifconfig",shell=1)
    res = res.decode()
    print(res.split(": flags"),sep="\n")
    interfaces = re.findall(r"(.+): flags", res)
    options = args()
    if options.interface not in interfaces:
        print("Error wrong interface: ")
        print(f"interface must be one of {interfaces}...")
        exit(0)
    print(f"trying to change mac on interface {options.interface}...")
    interface = options.interface
    mac = options.mac
    print(res)
#    options = args()
#    print(options.mac)
#    print(options.interface)


#interface="eth0"
#mac="f0:fa:ab:12:3d:11"

    res = subprocess.check_output(f"ifconfig {interface} down",shell=1)
    print("down result: ",res.decode())
    res = subprocess.check_output(f"ifconfig {interface} hw ether {mac}",shell=1)
    print("change mac result: ",res.decode())
    res = subprocess.check_output(f"ifconfig {interface} up",shell=1)
    print("up result: ",res.decode())
    res = subprocess.check_output(f"ifconfig", shell=1)
    if mac in res.decode():
        print("interface mac changed")
    else:
        print("something goes wrong...")