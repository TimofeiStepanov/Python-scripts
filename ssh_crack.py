#!./venv/bin/python3.8
import concurrent.futures
import argparse
import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
import time
import random
import os


tcp_ans = []
mac_ip_cross = {}
ip_addr = ''
dst_port = int
ip_pool = []
open_ips=[]
open_ports =[]
open_ip_port = []
open_ips_ports = []
d_port = int
s_port = int
ip_dst = ""
answer_split = []
sp_for_brute = []

def args():
    parser = argparse.ArgumentParser("""Scapy SSH scout.
    Scan pool of IP addresses and ports, return MACaddress , IP address , PORT with open ssh .""")
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

def tcp_open_ports_scan(port_pool,ip_pool):
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
                    open_ip = future.result()['IP'].src
                    open_port = future.result()['TCP'].sport
                    tcp_ans = str(f"{open_ip}:{open_port}")
                    open_ip_port = tcp_ans.split(':')
                    open_ips_ports.append(open_ip_port)
    return open_ips_ports

def find_ssh_ip_port_open(ip_dst,d_port):
    #ip_dst = ""
    #s_port = random.randrange(44444,55555,1)
    #d_port = int
    answer_split = []
    for_brute = ""
    s_port = 44547
    SYN = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=s_port, dport=d_port))
    ACK = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=s_port, dport=d_port, flags='A', seq=1, ack=SYN.getlayer('TCP').seq + 1))
    FIN = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=s_port, dport=d_port, flags="FA", seq=1, ack=SYN.getlayer('TCP').seq + 1))
    scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=s_port, dport=d_port, flags="A", seq=FIN.getlayer('TCP').ack, ack=FIN.getlayer('TCP').seq + 1))

    try:
        answer_ssh_bytes = bytes(ACK.getlayer(scapy.Raw))
        answer_ssh = answer_ssh_bytes.decode('utf-8')
        answer_split = answer_ssh.split('-')
        if answer_split[0] =='SSH':
            for_brute = str(f"{ip_dst}:{d_port}")
            print(f"On IP:PORT {for_brute} present SSH")
            sp_for_brute.append(for_brute)
    except:
        print("no")
    return sp_for_brute


if __name__ == '__main__':
    t = time.time()
    options = args()
    scan_result = scaner(options.ip)
    mac_ip_cross = print_results(scan_result)
    make_ip_pool(mac_ip_cross)
    port_pool = make_port_pool()
    open_ips_ports = tcp_open_ports_scan(port_pool,ip_pool)
    print(open_ips_ports)
    for ip_port in open_ips_ports:
        ip_dst = str(ip_port[0])
        d_port = int(ip_port[1])
        print(ip_dst)
        print(d_port)
        sp_for_brute = find_ssh_ip_port_open(ip_dst,d_port)






    print(f"time {time.time() - t}")