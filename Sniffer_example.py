import scapy.all as scapy
from scapy.layers.l2 import ARP, Ether
from scapy.layers.http import HTTPRequest, Raw
import argparse
import time


def packet_analyze(p: scapy.Packet):

    if p.haslayer(HTTPRequest):
        print("*" * 150)
        if p.haslayer(Raw):
            print(p[Raw].load)
            print("-" * 150)




def sniff_packets():
    scapy.sniff(
        prn=packet_analyze
    )

if name == 'main':
    sniff_packets()