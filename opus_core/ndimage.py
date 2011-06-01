# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

# Functions to work around  numpy/scipy bug -- need to fix the char and num attributes of arrays with dtype==int32
# to get them to work with ndimage.sum etc.  TODO: remove this if scipy bug gets fixed.
# The problem is that under some circumstances dtype.char and dtype.num have the wrong values (for intc
# rather than int_, the native python int 32 type).
# See comment at the end of this file for more details.

from numpy import int32, int64, ndarray, ones, array, asarray
import scipy, scipy.ndimage
import numpy

# *** ndimage.measurements functions ***

def sum(input, labels=None, index=None):
    # work around for sum() method of scipy.ndimage not allowing numpy.int64 index type
    # this won't be needed if scipy ticket #1162 is fixed: http://projects.scipy.org/scipy/ticket/1162
    if index is not None and getattr(index, "dtype", int32) == int64 and index.max() <= numpy.iinfo(int32).max:
        index = index.astype(int32)

    _fix_dtype(input)
    if labels is not None:
        _fix_dtype(labels)
    if index is not None:
        _fix_dtype(index)
    if index is not None and (labels is None or len(labels) ==0):
        return scipy.ndimage.sum(input, labels=None, index=index) * ones(array(len(index)))
    return scipy.ndimage.sum(input, labels, index)

def mean(input, labels=None, index=None):
    _fix_dtype(input)
    _fix_dtype(labels)
    _fix_dtype(index)
    if index is not None and (labels is None or len(labels) ==0):
        results = scipy.ndimage.mean(input, labels=None, index=index) * ones(array(len(index)))
    else: 
        results = scipy.ndimage.mean(input, labels, index)
    ## scipy 0.7.0 may return a list instead of an array
    results = asarray(results)
    ## scipy 0.8.0 returns NaN for 0 counts
    if numpy.any(numpy.isnan(results)):
        results[numpy.isnan(results)] = 0
    return results

def labeled_comprehension(input, labels, index, func, out_dtype, default, pass_positions=False):
    '''
    Taken from the trunk version of scipy/ndimage/measurements.py
    
    Roughly equivalent to [func(input[labels == i]) for i in index].

    Special cases:
      - index a scalar: returns a single value
      - index is None: returns func(inputs[labels > 0])

    func will be called with linear indices as a second argument if
    pass_positions is True.
    '''
    
    as_scalar = numpy.isscalar(index)
    input = numpy.asarray(input)

    if pass_positions:
        positions = numpy.arange(input.size).reshape(input.shape)

    if labels is None:
        if index is not None:
            raise ValueError, "index without defined labels"
        if not pass_positions:
            return func(input.ravel())
        else:
            return func(input.ravel(), positions.ravel())

    try:
        input, labels = numpy.broadcast_arrays(input, labels)
    except ValueError:
        raise ValueError, "input and labels must have the same shape (excepting dimensions with width 1)"

    if index is None:
        if not pass_positions:
            return func(input[labels > 0])
        else:
            return func(input[labels > 0], positions[labels > 0])

    index = numpy.atleast_1d(index)
    if numpy.any(index.astype(labels.dtype).astype(index.dtype) != index):
        raise ValueError, "Cannot convert index values from <%s> to <%s> (labels' type) without loss of precision"%(index.dtype, labels.dtype)
    index = index.astype(labels.dtype)

    # optimization: find min/max in index, and select those parts of labels, input, and positions
    lo = index.min()
    hi = index.max()
    mask = (labels >= lo) & (labels <= hi)

    # this also ravels the arrays
    labels = labels[mask]
    input = input[mask]
    if pass_positions:
        positions = positions[mask]

    # sort everything by labels
    label_order = labels.argsort()
    labels = labels[label_order]
    input = input[label_order]
    if pass_positions:
        positions = positions[label_order]
    
    index_order = index.argsort()
    sorted_index = index[index_order]

    def do_map(inputs, output):
        '''labels must be sorted'''
        
        nlabels = labels.size
        nidx = sorted_index.size

        # Find boundaries for each stretch of constant labels
        # This could be faster, but we already paid N log N to sort labels.
        lo = numpy.searchsorted(labels, sorted_index, side='left')
        hi = numpy.searchsorted(labels, sorted_index, side='right')
    
        for i, l, h in zip(range(nidx), lo, hi):
            if l == h:
                continue
            idx = sorted_index[i]
            output[i] = func(*[inp[l:h] for inp in inputs])
            
    temp = numpy.empty(index.shape, out_dtype)
    temp[:] = default
    if not pass_positions:
        do_map([input], temp)
    else:
        do_map([input, positions], temp)
    output = numpy.zeros(index.shape, out_dtype)
    output[index_order] = temp

    if as_scalar:
        output = output[0]

    return output

