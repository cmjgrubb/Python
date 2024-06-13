# CMJ Grubb
# 06/13/2024
# This script prompts a user for a password and returns an encrypted password and key.

from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
password = input("Enter the password you would like to encrypt: ")
pass_bin = password.encode()
enc_pass = cipher_suite.encrypt(pass_bin)

print("Encrypted password:", enc_pass)
print("Key:", key)
