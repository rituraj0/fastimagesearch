#preprocess.py

#Module for preprocessing an image to get its signature

import math
import Image
from copy import *
from numpy import *
import numpy
import sys

path = '/mnt/windows/pictures/animals/163061.JPG'
path01 = '/mnt/windows/pictures/animals/image7.jpg'
sz = 128
tsize = sz,sz
#the tuple for RGB to YIQ color space conversion
#we work in the YIQ color space for best results
#unfortunately YIQ is not directly supported by PIL
rgb2yiq = (0.299, 0.587, 0.114, 0,
            0.596, -0.275, -0.321, 0,
            0.212, -0.523, 0.311, 0)


def Decompose(A):
    """ standard one dimensional Haar wavelet decomposition 
    
    Takes 1D array A of image data of length h which is a power of two
    Returns wavelet coefficients as array
    """

    #if type(A) != ArrayType:
     #   raise TypeError, 'Error: A must be a Numeric Python array'
    
    #if numpy.rank(A) != 1:
       # raise AssertionError, 'Error: A must be a row vector'
    
    h = len(A) #h is a power of two
    Aprime = zeros(h, float)
    if (h == 0):
        raise AssertionError, "Warning: Haar decomposition of zero length row attempted!"
    
    divide(A, math.sqrt(h), A)
    Root2 = math.sqrt(2)
    while h > 1:
        h=h/2
        for i in range(0,h):
            Aprime[i] = (A[2*i] + A[2*i+1])/Root2
            Aprime[h+i] = (A[2*i] - A[2*i+1])/Root2
        A = copy(Aprime)

    return A
    

def DecomposeImage(T):
    #if type(T) != ArrayType:
     #   raise TypeError, 'Error: T must be a Numeric Python array'
    
    #if numpy.rank(T) != 2:
       #raise AssertionError, 'Error: T must be a matrix'

    #decompose rows
    for row in range(0,len(T)):
        T[row] = Decompose(T[row])
    
    T = transpose(T)
    #Decompose columns
    for row in range(0,len(T)):
        T[row] = Decompose(T[row])
    
    T = transpose(T)

    return T

def TruncateImage(A, m):
    """Set all but m largest elements of A to 0"""
    #TODO error checks
    avgcolor = A[0,0] #save (0,0)th entry
    A[0,0] = numpy.min(numpy.min(A)) #make it least so that it is not included in the selection
    
    rowvect = reshape(A, (len(A)*len(A[0]),)) #flatten matrix to vector
    rowvect = sort(rowvect)[::-1] #sort and reverse
    thresh = rowvect[m] - 1 #select the (m+1)th-1 element as threshold
    multiply(A,(A>thresh).astype(float),A) #set all but m largest elements to 0
    A[0,0] = avgcolor #put back saved value
    return A

def QuantizeImage(A):
    """Quantizes A to 3 levels +1:positive, 0, -1:negative"""
    avgcolor = A[0,0] #save (0,0)th entry
    A = sign(A).astype(float)
    A[0,0] = avgcolor #put back saved value
    return A
    
#always return something , bug fix 

def ProcessImage(path):
    
    print(path);

    try:
        im = Image.open(path)
        print( "opend successfulyy");
    except:
        print 'Unknown format ', path, ' => skipping'
        return numpy.zeros((3,sz,sz), float)
    #resize the image to standard size
    #we don't worry about the aspect ratio
    try:
        im = im.resize(tsize, Image.ANTIALIAS)
    
        im = im.convert('RGB', rgb2yiq) #convert to YIQ color space
        colorplanes = im.split() #separate the three color planes
    except:
        sys.stderr.write("Cannot manipulate " + path + " => Skipping ... \n")
        return numpy.zeros((3,sz,sz), float)
    
    imat = numpy.zeros((3,sz,sz), float) #create a 3 x sz x sz matrix for converting image to matrix

    print( " imat initalized");  
    
    #convert data in each colorplane to matrix
    for cp,i in zip(colorplanes,range(0,3)):
        imat[i] = reshape(array(cp.getdata(), float), tsize)
        
    for i in range(0,3):
        imat[i] = DecomposeImage(imat[i])
        #print imat[i]
        #print '-'*90
        imat[i] = TruncateImage(imat[i],30)
        #print imat[i]
        #print '-'*90
        imat[i] = QuantizeImage(imat[i])
        #print imat[i]
        #print '='*90
        #raw_input('Press Enter for next colorplane')

    #print(imat);

    return imat

