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
# 

import unittest

import pp
import time
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.misc import unique_values
from numpy import arange, resize

class ParallelPythonTest(unittest.TestCase):

    def setUp(self):
        # tuple of all parallel python servers to connect with
        self.ppservers = ()
        #ppservers = ("10.0.0.1",)

    def xtest_sample(self):

        def mysamplefunc(arr):
            sample_noreplace(arr, arr.size/10)
            return unique_values(arr)
        
        l = resize(arange(100), (100,100000))
        nthreads = 2
        # Creates jobserver with ncpus workers
        job_server = pp.Server(nthreads, ppservers=self.ppservers)

        start= time.time()
        jobs = [(input, job_server.submit(mysamplefunc,(input,), (sample_noreplace,unique_values), ())) for input in l]

        print "\n%s threads: %s" % (nthreads, time.time()-start)
        #print result
        start= time.time()
        for i in l:
            mysamplefunc(i)
        print "sequential: %s" % (time.time()-start)


if __name__=='__main__':
    unittest.main()
