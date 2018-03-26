#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear',shell=True)

# Ask for input
remoteServer = raw_input("Enter remote host IP to scan: ")


print "#" * 30
print "Please wait, scanning ", remoteServer
print "#" * 30

#Check start time
time1 = datetime.now()

try:
    for port in range(1,1025):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServer,port))
        if result == 0:
            print "Port {}:         Open".format(port)
        sock.close()

except KeyboardInterrupt:
    print "You pressed Ctrl+c."
    sys.exit()

except socket.error:
    print "Couldn't connect to server."
    sys.exit()

time2 = datetime.now()

total = time2 - time1

print "Scanning completed in: ", total
