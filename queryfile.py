#!/usr/bin/env python

import query
import sys
import db
import shelve
from numpy import *
from os import system
import string

if(len(sys.argv)<2):
    raise AssertionError, 'usage queryfile <queryimage>'

resultsperpage = 20
page=0

scores = query.ScoreQuery(sys.argv[1])
matches = argsort(scores)[0:resultsperpage]
print matches

try:
    idb = shelve.open(db.idbpath,flag='r')
except:
    raise IOError, 'Cannot open image database for reading'

cmd = '/usr/bin/gqview -l -t '

tmpdir = '/tmp'
for index in matches:
    iid = str(index).zfill(6)
    imgfile = idb[iid][0]
    cmd = cmd + '"' + imgfile + '" '
    #cmd = '/usr/bin/gqview -l -t "' + imgfile + '"'

system(cmd) #start slideshow



