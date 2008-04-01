from numarray import *
from numarray.random_array import randint, seed
import time

def find_duplicates1(checking_set, compared_set=None):
    """check if there are duplicates in numarray checking_set
    
    checking_set - array to be checked, must be a rank-1 array
    compared_set - array to be compared with checking_set,
    either a rank-2 array (the second axis could be 1) or None.
    If it is None, check if checking_set has repeat values
    
    Example:
    n = 9; max = 11
    a = randint(0,max,(n,))  # rank-1 array
    b = randint(0,max,(n,4)) # rank-2 array, which could be b = randint(0,max,(n,1))
    _checking_duplicates(a,b)
    """
    #TODO: if checking_set has more than one dimensions, use its first dimension
    _checking_set = checking_set #[...,0]
    if (compared_set == None): #check if checking_set has duplicate values in itself
        compared_set = ones((checking_set.shape[0],checking_set.shape[0])) * checking_set
        #use e to eliminate value itself from duplicates, which appears at diagonal 
        e = identity(_checking_set.shape[0]) 
    else:
        e = 0  #if compared_to is not None then e = 0
        #TODO: need to make sure the sizes of this two arrays if they are comparable            
    _checking_set = repeat(_checking_set,compared_set.shape[1])
    _checking_set = reshape(_checking_set,(compared_set.shape[0],-1))
    compare = (compared_set == _checking_set) - e
    duplicates = add.reduce(compare,axis=1)        
    return nonzero(duplicates)[0]
    
def find_duplicates2(set_a):
    """find index of duplicate values in a list or array"""
    
    set_a = asarray(set_a)
    set_a = set_a.flat
    
    a0 = zeros(set_a.shape)
    a1 = ones(set_a.shape)
    for a in set_a:
        a0 += where(equal(set_a, a), 1, 0)
    return nonzero(a0-a1)[0]
    
def find_duplicates3(set_a):
    """find index of duplicate values in a list or array"""
    
    set_a = asarray(set_a)
    set_a = set_a.flat
    
    sort_a = sort(set_a)
    reserve_a = argsort(argsort(set_a))
    
    a0 = zeros(set_a.shape)
    a1 = ones(set_a.shape)
    for a in sort_a:
        for i in range(len(sort_a)):
            if sort_a[i] == a:
                a0[i] += 1
            elif sort_a[i] > a:
                break
    a0 = take(a0,reserve_a)
    return nonzero(a0-a1)[0]
        
if __name__ == "__main__":

    seed(1,1)               
    test_num = randint(0,100000,(10000,))

    start_time1 = time.time()
    find1=find_duplicates1(test_num)
    end_time1 = time.time()


    start_time2 = time.time()
    find2=find_duplicates2(test_num)
    end_time2 = time.time()


    start_time3 = time.time()
    find3=find_duplicates3(test_num)
    end_time3 = time.time()

    print "1 Elapsed time = " + str(end_time1 - start_time1)
    print "2 Elapsed time = " + str(end_time2 - start_time2)
    print "3 Elapsed time = " + str(end_time3 - start_time3)
    
    print "test numbers:",test_num
    print find1
    print find2
    print find3
