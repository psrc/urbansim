#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import pp
from numpy import array

class ParallelManager:
    def __init__(self, ncpus="autodetect", servers=(), secret=None):
        self.parallel_server = pp.Server(ncpus=ncpus, ppservers=servers, secret=secret)
        
    def run_parallel(self, function, inputs, args=(), depfuncs=(), modules=(), return_as_numpy=True):
        # submit jobs
        jobs = [self.parallel_server.submit(function,(input,) + args, depfuncs=depfuncs, modules=modules) for input in inputs]
        result = [job() for job in jobs]
        #print result
        if return_as_numpy:
            return array(result)
        return result
    
from opus_core.tests import opus_unittest
from opus_core.misc import unique_values
from numpy import arange, resize, array, zeros
import time

class ParallelManagerTest(opus_unittest.OpusTestCase):
    def xtest_pp_manager_sample(self):

        def mysamplefunc(arr):
            a = sample_noreplace(arr, arr.size/10)
            return unique_values(a)
        
        ncpus = 2
        manager = ParallelManager(ncpus=ncpus)
        l = resize(arange(100), (10,10000))

        start= time.time()
        results = manager.run_parallel(mysamplefunc, l, depfuncs=(sample_noreplace,unique_values))
        print "test_pp_manager_sample on %s cpus: %s" % (ncpus, time.time()-start)
        #print result
        start= time.time()
        result = zeros((10,100))
        for i in xrange(l.shape[0]):
            result[i,:] = mysamplefunc(l[i,:])
        print "test_pp_manager_sample sequential: %s" % (time.time()-start)

def sample_noreplace(source_array, size, return_indices=False):
    """taken from opus_core.sampling_toolbox. Required imports are added here."""
    from numpy import resize, array, float32
    from opus_core.sampling_toolbox import probsample_noreplace
    n = source_array.size
    if n == 0:
        return source_array
    prob_array = resize(array([1.0/n], dtype = float32), n)  #fake a equal probability array to use probsample_noreplace
    return probsample_noreplace(source_array, size, prob_array, return_indices=return_indices)

if __name__ == "__main__":
    opus_unittest.main()