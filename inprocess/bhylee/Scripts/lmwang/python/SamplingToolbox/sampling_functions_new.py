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
     Float32, Float64, NewAxis, rank, take
from numarray.random_array import randint, seed, uniform, random
from opus.core.miscellaneous import DebugPrinter

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

def SampleNoReplaceL(source_array, size):
    """equal probability sampling; without replacement case.
    Using numarray functions, efficient for large array"""

    #fake a equal value prob_array, so we can call ProbSampleNoReplaceL
    prob_array = ones(source_array.size()).astype(Float64)
    return ProbSampleNoReplaceL(source_array, size, prob_array)


def ProbSampleReplace(source_array, size, prob_array):
    """Unequal probability sampling; with replacement case"""
    if prob_array is None:
        return SampleReplace(source_array,size)

    src_array = source_array.copy()
    prb_array = prob_array.copy().astype(Float64)
    
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

    return output

def ProbSampleReplaceL(source_array, size, prob_array, debuglevel=0):
    """Unequal probability sampling; with replacement case.
    Using numarray searchsorted function, suitable for large array"""

    if prob_array is None:
        return SampleReplace(source_array,size)

    if sum(prob_array) == 0:
        raise ValueError, "there aren't non-zero weights in prob_array"

    prob_array = prob_array.astype(Float64)
    cum_prob = cumsum(prob_array)
    sample_prob = uniform(0, 1, shape = (size,))

    output = searchsorted(cum_prob, sample_prob)

    return output

def ProbSampleNoReplace(source_array, size, prob_array, debuglevel=0):
    """Unequal probability sampling; without replacement case"""
    debug = DebugPrinter(debuglevel)
    
    if prob_array is None:
        return SampleNoReplace(source_array,size)
    
    src_array = source_array.copy()
    p_array = prob_array.copy().astype(Float64)

    if sum(p_array) <> 1:
        p_array = p_array / sum(p_array)
        debug.print_debug("prob_array doesn't sum up to 1, and is normalized.",5)

    dest_array = array([])
    totalmass = 1
    n = src_array.size() - 1
    for i in range(size):
        r = random() * totalmass
        mass = 0
        for j in range(n):
            mass += p_array[j]
            if r <= mass: break
        dest_array = concatenate((dest_array, src_array[j]))
        totalmass -= p_array[j]
        for k in range(j,n):
            src_array[j] = src_array[j+1]
            p_array[j] = p_array[j+1]
        n -= 1
    return dest_array

def ProbSampleNoReplaceL(source_array, sample_size, prob_array=None, exclude_index=None, debuglevel=0):
    """generate non-repeat random 1d samples from source_array of sample_size, excluding
    indices appeared in exclude_index.

    return elements in source_array.

    source_array - the source array to sample from
    sample_size - scalar representing the sample size
    prob_array - the array used to weight sample
    exclude_index - array representing indices should not appear in resulted array,
                    which can be used, for example, to exclude current choice from sampling
    """

    debug = DebugPrinter(debuglevel)
    if not isinstance(source_array, NumArray):
        try:
            source_array = asarray(source_array)
        except:
            raise TypeError, "source_array must be of type NumArray"

    pop_size = source_array.size()
    if pop_size <= sample_size:
        debug.print_debug("Warning: there are less indices (%s) in source_array than the sample_size (%s). Sample %s instead. " %\
              (pop_size, sample_size, pop_size), 1)
        #sample_size = max
        return source_array

    if prob_array is None:
        return SampleNoReplaceL(source_array, sample_size)
    
    if not isinstance(prob_array, NumArray):
        try:
            source_array = asarray(source_array)
        except:
            raise TypeError, "prob_array must be of type NumArray"

    #import pdb; pdb.set_trace()
    prob_array_size = nonzerocounts(prob_array)
    if prob_array_size <= sample_size:
        debug.print_debug("Warning: there are less non-zero weight (%s) in prob_array than the sample_size (%s). Sample %s instead. " %\
              (prob_array_size, sample_size, prob_array_size), 1)
        return source_array[prob_array>0]

    p_array = prob_array.copy().astype(Float64)
    
    if sum(p_array) <> 1.0:
        p_array = p_array / sum(p_array)
        debug.print_debug("prob_array doesn't sum up to 1, and is normalized.",5)

    totalmass = 1.0
    to_be_sampled = sample_size
    sampled = array([])  #initialize sampled

    if exclude_index is not None:
        try:
            totalmass -= sum(p_array[exclude_index])
            p_array[exclude_index] = 0
        except:
            raise IndexError, "Having problem to apply exclude_index values"
    
    prob_sum = cumsum(p_array)
    
    while True:
        sample_prob = uniform(0, totalmass, shape=(to_be_sampled,))
        proposed_index = searchsorted(prob_sum, sample_prob)

#         dup_indicator = find_duplicates_self(proposed_index)        
#         valid_index = proposed_index[dup_indicator==0]
#         sampled = concatenate((sampled, source_array[valid_index]))

#         if not sometrue(dup_indicator):
#             return sampled

        #TODO:: try to the performace of using unique_values in the place of find_duplicates1d
        valid_index = unique_values(proposed_index)
        #import pdb; pdb.set_trace()
        sampled = concatenate((sampled, source_array[valid_index]))
        if valid_index.size() == to_be_sampled:
            return sampled
        
        totalmass -= sum(p_array[valid_index])
        p_array[valid_index] = 0

        #TODO::should we update the p_array?
        #p_array = p_array / sum(p_array)
        prob_sum = cumsum(p_array)
        to_be_sampled -= valid_index.size()
        
    #return source_array[sampled_index]


