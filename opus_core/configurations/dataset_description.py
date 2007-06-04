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

from opus_core.configurations.abstract_configuration import AbstractConfiguration
from enthought.traits import Int, Str
import os

class DatasetDescription(AbstractConfiguration):
    """Description of a dataset using traits.  dataset_name is the name of the dataset 
    (e.g. 'gridcell'), package_name is the name of the package in which it is defined
    (e.g. 'opus_core'), and nchunks is the number of chunks in which the dataset's attributes
    are read.  The default number of chunks is 1; use more if necessary to reduce memory usage.
    """
    dataset_name = Str
    package_name = Str
    nchunks = Int
    
    def __init__(self, dataset_name, package_name='opus_core', nchunks=1):
        self.dataset_name = dataset_name
        self.package_name = package_name
        self.nchunks = nchunks
        
    def __eq__(self, other):
        return (isinstance(other,DatasetDescription)
            and self.dataset_name == other.dataset_name
            and self.package_name == other.package_name
            and self.nchunks == other.nchunks)
        
    def __str__(self):
        """return a human-readable description of the dataset"""
        if self.nchunks>1:
            return self.package_name + '.' + self.dataset_name + ' (' + str(self.nchunks) + ' chunks)'
        else:
            return self.package_name + '.' + self.dataset_name
        
    # compatability method - add myself to dictionary for old-style configurations 
    # that represents the data in this configuration. 
    def add_to_dictionary(self,d):
        p = {'package_name': self.package_name}
        if self.nchunks>1:
            p['nchunks'] = self.nchunks
        d[self.dataset_name] = p

from opus_core.tests import opus_unittest
class DatasetDescriptionTests(opus_unittest.OpusTestCase):
    def test_traits(self):
            c = DatasetDescription('jobs', 'chicago.suburbs')
            self.assertEqual(str(c), 'chicago.suburbs.jobs')
            # test __eq__
            c2 = DatasetDescription('jobs', 'chicago.suburbs')
            self.assertEqual(c,c2)
            d = DatasetDescription('jobs', 'chicago.suburbs', 3)
            self.assertEqual(str(d), 'chicago.suburbs.jobs (3 chunks)')
            self.assertNotEqual(c,d)
            testdict = {}
            d.add_to_dictionary(testdict)
            self.assertEqual(testdict, {'jobs': {'package_name': 'chicago.suburbs', 'nchunks': 3}} )

if __name__=='__main__':
    opus_unittest.main()

