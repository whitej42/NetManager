## Basic python script for configuring a loopback interface and adding a message of the day banner

import getpass
import telnetlib

#Login manually
HOST = "192.168.122.89"
user = input("Enter your Login Credentials: ")
password = getpass.getpass()

#Login automatically
#HOST = "192.168.122.89"
#user = "james"
#password = "cisco"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password: #Remove for auto login
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco\n")
tn.write(b"conf t\n")
tn.write(b"int loop 0\n")
tn.write(b"ip address 1.1.1.1\n")
tn.write(b"router ospf 1\n")
tn.write(b"network 192.168.0.0 0.0.255.255 area 0\n")
tn.write(b"end\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))