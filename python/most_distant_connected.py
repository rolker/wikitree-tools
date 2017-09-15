#!/usr/bin/env python

import sys

data = {}

missing_profiles = []
extra_tabs = []

class ProfileException(BaseException):
  def __init__(self):
    BaseException.__init__(self)

class Profile:
  def __init__(self,row):
    self.uid = int(row[0])
    self.wtid = row[1]
    self.gender = row[2]
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

lcount = 0
for line in open(sys.argv[1], 'r'):
  row = line.split('\t')
  if header is None:
    header = row
  else:
    if len(row) > 16:
      extra_tabs.append(row[0])
    try:
      p = Profile(row)
      data[p.uid] = p
      lcount += 1
      if lcount > 40000000:
        break
    except (ValueError,ProfileException,IndexError):
      c = min(len(header),len(row))
      for i in range(c):
        print '\t',header[i]+':'+row[i]
      if len(row) > c:
        print row[c:]
 
print len(data),'records'

print len(extra_tabs),'profiles with extra tabs',extra_tabs[:10],'...'


uids = data.keys()
uids.sort()

for atype in ('paternal','maternal'):
  print atype
  
  recursives = []
  maxGens = 0
  candidate_lines = []
  
  for uid in uids:
    if data[uid].gender == '':
      try:
        line = getLine(data[uid],atype)
      except RuntimeError:
        recursives.append(data[uid])
      maxGens = max(maxGens,len(line))
      if len(line) > 10:
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
  
  steps = {}
  
  for i in range(len(candidate_lines)):
    l1 = candidate_lines[i]
    for j in range(i,len(candidate_lines)):
      l2 = candidate_lines[j]
      if l2[0] not in l1 and l1[-1] == l2[-1]:
        last = 1
        minlen = min(len(l1),len(l2))
        try:
          while l1[-last] == l2[-last] and last < minlen:
            last += 1
          s = len(l1)-last+len(l2)-last
          if s > 5:
            if not s in steps:
              steps[s]=[]
            steps[s].append((l1,l2)) 
        except IndexError:
          print l1
          print l2
          sys.exit(1)
        
  skeys = steps.keys()
  skeys.sort()
  
  print
  
  for i in range(1,11):
    s = skeys[-i]
    print s
    for l1,l2 in steps[skeys[-i]]:
      last = 1
      minlen = min(len(l1),len(l2))
      while l1[-last] == l2[-last] and last < minlen:
        last += 1
      print '\t',l1[0].wtid,l1[0].name,'\t',l2[0].wtid,l2[0].name,'\tcommon:',l1[-last+1].wtid,l1[-last+1].name
  
  
