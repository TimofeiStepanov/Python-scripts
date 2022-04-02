#!./venv/bin/python3.8
import argparse
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP


mac_ip_cross={}

def args():
    parser = argparse.ArgumentParser("""Scapy ARP scaner.
    Scan pool of IP adresses , create dict {mac:ip}.""")
    parser.add_argument("-p", help="Pool of IP for scan.Example: 10.10.10.10/24")
    return parser.parse_args()

def scaner(ip_address):
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ip_address)
    package = ether / arp
    answer, unanswer = scapy.srp(package, timeout=2)
    scan_answer = [t[1] for t in answer]
    return scan_answer

def print_results(scan_result):
    for ans_package in scan_result:
        ip_host = ans_package['ARP'].psrc
        mac_host = ans_package['ARP'].hwsrc
        mac_ip_cross[mac_host]=ip_host
    return mac_ip_cross

if __name__ == '__main__':
    options = args()
    scan_result = scaner(options.p)
    print_results(scan_result)
    print(print_results(scan_result))