def Prob2dSampleNoReplaceL(source_array, sample_size, prob_array=None, exclude_index=None, debuglevel=0):
    """generate non-repeat random 2d samples from source_array of sample_size, not including
    indices appeared in exclude_index; sample column by column, more efficient when there are more 
    rows than columns in sample_size.

    return elements in source_array of shape sample_size.

    source_array - the source array to sample from
    sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row
    exclude_index - array representing indices should not appear in resulted array, used to exclude current choice from sampling
    prob_array - the array used to weight sample
    """
    
    debug = DebugPrinter(debuglevel)
        
    rows, columns = sample_size
    source_array_size = source_array.size()
    
    if source_array_size <= columns:
        print "There are less indices (%s) in source_array than the sample_size (%s). Sample %s instead." %\
              (source_array_size, columns, source_array_size)
        return ones((rows,source_array_size)) * source_array

    if prob_array is None:
        prob_array = ones(source_array_size)
        
    if not isinstance(prob_array, NumArray):
        raise TypeError, "prob_array must be of type NumArray"

    prob_array_size = nonzerocounts(prob_array)
    if prob_array_size <= columns:
            print "there are less non-zero weight (%s) in prob_array than the sample_size (%s). Sample %s instead. " %\
                  (prob_array_size, columns, prob_array_size)
            return ones((rows,source_array_size)) * source_array

    p_array = prob_array.astype(Float64)

    if sum(p_array) <> 1.0:
        p_array = p_array / sum(p_array)
        debug.print_debug("prob_array doesn't sum up to 1, and is normalized.",5)
    
    prob_sum = cumsum(p_array)

    sampled_choiceset_index = zeros(sample_size) - 1    #initialize output

    if exclude_index is not None:
        if not isinstance(exclude_index, NumArray):            
            try:
                exclude_index = asarray(exclude_index)
            except:
                raise TypeError, "exclude_index must be of type NumArray"
        if exclude_index.shape[0] <> rows:
            raise ValueError, "exclude_index should have the same number of rows as sample_size[0]"
        if rank(exclude_index) == 1:
            exclude_index = exclude_index[:, NewAxis]
        #sampled_choiceset_index = concatenate((exclude_index,sampled_choiceset_index),axis=1)
                  #attach exclude_index to the beginning of sampled_choiceset_index

    for j in range(columns):
        slots_to_be_sampled = arange(rows)
        #proposed_index = zeros((rows,1)) - 1
        while True:
            proposed_index = ProbSampleReplaceL(source_array, slots_to_be_sampled.size(), p_array)
            try:
                exclude_array = exclude_index[slots_to_be_sampled,]
            except:
                exclude_array = None
            duplicate_indicator = find_duplicates_others(proposed_index, exclude_array)
            valid_index = slots_to_be_sampled[duplicate_indicator==0]
            sampled_choiceset_index[valid_index, j] = proposed_index[duplicate_indicator==0]
            if nonzerocounts(duplicate_indicator) == 0:
                break
            
            slots_to_be_sampled = slots_to_be_sampled[duplicate_indicator>0]

        exclude_index = concatenate((exclude_index, take(sampled_choiceset_index,(j,), axis=1)), axis = 1)
        
    return sampled_choiceset_index


def nonzerocounts(source_array):
    return nonzero(source_array)[0].size()

def find_duplicates(src_array):
    """find duplicate values in a list or array
    return a Numarray where nonzero indicates having duplicates, zero indicates none.
    """

    if not isinstance(src_array, NumArray):
        src_array = asarray(src_array)
    if src_array.rank <> 1:
        src_array = src_array.flat
    array_size = src_array.size()
    allsum = zeros(array_size)
    allone = ones(array_size)
    for element in src_array:
        allsum += where(equal(src_array, element), 1, 0)
    duplicate_indicator = allsum - allone

    #dup_idx = nonzero(duplicate_indicator)
    return duplicate_indicator

def find_duplicates_others(source_array, other_array):
    """find indices of duplicate values in src_array against other_array
    src_array - numarray to be checked
    other_array - numarray to be checked againt, must have compatiable shape[0] 
                   with src_array
    """
    
    if other_array is None or len(other_array) == 0:
        return array([])
    
#     if not isinstance(src_array, NumArray):
#         src_array = array(source_array, shape=(:,NewAxis))
#     if not isinstance(other_array, NumArray):       
#         other_array = asarray(other_array)
        
    if other_array.shape[0] <> source_array.shape[0]:
        raise ValueError, "Arrays have incompatible shapes"
    
    if rank(source_array) < rank(other_array):
        src_array = source_array[:, NewAxis]
        oth_array = other_array
    elif rank(source_array) > rank(other_array):
        src_array = source_array
        oth_array = other_array[:, NewAxis]

    is_duplicates = where(equal(src_array, oth_array),1,0)
    duplicate_indicator = sum(is_duplicates, axis=1)

    return duplicate_indicator


# def find_duplicates1d(src_array):
#     """find indices of duplicate values in a list or array"""
    
#     return find_duplicates_self(src_array)

# def find_duplicates2d(src_array, other_array):
#     """find indices of duplicate values in src_array against other_array
#     src_array - numarray to be checked, must be a rank-1 array
#     other_array - numarray to be checked againt, must have compatiable shape[0] 
#                    with src_array
#     """
    
#     return find_duplicates_others(src_array, other_array)

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
        return array([])

    try:
        t = sort(na_array)
    except TypeError:
        del t
        raise RuntimeError, "unable to find unique values for na_array"
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

