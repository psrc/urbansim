#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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


class DatasetPoolConfiguration(object):
    """Provides configuration information for a DatasetPool object."""

    def __init__(self, package_order, package_order_exceptions):
        self.package_order = package_order
        self.package_order_exceptions = package_order_exceptions
        

from opus_core.tests import opus_unittest


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_stored_valudes(self):
        expected_package_order = ['a', 'c', 'b']
        expected_package_order_exceptions = {'dataset_1':'d', 
                               'dataset_2':'b'}
        dataset_pool_config = DatasetPoolConfiguration(
            package_order=expected_package_order,
            package_order_exceptions=expected_package_order_exceptions
            )
            
        self.assertEqual(dataset_pool_config.package_order, 
            expected_package_order)
            
        self.assertEqual(dataset_pool_config.package_order_exceptions,
            expected_package_order_exceptions)
        

if __name__=='__main__':
    opus_unittest.main()