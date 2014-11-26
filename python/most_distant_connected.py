#!/usr/bin/env python

import sys

data = {}

missing_profiles = []

class ProfileException(BaseException):
  def __init__(self):
    BaseException.__init__(self)

class Profile:
  def __init__(self,row):
    self.uid = int(row[0])
    self.wtid = row[1]
    self.name = row[3]+' '+row[5]
    if row[-3] in ('','0'):
      self.father = None
    else:
      self.father = int(row[-3])
    if row[-2] in ('','0'):
      self.mother = None
    else:
      self.mother = int(row[-2])
      
  def __repr__(self):
    return str(self.__dict__)

def getLine(profile,line='paternal'):
  if line=='paternal':
    ancestor = profile.father
  else:
    ancestor = profile.mother
  if ancestor is None:
    return [profile,]
  else:
    try:
      ap = data[ancestor]
    except KeyError:
      if not ancestor in missing_profiles:
        missing_profiles.append(ancestor)
      return [profile,]
    return [profile,] + getLine(data[ancestor],line)
  
header = None

for line in open(sys.argv[1], 'r'):
  row = line.split('\t')
  if header is None:
    header = row
  try:
    p = Profile(row)
    data[p.uid] = p
  except (ValueError,ProfileException,IndexError):
    c = min(len(header),len(row))
    for i in range(c):
      print '\t',header[i]+':'+row[i]
    if len(row) > c:
      print row[c:]
 
print len(data),'records'

uids = data.keys()
uids.sort()

recursives = []
maxGens = 0
candidate_lines = []

for uid in uids:
  try:
    line = getLine(data[uid])
  except RuntimeError:
    recursives.append(data[uid])
  maxGens = max(maxGens,len(line))
  if len(line) > 15:
    candidate_lines.append(line)
#    print data[uid].name
#    for p in line:
#      print '\t',p.wtid,p.name

#for r in recursives:
#  print 'error:',r
  
print 'max gens:', maxGens

print len(recursives),'profiles with recursion errors'

print len(missing_profiles),'missing profiles',missing_profiles[:10],'...' 
print len(candidate_lines), 'candidate lines'
