#!/usr/bin/env python

"""Recursively add all images in a directory to the database

"""
import sys
import db
import preprocess
import os.path, fnmatch

verbose = 0

##from python cookbook
def listFiles(root, patterns='*', recurse=1, return_folders=0):

    # Expand patterns from semicolon-separated string to list
    pattern_list = patterns.split(';')
    # Collect input and output arguments into one bunch
    class Bunch:
        def __init__(self, **kwds): self.__dict__.update(kwds)
    arg = Bunch(recurse=recurse, pattern_list=pattern_list,
        return_folders=return_folders, results=[])

    def visit(arg, dirname, files):
        # Append to arg.results all relevant files (and perhaps folders)
        for name in files:
            fullname = os.path.normpath(os.path.join(dirname, name))
            if arg.return_folders or os.path.isfile(fullname):
                for pattern in arg.pattern_list:
                    if fnmatch.fnmatch(name, pattern):
                        arg.results.append(fullname)
                        break
        # Block recursion if recursion was disallowed
        if not arg.recurse: files[:]=[]

    os.path.walk(root, visit, arg)

    return arg.results

usage = 'usage: ' + sys.argv[0] + ' --dir <images-directory>'

if('--help' in sys.argv):
    print usage
    sys.exit(0)    
if('--verbose' in sys.argv):
    verbose = 1
dirArgIndex = sys.argv.index('--dir')
try:
    dir = sys.argv[dirArgIndex+1]
except IndexError:
    print 'Invalid directory argument'

if (not os.path.exists(dir)) or (not os.path.isdir(dir)):
    print 'Invalid directory argument'
    sys.exit(2)
    
images = listFiles(dir, '*.JPG;*.jpg;*.png;*.jpeg;*.bmp;*.dcx;*.gif;*.pcx;*.ppm;*.psd;*.tga;*.tif;*.tiff;*.xpm')
    
index = db.size()
for image in images:
    imat = preprocess.ProcessImage(image)
    if(numpy.count_nonzero(imat) > 0):
        iid = str(index).zfill(6) 
        db.addimg(iid,image)
        db.addsig(iid,imat[0],0)
        db.addsig(iid,imat[1],1)
        db.addsig(iid,imat[2],2)
        if(verbose): print 'added ', iid, ':', image
        index += 1
