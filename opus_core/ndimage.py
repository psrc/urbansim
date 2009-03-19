# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

# Functions to work around  numpy/scipy bug -- need to fix the char and num attributes of arrays with dtype==int32
# to get them to work with ndimage.sum etc.  TODO: remove this if scipy bug gets fixed.
# The problem is that under some circumstances dtype.char and dtype.num have the wrong values (for intc
# rather than int_, the native python int 32 type).
# See comment at the end of this file for more details.

from numpy import int32
import scipy.ndimage

# *** ndimage.measurements functions ***

def sum(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.sum(input, labels, index)

def mean(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.mean(input, labels, index)

def variance(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.variance(input, labels, index)

def standard_deviation(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.standard_deviation(input, labels, index)

def minimum(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.minimum(input, labels, index)

def maximum(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.maximum(input, labels, index)

def minimum_position(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.minimum_position(input, labels, index)

def maximum_position(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.maximum_position(input, labels, index)

def extrema(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.extrema(input, labels, index)

def center_of_mass(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    return scipy.ndimage.center_of_mass(input, labels, index)
    
# *** ndimage.filters functions ***

def correlate(input, weights, output=None, mode='reflect', cval=0.0, origin=0):
    _fix_dtype(input)
    _fix_dtype(weights)
    return scipy.ndimage.correlate(input, weights, output, mode, cval, origin)


# *** private functions (to fix dtype) ***

def _fix_dtype(a):
    if a.dtype == int32:
        a.dtype = int32


# More details on the numpy/scipy bug:
# Running the following test code will trigger the error:

# from numpy import array, ma, int32
# from scipy import ndimage
# a = array([1,2,3,4])
# m = ma.masked_array(10-a, mask=False)
# ndimage.sum(ma.filled(m, 0))

# if you put this line before the ndimage.sum command then it works:
# m.dtype = int32

# Even though numpy thinks the dype of m is int32, there is a difference from the standard one:
# before changing dtype:
#   m.dtype.char = 'i'
#   m.dtype.num = 5
# afterwards:
#   m.dtype.char = 'l'
#   m.dtype.num = 7
# The former one is for numpy type intc; the latter is for int_ (corresponding to the builtin Python type int)
