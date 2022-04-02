#!./venv/bin/python3.8
import scapy.all as scapy
import socket

ip_dst = "192.168.18.134"
src_port = 41871
dst_port = 22

packets = scapy.sniff(count=10,filter='tcp')
sck = socket.socket()
conn = sck.connect((ip_dst,dst_port))
stream_sck = scapy.StreamSocket(sck)

sck.close()