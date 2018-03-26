#!/usr/local/bin/python

#import fileinput
import os
import re

dist = open('dist', 'r')
remap = open('remap.config_PANAMA', 'r+w')
output = open('file', 'w')

distlines = dist.readlines()
remaplines = remap.readlines()

for line in distlines:
  pool = line.rstrip("\n\r").split(" ")
  for k, li in enumerate(remaplines):
    if pool[0] in li:
      remaplines[k] = re.sub(r"http:\/\/172\.26\.113\.[0-9][0-9]", "http://" + pool[1], li).rstrip("\r\n")

output.write("\n".join(remaplines))

dist.close()
remap.close()
