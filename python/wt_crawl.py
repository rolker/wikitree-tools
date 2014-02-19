#!/usr/bin/env python

import sys
import json
import wt
import codecs
import urllib

home = None
gens = 6
out = None

for a in sys.argv[1:]:
    if '=' in a:
        parts = a.split('=',1)
        if parts[0] == 'gens':
            gens = int(parts[1])
        if parts[0] == 'out':
            out = parts[1]
    else:
        home = a

c = wt.Connection()
if home is None:
    home = c.uname
    
print 'home',home,'gens',gens

data = json.load(c.getPage('action=getPerson&key='+home+'&fields=Id'))

toCheck = []
checked = []

toCheck.append(data[0]['person']['Id'])

outfile = None
if out is not None:
    outfile = codecs.open(out,'w',encoding='utf-8')
    outfile.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head><body>\n')


for gen in range(gens):
    newToCheck = []
    if outfile is not None:
        outfile.write('<h1>Degree '+str(gen)+'</h1>\n')
    for uid in toCheck:
        checked.append(uid)
        data = json.load(c.getPage('action=getPerson&key='+str(uid)+'&fields=Name,FirstName,LastNameCurrent,Parents,Siblings,Children,Spouses'))[0]['person']
        print gen,data['Name'],
        name = ''
        if 'FirstName' in data:
            name += data['FirstName']+' '
            print data['FirstName'],
        if 'LastNameCurrent' in data:
            name += data['LastNameCurrent']+' '
            print data['LastNameCurrent'],
        print
        if outfile is not None:
            outfile.write('<a href="http://www.wikitree.com/wiki/'+data['Name']+'">'+name+'</a><br>\n')
        if type(data['Parents']) == type({}):
            for id in data['Parents'].keys():
                id = int(id)
                if not (id in toCheck or id in checked or id in newToCheck):
                    newToCheck.append(id)
        if 'Siblings' in data and type(data['Siblings']) == type({}):
            for id in data['Siblings'].keys():
                id = int(id)
                if not (id in toCheck or id in checked or id in newToCheck):
                    newToCheck.append(id)
        if 'Children' in data and type(data['Children']) == type({}):
            for id in data['Children'].keys():
                id = int(id)
                if not (id in toCheck or id in checked or id in newToCheck):
                    newToCheck.append(id)
        if 'Spouses' in data and type(data['Spouses']) == type({}):
            for id in data['Spouses'].keys():
                id = int(id)
                if not (id in toCheck or id in checked or id in newToCheck):
                    newToCheck.append(id)
        #print checked
        #print toCheck
        #print newToCheck
    toCheck = newToCheck
    
print len(checked),'checked'
if outfile is not None:
    outfile.write('</body></html>')
    