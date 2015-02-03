#imdb.py

#Module to handleimage database

import shelve
import sys
from numpy import *
import numpy

#paths for the image and searcharray database files
#searcharrays are stored in 6 databases 
#eg. db_sa1p: search array for color 1 positive values
#    db_sa0m: search array for color 0 negative values
idbpath = 'db_imagedb'
sadbpaths = [ ['db_sa0p','db_sa0m'], ['db_sa1p','db_sa1m'], ['db_sa2p','db_sa2m']]

def listimages():
    """ lists all the existing images in the database """

    try:
        idb = shelve.open(idbpath, writeback=True)
    except:
        sys.stderr.write('Error: Cannot open image database\n')
        return None
    for k, i in idb.iteritems():
        print k, ':', i[0],
        for v in i[1:]:
            print ' %4.2f ' % v,
        print
    idb.close()
    
def size():
    """ returns the current database size

    database size is determined by the number of images
    """
    try:
        idb = shelve.open(idbpath, writeback=True)
    except:
        sys.stderr.write('Error: Cannot open image database\n')
        return None

    entries = len(idb)
    idb.close()
    return entries
    
def addimg(iid, path):
    """ add image to the image database

    iid: image id (string)
    path: path to actual image

    if iid already exists it will be overwritten (be careful)
    """
    try:
    	idb = shelve.open(idbpath,writeback=True)
    except IOError:
        raise IOError, 'Error: Cannot open image database'
        
    idb[iid] = [ path ] 
    idb.close() #writeback mode might make this slower

def addsig(iid, imat, cp):
    """ add image signature to database

    iid: image id (string)
    imat: image waelet matrix from preprocessing
    cp: colorplane to be used

    no check is made to see if iid already exists
    even if it does, it will be added to search array at appropriate position

    also appends the avg color - corresponding to imat[0,0] - for this channel in imagedb
    """
    try:
        sa_plus = shelve.open(sadbpaths[cp][0],writeback=True)
        sa_minus = shelve.open(sadbpaths[cp][1],writeback=True)
    except:
        raise IOError, 'Cannot open search array(s) for colorplane '+ str(cp)

    try:
        idb = shelve.open(idbpath, writeback=True)
    except:
        raise IOError, 'Cannot open image database for update'

    idb[iid].append(imat[0,0]) #add avg color for channel cp to image database
    idb.close()

    print( imat.shape );
    print( imat[0,0] );
    
    #now we go through each of the non-zero coefficients in imat
    #and append the iid to appropriate position in the corresponding search array
    for row in range(0,len(imat)):
        indices = numpy.nonzero(imat[row]) #get nonzero indices in imat  
        indices = indices[0]; #bug-fix
         

        #print(indices);
     
        for col in indices:
 
            rowcolid = str(row).zfill(3) + str(col).zfill(3) #generate rowcolid string for database
            
            #print(row)
            #print(col)
            
            #print( imat[row,col] );           

            if(imat[row,col] > 0):
                if(sa_plus.has_key(rowcolid)):
                    sa_plus[rowcolid].append(iid) #if positive append to postive search array
                else:
                    sa_plus[rowcolid] = [iid]
            else:
                if(sa_minus.has_key(rowcolid)):
                    sa_minus[rowcolid].append(iid) #else append to negative search array
                else:
                    sa_minus[rowcolid] = [iid]

    #writeback mode might make this slower
    sa_plus.close()
    sa_minus.close()


