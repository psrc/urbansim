# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


class DatasetPoolConfiguration(object):
    """Provides configuration information for a DatasetPool object."""

    def __init__(self, package_order, package_order_exceptions={}):
        self.package_order = package_order
        if len(package_order_exceptions)>0:
            raise ValueError, "parameter package_order_exceptions is deprecated and shouldn't be used -- tried to pass in a non-empty dictionary to package_order_exceptions"        

from opus_core.tests import opus_unittest


class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_stored_valudes(self):
        expected_package_order = ['a', 'c', 'b']
        dataset_pool_config = DatasetPoolConfiguration(package_order=expected_package_order)
        self.assertEqual(dataset_pool_config.package_order, expected_package_order)
        # try passing in a nonempty package_order_exceptions and make sure it raises an error
        self.assertRaises(ValueError, DatasetPoolConfiguration, expected_package_order, {'pkg': 'gridcell'})
        

if __name__=='__main__':
    opus_unittest.main()