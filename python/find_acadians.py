#!/usr/bin/env python

import sys
import csv
import gzip

csv.field_size_limit(3000000)

acadians = []

root_profile = 'Arsenault-64'
rootid = None


cat_fname = 'data/dump_categories.csv.gz'
#users_fname = 'data/dump_people_user.csv.gz'
users_fname = 'data/dump_people_user.csv'

cat_file = gzip.open(cat_fname,'r')

reader = csv.reader(cat_file,delimiter='\t')
for row in reader:
    #print row
    if row[1] == 'Acadians':
        acadians.append(int(row[0]))
        
print len(acadians),'acadians'

data = {}

def Profile2Tuple(row):
    uid = int(row[0])
    wtid = row[1]
    if row[14] in ('','0'):
      father = None
    else:
      father = int(row[14])
    if row[15] in ('','0'):
      mother = None
    else:
      mother = int(row[15])
    return (uid,wtid,father,mother)

header = None

#users_file = gzip.open(users_fname,'r')
users_file = open(users_fname,'r')
reader = csv.reader(users_file,delimiter='\t')

lcount = 0
for row in reader:
    if header is None:
        header = row
    else:
        try:
            p = Profile2Tuple(row)
            if p[1] == root_profile:
                rootid = p[0]
            #print p
            data[p[0]] = p
            lcount += 1
            if lcount%100000 == 0:
                print lcount
            if lcount > 20000000:
                break
        except (ValueError, IndexError) as e:
            print header
            print row
            break
 
print len(data),'records'

print root_profile,rootid, rootid in acadians

seen_profiles = []
unseen_profiles = [rootid,]

out = open('out.html','w')
out.write('<html><body>\n')

while len(unseen_profiles):
    try:
        p = data[unseen_profiles[0]]
        if p[2] is not None:
            if not p[2] in seen_profiles:
                unseen_profiles.append(p[2])
        if p[3] is not None:
            if not p[3] in seen_profiles:
                unseen_profiles.append(p[3])
        seen_profiles.append(p[0])
        print p,p[0] in acadians
        if not p[0] in acadians:
            out.write('<p><a href="https://wikitree.com/wiki/'+p[1]+'">'+p[1]+'</a></p>\n')
    except KeyError:
        pass
    unseen_profiles = unseen_profiles[1:]

out.write('</body></html>\n')
                         

#uids = data.keys()
#uids.sort()

