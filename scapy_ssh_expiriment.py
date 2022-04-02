#!./venv/bin/python3.8
import scapy.all as scapy

ip_dst = "192.168.18.134"
src_port = 41851
dst_potr = 111
answer_split= []

ip_address = scapy.IP(dst=ip_dst)

tcp1 = scapy.TCP(sport=src_port,dport = dst_potr)
packege1 = ip_address / tcp1
ans1 = scapy.sr1(packege1)

tcp2 = scapy.TCP(sport=src_port,dport = dst_potr,flags = 'A',seq=1,ack=ans1.getlayer('TCP').seq+1)
packege2 = ip_address / tcp2
ans2 = scapy.sr1(packege2)

tcp3 = scapy.TCP(sport=src_port, dport=dst_potr, flags="FA", seq=1, ack=ans1.getlayer('TCP').seq + 1)
package3 =ip_address/tcp3
ans3 = scapy.sr1(package3)

tcp4 = scapy.TCP(sport=src_port, dport=dst_potr, flags="A", seq=ans3.getlayer('TCP').ack, ack=ans3.getlayer('TCP').seq + 1)
package4 =ip_address / tcp4
ans4 = scapy.sr1(package4)

try:
    answer_ssh_bytes = bytes(ans2.getlayer(scapy.Raw))
    answer_ssh = answer_ssh_bytes.decode('utf-8')
    answer_split = answer_ssh.split('-')
    if answer_split[0]=='SSH':
        print(f"On IP:POTR  {ip_dst}:{dst_potr} present SSH")
except:
    print("SSH not found")




