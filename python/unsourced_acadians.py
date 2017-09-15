#!/usr/bin/env python

import sys
import csv
import gzip

csv.field_size_limit(sys.maxsize)

acadians = []
unsourced = []
unsourced_acadians = []

cat_fname = 'data/dump_categories.csv.gz'
users_fname = 'data/dump_people_user.csv.gz'

cat_file = gzip.open(cat_fname,'r')

reader = csv.reader(cat_file,delimiter='\t')
for row in reader:
    print row
    if row[1] == 'Acadians':
        acadians.append(row[0])
    if row[1] == 'Unsourced_Profiles':
        unsourced.append(row[0])

print 'finding acadians that are unsourced...'
for a in acadians:
    if a in unsourced:
        unsourced_acadians.append(a)
        
print unsourced_acadians

users_file = gzip.open(users_fname,'r')
reader = csv.reader(users_file,delimiter='\t')
for row in reader:
    if row[0] in unsourced_acadians:
        print row
    
