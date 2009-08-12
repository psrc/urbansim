from numarray import *
import time
def _unique(na_array):
    if not isinstance(na_array, NumArray):			
        raise TypeError, "na_array must be of type NumArray"
    if na_array.rank <> 1:
        na_array = na_array.flat
        raise RuntimeWarning, "Array na_array is converted a rank-1 array"

    n = len(na_array)
    if n == 0:
        return []
    
    na_array = sort(na_array)
    u=array([])

    
    while True:
        i = 0
        try:
            x = na_array[i]
        except IndexError:
            return u
        u = concatenate((u,x))
        if x == u[-1]:
            na_array=compress(not_equal(na_array, x),na_array)

def _unique2(na_array):
    if not isinstance(na_array, NumArray):			
        raise TypeError, "na_array must be of type NumArray"
    if na_array.rank <> 1:
        na_array = na_array.flat
        raise RuntimeWarning, "Array na_array is converted a rank-1 array"

    n = len(na_array)
    if n == 0:
        return []

    u = {}
    try:
        for x in na_array:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

def _unique3(na_array):
    if not isinstance(na_array, NumArray):			
        raise TypeError, "na_array must be of type NumArray"
    if na_array.rank <> 1:
        na_array = na_array.flat
        raise RuntimeWarning, "Array na_array is converted a rank-1 array"

    n = len(na_array)
    if n == 0:
        return []
    
    try:
        t = na_array.tolist()
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

b=arange(329)
b2 = repeat(b,340)
start_time = time.time()
print len(_unique(b2))
print "Elapsed time = " + str(time.time() - start_time)

start_time = time.time()
print len(_unique2(b2))
print "Elapsed time = " + str(time.time() - start_time)

start_time = time.time()
print len(_unique3(b2))
print "Elapsed time = " + str(time.time() - start_time)
