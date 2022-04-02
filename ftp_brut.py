import ftplib
import os


def password():
    passes_ftp = []
    with open("passwords.txt","r") as pass_ftp:
        passwd_ftp = pass_ftp.readline()
    return passwd_ftp


