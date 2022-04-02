#!./venv/bin/python3.8
import concurrent.futures
import argparse
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
import time

tcp_ans = []
mac_ip_cross = {}
ip_addr = ''
dst_port = int
ip_pool = []

def args():
    parser = argparse.ArgumentParser("""Scapy TCP scout.
    Scan pool of IP addresses and ports, return MACaddress , IP address , PORT with open TCP  .""")
    parser.add_argument("-ip", help="Pool of IP for scan.Example: 10.10.10.10/24")
    parser.add_argument("-p", help="Pool of PORT for scan.Example: 1-65535")
    return parser.parse_args()

def scaner(ip_address):
    scapy.conf.verb = 0
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=ip_address)
    package = ether / arp
    answer,unanswer = scapy.srp(package, timeout=2)
    scan_answer = [a[1] for a in answer]
    return scan_answer

def print_results(scan_result):

    for ans_package in scan_result:
        ip_host = ans_package['ARP'].psrc
        mac_host = ans_package['ARP'].hwsrc
        mac_ip_cross[ip_host]=mac_host
    return mac_ip_cross

def send_package(ip_addres,tcp):
    scapy.conf.verb = 0
    return scapy.sr1(ip_addres / tcp, timeout=0.0025 , retry=1)

def make_ip_pool(mac_ip_cross):
    for key in mac_ip_cross:
        ip_pool.append(key)
    return ip_pool

def make_port_pool():
    port_range = options.p.split('-')
    start_port_range = port_range[0]
    end_port_range = port_range[1]
    port_pool = list(range(int(start_port_range),int(end_port_range)))
    return port_pool

if __name__ == '__main__':
    t = time.time()
    options = args()
    scan_result = scaner(options.ip)
    mac_ip_cross = print_results(scan_result)
    ip_pool = make_ip_pool(mac_ip_cross)
    port_pool = make_port_pool()

    with concurrent.futures.ThreadPoolExecutor(max_workers=9) as executor:
        futures=[]
        for ip_addr in ip_pool:
            for dst_port in port_pool:
                futures.append(
                    executor.submit(
                        send_package,ip_addres = scapy.IP(dst=str(ip_addr)),tcp = scapy.TCP(sport=22,dport=dst_port)
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            if (str(type(future.result())) != "<class 'NoneType'>"):
                if future.result().getlayer(scapy.TCP).flags == 'SA':
                    tcp_ans.append(f"OPEN TCP IS FOUND : MAC = {mac_ip_cross[future.result()['IP'].src]} "
                                   f"IP =  {future.result()['IP'].src} PORT =  {future.result()['TCP'].sport}")

    for found_tcp in tcp_ans:
        print(found_tcp)
    print(f"time {time.time() - t}")