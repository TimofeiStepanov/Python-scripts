#!/usr/bin/python3

import re
import subprocess
import argparse
import sys

command = ''

def args():
     parser = argparse.ArgumentParser("""This script collect info about host:
               software,hardware and settings.""")

     parser.add_argument("--hard", help="All hardware info (-c,-d,-n,")
     parser.add_argument("-c",action='store_true',help="Not show CPU info 'lscpu'")
     parser.add_argument("-d",action='store_true',help="Not show Dicks info'blkid'")
     parser.add_argument("-n",action='store_true',help="Not show NET info 'ifconfig'")
     parser.add_argument("--soft",help="All software info (-o,-p,)")
     parser.add_argument("-o",action='store_true', help="Not show OS info 'uname -a'")
     parser.add_argument("-p",action='store_true', help="Not show System process info 'service --status-all")
     parser.add_argument("-u",action='store_true',help="Not show Users info 'cat /etc/passwd'")
     parser.add_argument("-s",action='store_true',help="Not show Package installed info 'dpkg -l'")
     parser.add_argument()
     parser.add_argument()
     parser.add_argument()
     return parser.parse_args()

func_dict = {}

def lscpu():
     path_tmp_file_lscpu= "/tmp/lscpu.txt"
     with open(path_tmp_file_lscpu,"w+") as file_lscpu:
          collect_lscpu = subprocess.check_output("lscpu")
          file_lscpu.write("CPU info:\n\r"+collect_lscpu.decode()+"\n++++++++++++++++++++++++++++\n")
     return path_tmp_file_lscpu
func_dict.update({lscpu(): args().c})

def uname():
     path_tmp_file_uname = "/tmp/uname.txt"
     with open(path_tmp_file_uname, "w+") as file_lscpu:
          collect_uname = subprocess.check_output(["uname","-a"])
          file_lscpu.write("OS info:\n\r"+collect_uname.decode()+"\n++++++++++++++++++++++++++++\n")
     return path_tmp_file_uname
func_dict.update({uname():args().o})


result_file = open("/tmp/collector_results.txt", "w+")

for key in func_dict:
     if func_dict.get(key) == False:
          with open(key,"r") as file:
               result_file.write(file.read())
     os.remove(key)

result_file.seek(0)
print(result_file.read())

os.remove("/tmp/collector_results.txt")