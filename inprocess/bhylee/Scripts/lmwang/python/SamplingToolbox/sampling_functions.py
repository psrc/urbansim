#! /projects/urbansim/third-party/ActivePython/bin/python

#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import os,sys
from numarray import array, asarray, arange, concatenate, zeros, ones, \
     sometrue, where, equal, not_equal, nonzero, NumArray, \
     reshape, sum, cumsum, sort, searchsorted, repeat, argsort, \
     Float32
from numarray.random_array import randint, seed, uniform, random

def SampleReplace(source_array, size):
    """Equal probability sampling; with-replacement case"""
    
    min = 0; max = source_array.size()
    return source_array[randint(min,max,size)]

def SampleNoReplace(source_array, size):
    """Equal probability sampling; without-replacement case"""

    src_array = source_array.copy()
    min = 0; max = src_array.size()
    dest_array = array([])
    for i in range(size):
        j = randint(min,max)
        dest_array = concatenate((dest_array, src_array[j]))
        max -= 1
        src_array[j] = src_array[max]
    return dest_array

def ProbSampleReplace(source_array, size, prob_array, output=None):
    """Unequal probability sampling; replacement case"""
    if prob_array is None:
        return SampleReplace(source_array,size)

    src_array = source_array.copy()
    prb_array = prob_array.copy()
    
    #descending order by probability, is ordering necessary?
    #order = argsort(prb_array)
    #order[arange(order.size-1,0)] = order
    
    #src_array = src_array[order]
    #prb_array = prb_array[order]
    
    cum_prob = cumsum(prb_array)
    n = src_array.size()
    s = []
    for i in range(size):
        r = random()
        for j in range(n):
            if r <= cum_prob[j]:break
        s.append(src_array[j])
    output = asarray(s)
    #if output is None:
    return output

def ProbSampleReplaceL(source_array, size, prob_array):
    """Unequal probability sampling; replacement case.
    Using numarray searchsorted function, suitable for large array"""

    if prob_array is None:
        return SampleReplace(source_array,size)
    
    cum_prob = cumsum(prob_array)
    sample_prob = uniform(0, 1, shape = (size,))

    output = searchsorted(cum_prob, sample_prob)
    #if output is None:
    return output

def ProbSampleNoReplace(source_array, size, prob_array):
    """Unequal probability sampling; without-replacement case"""
    if prob_array is None:
        return SampleNoReplace(source_array,size)
    
    src_array = source_array.copy()
    prb_array = prob_array.copy()

    if sum(prb_array) <> 1:
        raise RuntimeError,"prob_array doesn't sum up to 1"
    #cum_prob = cumsum(prob_array)
    dest_array = array([])
    totalmass = 1
    n = src_array.size() - 1
    for i in range(size):
        r = random() * totalmass
        mass = 0
        for j in range(n):
            mass += prb_array[j]
            if r <= mass: break
        dest_array = concatenate((dest_array, src_array[j]))
        totalmass -= prb_array[j]
        for k in range(j,n):
            src_array[j] = src_array[j+1]
            prb_array[j] = prb_array[j+1]
        n -= 1
    return dest_array

def sample_1d_array_of_non_repeat_random_num(from_array, sample_size, init=None, weight_array=None):
    """generate non-repeat random 1d samples from from_array of sample_size, not including
    indices appeared in init.

    return indices to from_array.

    from_array - the source array to sample from
    sample_size - scalar representing the sample size
    init - array representing indices should not appear in resulted array
    weight_array - the array used to weight sample
    """

    if not isinstance(from_array, NumArray):
        try:
            from_array = asar(from_array)
        except:
            raise TypeError, "from_array must be of type NumArray"

    min = 0; max = from_array.size()
    if max <= sample_size:
        print "there are less indices (%s) in from_array than the sample_size (%s). Sample %s instead. " %\
              (max, sample_size, max)
        #sample_size = max
        return from_array

    if weight_array is not None:
        if not isinstance(weight_array, NumArray):
            try:
                from_array = asar(from_array)
            except:                
                raise TypeError, "weight_array must be of type NumArray"

        size_weight_array = nonzero(weight_array)[0].size()
        if size_weight_array <= sample_size:
            print "there are less non-zero weight (%s) in weight_array than the sample_size (%s). Sample %s instead. " %\
                  (size_weight_array, sample_size, size_weight_array)
            #sample_size = size_weight_array
            return from_array[nonzero(weight_array)]

        weight_sum = cumsum(weight_array)
        max = weight_sum[-1]


    if init is not None:
        if not isinstance(init, NumArray):
            try:
                init = asarray(init)
            except:
                raise TypeError, "init must be of type NumArray"
        init = init.flat
        if sometrue(self.find_duplicates1d(init)):
            raise RuntimeWarning, "init includes duplicates and they will be replaced!"
    else:
        init = asarray([])

    dup_index = arange(sample_size) + init.size()
    sample_index = concatenate((init, zeros(dup_index.shape)-1))
    while True:
        sample_index[dup_index] = randint(min,max,dup_index.shape)
        if weight_array is not None:
            sample_index[dup_index] = searchsorted(weight_sum,sample_index[dup_index])
        dup_index = find_duplicates1d(sample_index)
        if not sometrue(dup_index): break
    return from_array[sample_index]


