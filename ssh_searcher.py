import argparse
import scapy
import threading


def args():
    parser = argparse.ArgumentParser("""This script scan IP in pool for search SSH open ports and then bruteforce it.""")
    parser.add_argument("-i",  help="Input IP pool . Example: 192.168.10.0/24 ")
    parser.add_argument("-u", help="Path to users wordlist.")
    parser.add_argument("-p", help="Path to passwords wordlist.")
    return parser.parse_args()



