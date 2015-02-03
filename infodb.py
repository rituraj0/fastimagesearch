#!/usr/bin/env python

#infodb.py
#lists all the images in the database along with keys

import db
import sys

count = True
disp = False

if('--list' in sys.argv):
    disp = True
if('--help' in sys.argv):
    print 'usage: ', sys.argv[0], ' [--list]', ' => count and optionally list images in the database'
    print 'usage: ', sys.argv[0], ' --help', ' => print this message and quit'
    sys.exit()

print 'There are currently ', db.size(), ' images in the database'
if(disp):
    db.listimages()
    print '='*60
    print 'Finished listing ', db.size(), ' images.'