def sample_2d_array_of_non_repeat_random_num_by_column(from_array, sample_size, init=None, weight_array=None):
    """generate non-repeat random 2d samples from from_array of sample_size, not including
    indices appeared in init; sample column by column, more efficient when there are more 
    rows than columns in sample_size.

    return indices to from_array.

    from_array - the source array to sample from
    sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row
    init - array representing indices should not appear in resulted array
    weight_array - the array used to weight sample
    """
    rows = sample_size[0]
    columns = sample_size[1]
    min = 0; max = from_array.size()
    if max < columns:
        raise ValueError, "There are less indices (%s) in from_array than the sample_size (%s). Sample %s instead. " %\
              (max, sample_size, max)
        #sample_size = max
    elif max == columns:
        return from_array.resize((rows,columns))

    if weight_array is not None:
        if not isinstance(weight_array, NumArray):
            raise TypeError, "weight_array must be of type NumArray"

        size_weight_array = nonzero(weight_array)[0].size()
        if size_weight_array < columns:
            raise ValueError, "there are less non-zero weight (%s) in weight_array than the sample_size (%s). Sample %s instead. " %\
                  (size_weight_array, columns, size_weight_array)
        elif size_weight_array == columns:
            return from_array[nonzero(weight_array)].resize((rows,columns))

        weight_sum = cumsum(weight_array)
        max = weight_sum[-1]

    sampled_choiceset_index = zeros(sample_size)-1    #initialize

    if init is not None:
        if not isinstance(init, NumArray):            
            try:
                init = asarray(init)
            except:
                raise TypeError, "init must be of type NumArray"
        if init.shape[0] <> rows:
            raise ValueError, "init should have the same number of rows as sample_size[0]"
        cols = init.size()/init.shape[0]    #get the num of cols in init
        init.resize((sample_size[0],cols))
        #sampled_choiceset_index = concatenate((init,sampled_choiceset_index),axis=1)    #attach init to the beginning of sampled_choiceset_index

    for j in range(columns, 0, -1):
        dup_index = arange(rows)
        sample_index = zeros(dup_index.shape)-1  #initialize
        compared_set = concatenate((init,sampled_choiceset_index),axis=1)
        while True:
            sample_index[dup_index] = randint(min, max, dup_index.shape)
            if weight_array is not None:
                sample_index[dup_index] = searchsorted(weight_sum, sample_index[dup_index])
            dup_index = find_duplicates2d(sample_index, compared_set)
            if not sometrue(dup_index): break

        sampled_choiceset_index[:,-j] = from_array[sample_index]
        #compared_set = concatenate((init,sampled_choiceset_index),axis=1)

    return sampled_choiceset_index

def sample_2d_array_of_non_repeat_random_num_by_row(from_array, sample_size, init=None, weight_array=None):
    """generate non-repeat random 2d samples from from_array of sample_size, not including
    indices appeared in init; sample column by column, more efficient when there are more 
    rows than columns in sample_size.

    return indices to from_array.

    from_array - the source array to sample from
    sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row
    init - array representing indices should not appear in resulted array
    weight_array - the array used to weight sample
    """

    min = 0; max = from_array.size()
    if weight_array is not None:
        if not isinstance(weight_array, NumArray):
            raise TypeError, "weight_array must be of type NumArray"
        weight_sum = cumsum(weight_array)
        max = weight_sum[-1]

    sample_set = zeros(sample_size)-1
    if init is not None:
        if not isinstance(init, NumArray):            
            try:
                init = asarray(init)
            except:
                raise TypeError, "init must be of type NumArray"
        if init.shape[0] <> sample_size[0]:
            raise RuntimeError, "init should have the same number of rows as sample_size[0]"
        cols = init.size()/init.shape[0]    #get the num of cols in init
        init.resize((sample_size[0],cols))
        sample_set = concatenate((init,sample_set),axis=1)

        for j in range(sample_size[0]):
            sample_set[j,:] = sample_1d_array_of_non_repeat_random_num\
                      (from_array, sample_size=sample_size[1],init=init[j,...],weight_array=weight_array)
    else:
        for j in range(sample_size[0]):
            sample_set[j,:] = sample_1d_array_of_non_repeat_random_num\
                      (from_array, sample_size=sample_size[1],weight_array=weight_array)

    return sample_set


def find_duplicates1d(checking_set):
    """find indices of duplicate values in a list or array"""

    checking_set = asarray(checking_set)
    checking_set = checking_set.flat   #convert to a rank-1 array

    allsum = zeros(checking_set.shape)
    allone = ones(checking_set.shape)
    for a in checking_set:
        allsum += where(equal(checking_set, a), 1, 0)
    has_duplicates = allsum-allone
    dup_idx = nonzero(has_duplicates)
#         if dup_idx[0].size() > 0:
#             self.debug.print_debug("found repeats at index: ",5)
#             self.debug.print_debug(dup_idx[0],5)            
    return dup_idx[0]

def find_duplicates2d(checking_set, compared_set):
    """find indices of duplicate values at checking_set"""

    checking_set = asarray(checking_set)
    if checking_set.rank <> 1:
        raise ValueError, "Array checking_set must be a rank-1 array"
    compared_set = asarray(compared_set)
    if compared_set.shape[0] <> checking_set.shape[0]:
        raise ValueError, "Arrays have incompatible shapes"

    checking_set = reshape(checking_set,(compared_set.shape[0],-1))
    is_duplicates = where(equal(checking_set, compared_set,),1,0)
    has_duplicates = sum(is_duplicates, axis=1)
    dup_idx = nonzero(has_duplicates)
#         if dup_idx[0].size() > 0:
#             self.debug.print_debug("found repeats at index: ",5)
#             self.debug.print_debug(dup_idx[0],5)
    return dup_idx[0]


def unique_values(na_array):
    """return unique elements of na_array
    na_array - a NumArray object
    """

    if not isinstance(na_array, NumArray):            
        raise TypeError, "na_array must be of type NumArray"
    if na_array.rank <> 1:
        na_array = na_array.flat
        raise RuntimeWarning, "Array na_array is converted a rank-1 array"

    n = len(na_array)
    if n == 0:
        return []

    try:
        t = sort(na_array)
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