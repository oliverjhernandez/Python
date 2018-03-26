#!/usr/bin/env python

import os
import sys
import subprocess

time = "2016:02:31"
logfile = "/var/log/trafficserver/cwcats.log"

os.system("clear")

premin = []
totmin = []
bwidth = 0

cwcats = open(logfile).readlines()

for line in cwcats:
    if not time in line:
        continue
    try:
        ip = line.split(' ')[0]
        size = line.split(' ')[9]
        url = line.split(' ')[23]
        stream = url.split('/')[4]
        data = [ip, stream, size]
        premin.append(data)
    except IndexError:
        print

sessions = []

for log in premin:
    bwidth = bwidth + int(data[2])
    sessions.append([log[0],log[1]])

print "Minute: ", time
print "Total logs: ", len(premin)
print "Sessions: ", len(set(sessions))
print "Throughput: ", bwidth
