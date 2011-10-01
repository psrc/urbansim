# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import numpy
from numpy import array, asarray, arange, zeros, ones, concatenate, sum, resize
from numpy import where, equal, ndarray, clip, sort, searchsorted, cumsum
from numpy import float32, float64, newaxis, rank, take, ma, argmax
from numpy import logical_not
from opus_core.misc import ncumsum, is_masked_array, unique, ismember
from opus_core.logger import logger
from numpy.random import uniform, randint

def sample_replace(source_array, size, return_index=False):
    """Equal probability sampling; with-replacement case
    if return_index is True, return indices to source_array,
    otherwise, return elements in source_array
    """
    min = 0; max = source_array.size
    if return_index:
        return randint(min,max,size)
    else:
        return source_array[randint(min,max,size)]

def sample_noreplace(source_array, size, return_index=False):
    """equal probability sampling; without replacement case.
    Using numpy functions, efficient for large array"""
    if not isinstance(source_array, ndarray):
        try:
            source_array = asarray(source_array)
        except:
            raise TypeError, "source_array must be of type ndarray"
    
    n = source_array.size
    if n == 0:
        if return_index:
            return array([], dtype='i')
        else:
            return array([], dtype=source_array.dtype)
    prob_array = resize(array([1.0/n], dtype = float32), n)  #fake a equal probability array to use probsample_noreplace
    return probsample_noreplace(source_array, size, prob_array, return_index=return_index)

def probsample_replace(source_array, size, prob_array, return_index=False):
    """Unequal probability sampling; with replacement case.
    Using numpy searchsorted function, suitable for large array"""
    if not isinstance(source_array, ndarray):
        try:
            source_array = asarray(source_array)
        except:
            raise TypeError, "source_array must be of type ndarray"

    if prob_array is None:
        return sample_replace(source_array,size, return_index=return_index)

    if prob_array.sum() == 0:
        raise ValueError, "there aren't non-zero weights in prob_array"

    cum_prob = cumsum(prob_array, dtype='float64')

    sample_prob = uniform(0, cum_prob[-1], size)
    sampled_index = searchsorted(cum_prob, sample_prob)
    sampled_index = sampled_index.astype('int32')
    # due to precision problems, searchsorted could return index = cum_prob.size
    sampled_index = clip(sampled_index, 0, cum_prob.size-1) 
    
    if return_index:
        return sampled_index
    else:
        return source_array[sampled_index]

def probsample_noreplace(source_array, sample_size, prob_array=None,
                         exclude_element=None, exclude_index=None, return_index=False):
    """generate non-repeat random 1d samples from source_array of sample_size, excluding
    indices appeared in exclude_index.

    return indices to source_array if return_index is true.

    source_array - the source array to sample from
    sample_size - scalar representing the sample size
    prob_array - the array used to weight sample
    exclude_element - array representing elements should not appear in resulted array
    exclude_index - array representing indices should not appear in resulted array,
                    which can be used, for example, to exclude current choice from sampling,
                    indexed to source_array
    """
    if sample_size <= 0:
        #logger.log_warning("sample_size is %s. Nothing is sampled." % sample_size)
        if return_index:
            return array([], dtype='i')
        else:
            return array([], dtype=source_array.dtype)
            
    if prob_array is None:
        return sample_replace(source_array,sample_size, return_index=return_index)
    else:
        #make a copy of prob_array so we won't change its original value in the sampling process
        prob_array2 = prob_array.copy()
        if exclude_element is not None:
            prob_array2[ismember(source_array, exclude_element)] = 0.0
            
        if exclude_index is not None:
            index_range = arange(source_array.size, dtype="i")
            if isinstance(exclude_index, numpy.ndarray):
                exclude_index = exclude_index[ismember(exclude_index, index_range)]
                prob_array2[exclude_index] = 0.0
            elif (exclude_index in index_range):
                prob_array2[exclude_index] = 0.0
        
        nzc = nonzerocounts(prob_array2)
        if nzc == 0:
            raise ValueError, "The weight array contains no non-zero elements. Check the weight used for sampling."
        if nzc < sample_size:
            logger.log_warning("The weight array contains %s non-zero elements, less than the sample_size %s. Use probsample_replace. " %
                  (nzc, sample_size))
            #sample_size = max
            return probsample_replace(source_array, sample_size, prob_array=prob_array2, return_index=return_index)
        elif nzc == sample_size:
            nonzeroindex = prob_array2.nonzero()[0]
            if return_index:
                return nonzeroindex
            else:
                return source_array[nonzeroindex]

    to_be_sampled = sample_size
    sampled_index = array([], dtype='i')  #initialize sampled_index
    while True:
        proposed_index = probsample_replace(source_array, to_be_sampled, prob_array2, return_index=True)
        valid_index = unique(proposed_index, return_index=False)
        #assert all( logical_not(ismember(valid_index, sampled_index)) )
        #valid_index = valid_index[logical_not(ismember(valid_index, sampled_index))]  #this should not be necessary because we control the prob_array        
        sampled_index = concatenate((sampled_index, valid_index))
        
        to_be_sampled -= valid_index.size
        if to_be_sampled == 0:
            if return_index:
                return sampled_index
            else:
                return source_array[sampled_index]

        prob_array2[proposed_index] = 0.0
        nzc = nonzerocounts(prob_array2)
        assert nzc > 0 #given that we have checked and made sure nonzerocounts(prob_array2)>size, it should not run out before we have enough non-repeat samples
        
