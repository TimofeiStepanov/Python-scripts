#!./venv/bin/python3.8
import socket

import scapy.all as scapy

sck = scapy.L3RawSocket()

ip_dst = "192.168.18.134"
src_port = 41871
dst_port = 22
answer_split = []



SYN = sck.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=src_port, dport = dst_port,flags='S'))
ACK = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=src_port, dport = dst_port, flags ='A', seq=SYN.getlayer('TCP').ack, ack=SYN.getlayer('TCP').seq + 1))
FIN = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=src_port, dport=dst_port, flags="FA", seq=SYN.getlayer('TCP').ack, ack=SYN.getlayer('TCP').seq + 1))
ACK_end = scapy.sr1(scapy.IP(dst=ip_dst) / scapy.TCP(sport=src_port, dport=dst_port, flags="A", seq=FIN.getlayer('TCP').ack, ack=FIN.getlayer('TCP').seq + 1))
print(ACK)
try:
    answer_ssh_bytes = bytes(ACK.getlayer(scapy.Raw))
    answer_ssh = answer_ssh_bytes.decode('utf-8')
    answer_split = answer_ssh.split('-')
    if answer_split[0]=='SSH':
        print(f"On IP:PORT  {ip_dst}:{dst_port} present SSH")
except:
    print("SSH not found")