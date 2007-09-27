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

import handythread
import time
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.misc import unique_values
from numpy import arange, resize

class HandythreadTest(unittest.TestCase):
    def test_coverage(self):
        d = {}
        l = range(100)
        def f(x):
            d[x]=x**2
        handythread.foreach(f, l)
        for i in l:
            self.assertEqual(d[i],i**2)

    def test_sample(self):
        def f(arr):
            sample_noreplace(arr, arr.size/10)
            return unique_values(arr)

        l = resize(arange(100), (100,100000))
        nthreads = 2
        start= time.time()
        result = handythread.foreach(f, l, nthreads, return_=True)
        print "\n%s threads: %s" % (nthreads, time.time()-start)
        #print result
        start= time.time()
        for i in l:
            f(i)
        print "sequential: %s" % (time.time()-start)

        
    def test_return(self):
        l = range(100)
        r = handythread.foreach(lambda x: x**2, l, return_=True)
        for i in range(len(l)):
            self.assertEqual(l[i]**2,r[i])

    def test_parallel_map(self):
        l = range(100)
        r = handythread.parallel_map(lambda x: x**2, l)
        for i in range(len(l)):
            self.assertEqual(l[i]**2,r[i])


if __name__=='__main__':
    unittest.main()