def stratifiedsample(source_array, strata_array,
                     sample_size=1,
                     sample_rate=None, min_size=1,
                     weight_array=None, replace=False,
                     return_index=False):
    """stratified sampling from source_array,

    min_size works with sampling_rate,
    sample max(min_size, sample_rate * number of items in a stratum) from each stratum
    """

    sampled_index = array([], dtype='int32')
    unique_strata = unique(strata_array)
    for this_stratum in unique_strata:
        indices_in_stratum = where(equal(strata_array, this_stratum))[0]
        counts = len(indices_in_stratum)

        if sample_rate is not None:
            stratum_sample_size = max(min_size, int(round(counts * sample_rate)))
        else:
            stratum_sample_size = sample_size

        if counts < stratum_sample_size:
            logger.log_warning( "Warning: there are less counts(%s) than sample_size %s for stratum %s. sample %s instead"
             % (counts, stratum_sample_size, this_stratum, counts))
            stratum_sample_size = counts

        if weight_array is not None:
            stratum_weight_array = weight_array[indices_in_stratum].astype(float32)
            if sum(stratum_weight_array) == 0.0:
                logger.log_warning("Warning: the weight_array for stratum %s are all zeros; it is skipped."
                                       % (this_stratum))
                continue

            prob_array = normalize(stratum_weight_array)
            prob_array_size = nonzerocounts(prob_array)
            if stratum_sample_size > prob_array_size:
                if not replace:
                    logger.log_warning("Warning: there are less non-zero entries(%s) in weight_array than sample_size(%s) for stratum %s; sample with replacement"
                     % (prob_array_size, stratum_sample_size, this_stratum))
                    replace=True
        else:
            stratum_weight_array = None
            prob_array = None

        #logger.log_status(this_stratum, stratum_sample_size)
        if stratum_sample_size > 0:
            if not replace:
                sampled_index = concatenate(
                                        (sampled_index,
                                         probsample_noreplace(indices_in_stratum, stratum_sample_size, prob_array)
                                         ))
            else:
                sampled_index = concatenate(
                                        (sampled_index,
                                         probsample_replace(indices_in_stratum, stratum_sample_size, prob_array)
                                         ))
    if return_index:
        return sampled_index
    else:
        return source_array[sampled_index]

def prob2dsample(source_array, sample_size, prob_array=None, exclude_index=None,
                  replace=False, return_index=False):
    """generate non-repeat random 2d samples from source_array of sample_size, not including
    indices appeared in exclude_index; sample column by column, more efficient when there are more
    rows than columns in sample_size.

    return elements in source_array of shape sample_size.

    source_array - the source array to sample from
    sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row
    exclude_index - array representing indices should not appear in resulted array, used to exclude current choice from sampling
    prob_array - the array used to weight sample
    """

    rows, columns = sample_size
    source_array_size = source_array.size

    if source_array_size <= columns and not replace:
        logger.log_warning("There are less or equal indices (%s) in source_array than the sample_size (%s). Sample %s." %
              (source_array_size, columns, source_array_size))

        if return_index:
            return ones((rows,1), dtype='i') * arange(source_array_size)[newaxis,:]
        else:
            return ones((rows,1), dtype='i') * source_array[newaxis,:]
            

    if prob_array is None:
        prob_array = ones(source_array_size)

    if not (isinstance(prob_array, ndarray) or is_masked_array(prob_array)):
        raise TypeError, "prob_array must be of type ndarray"

#    prob_array_size = nonzerocounts(prob_array)
#    if prob_array_size <= columns:
#            logger.log_warning( "there are less or equal non-zero weight (%s) in prob_array than the sample_size (%s). Sample %s instead. " %\
#                  (prob_array_size, columns, prob_array_size))
#            return ones((rows,1)) * source_array[nonzero(prob_array)][newaxis,:]

    p_array = prob_array

    p_array_sum = p_array.sum(dtype="float64")
    if not ma.allclose(p_array_sum, 1.0):
        if abs(1.0 - p_array_sum) > 0.01:
            # print this message only if it is a serious difference
            logger.log_warning("prob_array doesn't sum up to 1, and is normalized. Sum: %s" % p_array_sum)
        p_array = p_array / p_array_sum

    cum_prob = ncumsum(p_array)

    sampled_choiceset_index = zeros(sample_size, dtype="int32") - 1    #initialize output

    if not replace:
        if exclude_index is not None:
            if not isinstance(exclude_index, ndarray):
                try:
                    exclude_index = asarray(exclude_index)
                except:
                    raise TypeError, "exclude_index must be of type ndarray"
            if exclude_index.shape[0] <> rows:
                raise ValueError, "exclude_index should have the same number of rows as sample_size[0]"
            if rank(exclude_index) == 1:
                exclude_index = exclude_index[:, newaxis]
            #sampled_choiceset_index = concatenate((exclude_index,sampled_choiceset_index),axis=1)
                      #attach exclude_index to the beginning of sampled_choiceset_index
        else:
            exclude_index = zeros(shape=(sample_size[0],1), dtype="int32")

        for j in range(columns):
            slots_to_be_sampled = arange(rows)
            #proposed_index = zeros((rows,1)) - 1
            while True:
                proposed_index = probsample_replace(arange(source_array_size), slots_to_be_sampled.size, p_array)
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
    else:
        for j in range(columns):
            sampled_choiceset_index[:,j] = probsample_replace(arange(source_array_size), rows, p_array)

    if return_index:
        return sampled_choiceset_index
    else:
        return source_array[sampled_choiceset_index]


