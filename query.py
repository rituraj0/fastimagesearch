#query.py

#Module to resolve a query
import db
import preprocess
import shelve
from numpy import *
import string
import numpy
import math

#create a 6x3 matrix for storing weights
#actual weights are read from external file
w = reshape(numpy.zeros(6*3, float), (6,3))

def loadweights(wfile):
    """ loads weights into w from wfile """
    try:
        f = open(wfile)
    except IOError:
        raise IOError, 'Cannot open weights-file'

    lines = f.readlines()
    for i,l in zip(range(0,6),lines):
        w[i] = array([float(x) for x in string.split(l)], float) #read and store weights

#call loadweights to load the default weights at module import time
loadweights('weights_paint.txt')

def bin(i,j):
    """ function to map coefficients into small number of bins

    it maps i,j to one of the 6 weights
    this functiion here is the one originally used by the authors of the paper
    since weights used are also from the paper the same bin function is used.
    """
    return min(max(i,j),5)


def ScoreQuery(query):
    """ generate scores for query image using m wavelet coefficients

    query is a path to uery image file
    returns a list of image scores
    number of wavelet coefficients is redefined in the preprocess model
    """
    qmat = preprocess.ProcessImage(query)

    print(qmat.shape);

    if(numpy.count_nonzero(qmat) == 0):
        raise AssertionError, 'Cannot preprocess query image'
        return

    scores = numpy.zeros(db.size(), float) #initialize scores for each image

    print(" score size is %s ",scores.size);

    #open databases for reading
    try:
        idb = shelve.open(db.idbpath,flag='r')
    except:
        raise AssertionError, 'Cannot open image database'


    print(" w shape is %s ", w.shape);

    for c in range(0,3): #for each color channel
        #open searcharrays for this color channel
        print 'color channel: ', c
        try:
            sa_plus = shelve.open(db.sadbpaths[c][0],flag='r')
            sa_minus = shelve.open(db.sadbpaths[c][1],flag='r')
        except:
            raise IOError, 'Cannot open search array(s) for colorplane ' + str(c)
        
        for iid in idb.keys(): #for each image
            print(" iid id %s int(iid) is %s  c is %s ", iid , int(iid) ,c  );
            print( len( idb[iid]) ); 
            if( len( idb[iid]) == 4 ): # otherwise corrupt data in db 
                scores[int(iid)] += w[0,c] * math.fabs(qmat[c,0,0] - idb[iid][c+1])#idb[iid][c+1]
            print(" done ");

        #set this color channel's avg color val to 0 so that it does not take
        #part in further scoring of images
        qmat[c,0,0] = 0

        print( qmat[c,0,0] );

        print(" we  are here %s ",w.size);

        for row in range(0,len(qmat[c])):
            indices = nonzero(qmat[c,row])
            indices = indices[0]; # bug-fixed
            for col in indices: #for each non-zero coefficient
                rowcolid = str(row).zfill(3) + str(col).zfill(3)
                #print rowcolid,
                imglist = []
		print( qmat[c,row,col]  );
                if(qmat[c,row,col] > 0): #positive search array
                    try:
                        iList = sa_plus[rowcolid]
                        imglist.extend(iList)
                    except KeyError:
                        continue
                else: #negative search array
                    try:
                        iList = sa_minus[rowcolid]
                        imglist.extend(iList)
                    except KeyError:
                        continue

                #print imglist
                for iid in imglist: #for each image in the matched im list
                    scores[int(iid)] -= w[bin(row,col),c] #update the scores

        sa_plus.close()
        sa_minus.close()

    idb.close()
    return scores