def median(input, labels = None, index = None):   
    """
    Calculate the median of the input array by label.

    Parameters
    ----------

    input : array_like
        median of the values of `input` inside the regions defined by `labels`
        are calculated.

    labels : array of integers, same shape as input
        Assign labels to the values of the array.

    index : scalar or array
        A single label number or a sequence of label numbers of
        the objects to be measured.

    Returns
    -------

    output : array
        An array of the median of the values of `input` inside the regions
        defined by `labels`.

    See also
    --------

    mean

    Examples
    --------

    >>> median(array([1,2,8,5, 2,4,6, 7]), labels=array([1,1,1,1, 2,2,2, 5]))
    4.5
    >>> median(array([1,2,8,5, 2,4,6, 7]), labels=array([1,1,1,1, 2,2,2, 5]), index=2)
    4
    >>> median(array([1,2,8,5, 2,4,6, 7]), labels=array([1,1,1,1, 2,2,2, 5]), index=array([1,5]))
    array([3.5, 7])
    >>> median(array([1,2,8,5, 2,4,6, 7]), labels=None, index=None))
    4.5
    
    """

    return labeled_comprehension(input, labels, index, numpy.median, numpy.float, 0.0, pass_positions=False)

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
    if isinstance(a, ndarray) and a.dtype == int32:
        a.dtype = int32


## lmwang: this seems to have been fixed as of numpy 1.4.0 and scipy 0.7.2
## the below code doesn't emit any error for me

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

from opus_core.tests import opus_unittest

class ndimageTests(opus_unittest.OpusTestCase):
    def test_median(self):
        from numpy import array, all
        input = array([1,2,8,5, 2,4,6, 7, 19])
        labels=array([1,1,1,1, 2,2,2, 5, 0])
        
        index = None
        expected = 4.5
        self.assert_(all(median(input, labels=labels, index=index)==expected))

        index = 2
        expected = 4
        self.assert_(all(median(input, labels=labels, index=index)==expected))

        index = array([1,5])
        expected = array([3.5,7])
        self.assert_(all(median(input, labels=labels, index=index)==expected))

        index = array([1,2,5])
        expected = array([3.5,4,7])
        self.assert_(all(median(input, labels=labels, index=index)==expected))

        labels = None
        index = None
        expected = 5.0
        self.assert_(all(median(input, labels=labels, index=index)==expected))

    def test_empty_array_zero_identity_error1(self):
        """test fix for scipy 0.8.0
        """
        from numpy import array, all, int64, int32
        input = array([],dtype=int32)
        labels=array([], dtype=int32)
        index = None
        expected = 0
        results = sum(input, labels=labels, index=index)
        self.assert_(all(results==expected))

    def test_empty_array_zero_identity_error2(self):
        """ test fix for scipy 0.8.0
        """
        from numpy import array, all, int64, int32
        input = array([],dtype=int32)
        labels=array([], dtype=int32)
        index = array([1,2,3],dtype=int32)
        expected = array([0, 0, 0], dtype=int32)
        results = sum(input, labels=labels, index=index)
        self.assert_(all(results==expected))
        self.assert_(len(results)==len(expected))
        
        index = [1,2,3]
        expected = array([0, 0, 0], dtype=int32)
        results = sum(input, labels=labels, index=index)
        self.assert_(all(results==expected))
        self.assert_(len(results)==len(expected))

    def test_ndimage_mean_nan(self):
        """ test fix for ndimage.mean for scipy 0.8.0
        """
        from numpy import array, all, int64, int32
        input = array([],dtype=int32)
        labels=array([], dtype=int32)
        index = array([1,2,3],dtype=int32)
        expected = array([0, 0, 0], dtype=int32)
        results = mean(input, labels=labels, index=index)
        self.assert_(all(results==expected))
        self.assert_(len(results)==len(expected))
        
        index = [1,2,3]
        expected = array([0, 0, 0], dtype=int32)
        results = mean(input, labels=labels, index=index)
        self.assert_(all(results==expected))
        self.assert_(len(results)==len(expected))

    def MASKED_test_empty_array_memory_error(self):
        """ weird error introduced in scipy 0.8.0
        """
        from numpy import array, all, int64, int32
        input = array([], dtype=int64)
        labels=array([])  ## default to float64
        print labels.dtype
        index = array([1,2,3])
        expected = 0
        self.assert_(all(sum(input, labels=labels, index=index)==expected))
                
if __name__ == "__main__":
    opus_unittest.main()