def sample_choice(prob_array, method="MC"):
    """sample chosen index given probability in prob_array
    prob_array - 2-d array for probability of being chosen, with probablities for a agent at
                 one row, and probabilities for alternatives at columns
    method - the method used to sample choice, either MC (Monte Carlo) or max_prob
    """

    if prob_array.ndim <> 2:
        raise RuntimeError, "prob_array must be a 2d array"

    rows, columns = prob_array.shape
    sum_prob_by_col = sum(prob_array, axis=1, dtype=float64)
    if not ma.allclose(sum_prob_by_col, ones((rows,))):
        strange_rows = where(sum_prob_by_col != ones((rows,)))
        raise RuntimeError, "prob_array must add up to 1 for each row. Abnormal rows: %s" % prob_array[strange_rows,:] 
    

    if method.lower() == "mc":
        cum_prob = ncumsum(prob_array, axis=1)

        R = uniform(0,1,rows)
        R.resize((rows,1))

        match = (R < cum_prob)
        choices = argmax(match, axis=1)   # return the first index of 1 in each row
    elif method.lower() == "max_prob":
        choices = argmax(prob_array)

    if choices.size <> rows:
        raise RuntimeError, "having problems sample choice"

    return (arange(rows), choices)

def find_duplicates(source_array):
    """find duplicate values in a list or array
    return a numpy array of the same shape as source_array
    where nonzero indicates having duplicates, zero indicates none.
    """

    if not isinstance(source_array, ndarray):
        source_array = asarray(source_array)
    if source_array.ndim <> 1:
        source_array = source_array.ravel()
    array_size = source_array.size
    allsum = zeros(array_size, dtype="int32")
    allone = ones(array_size, dtype="int32")
    for element in source_array:
        allsum += equal(source_array, element)
    duplicate_indicator = allsum - allone

    #dup_idx = nonzero(duplicate_indicator)
    return duplicate_indicator

def find_duplicates_others(source_array, other_array):
    """find indices of duplicate values in src_array against other_array
    source_array - numpy array to be checked
    other_array - numpy array to be checked againt, must have compatiable shape[0]
                   with src_array
    """

    if other_array is None or len(other_array) == 0:
        return zeros(source_array.shape, dtype="int32")

    if other_array.shape[0] <> source_array.shape[0]:
        raise ValueError, "Arrays have incompatible shapes"
    source_array_rank = rank(source_array)
    if rank(source_array) < rank(other_array):
        src_array = source_array[:, newaxis]
        oth_array = other_array
    elif rank(source_array) > rank(other_array):
        src_array = source_array
        oth_array = other_array[:, newaxis]

    is_duplicates = equal(src_array, oth_array)
    duplicate_indicator = sum(is_duplicates, axis=1)

#    if duplicate_indicator.ndim > source_array_rank:
#        reshape(duplicate_indicator, shape=(src_array.size,))
    return duplicate_indicator

def normalize(weight_array):
    """Normalize a weight_array of either 1 or 2 dimensions"""

    prob_array = None

    if weight_array is None:
        return prob_array

    # dimensions of weight array
    try:
        d = weight_array.ndim
    except:
        d = 0

    lt0_index = weight_array < 0
    if lt0_index.sum() > 0:
        raise ValueError, "some values of rows %s in weight_array are less than 0" % where(lt0_index)[0]

    if d > 2:
        raise ValueError, "Can't handle a weight_array with more than 2d"
    elif d == 2:
        weight_array_sum = sum(weight_array, axis=1, dtype=float32)[:, newaxis]
        zero_index = weight_array_sum<=0
        if zero_index.sum() > 0:
            logger.log_warning("Rows %s of weight_array sum to 0 or less" % where(zero_index)[0])
            prob_array = ma.filled( weight_array/ma.masked_where(weight_array_sum<=0, weight_array_sum), 0.0)
        else:
            prob_array = weight_array/weight_array_sum
    elif d == 1:
        weight_array_sum = weight_array.sum()
        if weight_array_sum > 0:
            prob_array = weight_array / float(weight_array_sum)
        else:
            logger.log_warning("weight_array sums to 0 or less")
            prob_array = weight_array * 0
    else:
        raise ValueError, "Can't handle this weight_array"

    return prob_array

def nonzerocounts(source_array):
    """return counts of nonzero elements in source_array"""
    return source_array.nonzero()[0].size
