#!/usr/bin/env python

import sys
import csv
import gzip

csv.field_size_limit(2000000)

acadians = []

cat_fname = 'data/dump_categories.csv.gz'
users_fname = 'data/dump_people_user.csv.gz'

cat_file = gzip.open(cat_fname,'r')

reader = csv.reader(cat_file,delimiter='\t')
for row in reader:
    #print row
    if row[1] == 'Acadians':
        acadians.append(row[0])
        print row

data = {}

missing_profiles = []
extra_tabs = []

class ProfileException(BaseException):
  def __init__(self):
    BaseException.__init__(self)

def Profile2Tuple(row):
    uid = int(row[0])
    wtid = row[1]
    if row[-3] in ('','0'):
      father = None
    else:
      father = int(row[-3])
    if row[-2] in ('','0'):
      mother = None
    else:
      mother = int(row[-2])
    return (uid,wtid,father,mother)


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
  
header = None

users_file = gzip.open(users_fname,'r')
reader = csv.reader(users_file,delimiter='\t')

lcount = 0
for row in reader:
  if header is None:
    header = row
  else:
    if len(row) > 16:
      extra_tabs.append(row[0])
    try:
      #p = Profile(row)
      p = Profile2Tuple(row)
      data[p[0]] = p
      lcount += 1
      if lcount%1000 == 0:
        print lcount
      if lcount > 20000000:
        break
    except (ValueError,ProfileException,IndexError):
      c = min(len(header),len(row))
      for i in range(c):
        print '\t',header[i]+':'+row[i]
      if len(row) > c:
        print row[c:]
 
print len(data),'records'

print len(extra_tabs),'profiles with extra tabs',extra_tabs[:10],'...'


#uids = data.keys()
#uids.sort()

