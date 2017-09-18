#!/usr/bin/env python

import sys

header = None

for line in open(sys.argv[1], 'r'):
  row = line.strip('\n').split('\t')
  if header is None:
    header = row
  else:
    if len(row) != 16:
      out = []
      for i in range(len(row)):
        if i < len(header):
          out.append(header[i]+':'+row[i])
        else:
          out.append(':'+row[i])
          
      print '*'.join(out)
