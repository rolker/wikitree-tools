#!/usr/bin/env python

import sys

data = {}

class ProfileException(BaseException):
  def __init__(self):
    BaseException.__init__(self)

class Profile:
  def __init__(self,line):
    row = l.split('\t')
    if len(row) != 16:
      print row
      raise ProfileException()
    self.uid = int(row[0])
    self.wtid = row[1]
    self.father = int(row[13])
    self.mother = int(row[14])


def getLine(profile,line='paternal'):
  if line=='paternal':
    ancestor = profile.father
  else:
    ancestor = profile.mother
  if ancestor == 0:
    return [profile,]
  else:
    return [profile,] + getLine(data[ancestor],line)
  


for l in open(sys.argv[1], 'r'):
  try:
    p = Profile(l)
    data[p.uid] = p
  except (ValueError,ProfileException):
    pass

print len(data),'records'

print getLine(data[32])
