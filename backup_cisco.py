# Author: CMJ Grubb
# 06/13/2024
# Must run on Windows - probably not hard to adapt to *nix
# This file reads a list of IP addresses from device_list.txt in the same subdirectory, iterates through them,
# and backs up the configs in a subdirectory Backups. Be sure that the credentials provided dump you straight
# into privileged mode on the Cisco device.

import paramiko
import datetime
import logging
import ctypes
from cryptography.fernet import Fernet
import os

encrypted_password = b'...'
key = b'...'

password = Fernet(key).decrypt(encrypted_password).decode()

logging.basicConfig(filename='backup_log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

current_time = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
devices_file = "device_list.txt"

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(current_dir, "Backups")
except Exception as e:
    logging.error(f"Failed to get current directory: {e}")
    ctypes.windll.user32.MessageBoxW(0, "Failed to get current directory. Check logs for details.", "Script Error", 0x10)

try:
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
except Exception as e:
    logging.error(f"Failed to create backup directory: {e}")
    ctypes.windll.user32.MessageBoxW(0, "Failed to create backup directory. Check logs for details.", "Script Error", 0x10)

try:
    with open(devices_file, "r") as input_file:
        ip_list = input_file.readlines()

    for ip in ip_list:
        ip_addr = ip.strip()
        try:
            ssh.connect(hostname=ip_addr, username='administrator', password=password, port=22)
            stdin, stdout, stderr = ssh.exec_command('show run')
            output = stdout.readlines()

            backup_file = os.path.join(backup_dir, f"{ip_addr}_{current_time}.txt")
            print(os.path.join(backup_dir, f"{ip_addr}_{current_time}.txt"))

            with open(backup_file, "w") as outfile:
                for line in output:
                    outfile.write(line)
            ctypes.windll.user32.MessageBoxW(0, f"Backup for {ip_addr} completed successfully.", "Backup Successful", 0)
        except paramiko.SSHException as e:
            logging.error(f"SSH connection failed for {ip_addr}: {e}")
            ctypes.windll.user32.MessageBoxW(0, f"SSH connection failed for {ip_addr}. Check logs for details.", "Backup Failed", 0x10)
        finally:
            ssh.close()
except Exception as e:
    logging.error(f"Failed to process device list: {e}")
    ctypes.windll.user32.MessageBoxW(0, "Failed to process device list. Check logs for details.", "Script Error", 0x10)
finally:
    if 'outfile' in locals() and not outfile.closed:
        outfile.close()
