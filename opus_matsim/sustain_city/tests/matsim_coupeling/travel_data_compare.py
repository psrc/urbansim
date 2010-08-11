# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_core.logger import logger
from opus_core.tests import opus_unittest
from numpy import savetxt, genfromtxt
import opus_matsim.sustain_city.tests as test_path
from opus_core.store.csv_storage import csv_storage
from urbansim.datasets.travel_data_dataset import TravelDataDataset
import tempfile
from shutil import rmtree

class TravelDataCompare(opus_unittest.OpusTestCase):
    """ This test validates the generated xml MATSim configuration while using pyxb's own validation process.
    """
    
    def setUp(self):
        print "Entering setup"
        
        logger.log_status('Executing numpy array comparison tests on MATSim travel data...')
        
        self.travel_data_source_dir = os.path.join(test_path.__path__[0], 'data', 'travel_cost')
        self.travel_data_source = os.path.join(self.travel_data_source_dir, 'travel_data_small.csv')
        if not os.path.exists( self.travel_data_source ):
            raise StandardError('Travel data source not found: %s' % self.travel_data_source)
        
        self.tempDir = tempfile.mkdtemp(prefix='opus_tmp')
        
        print "Leaving setup"

    def tearDown(self):
        print "entering tearDown"
        if os.path.exists(self.tempDir):
            rmtree(self.tempDir)
        print "leaving tearDown"
    
    def test_run(self):
        print "Entering test run"
        
        logger.log_status('Loading travel data: %s' % self.travel_data_source)
        # get travel data as an attribute marix
        in_storage = csv_storage(storage_location = self.travel_data_source_dir)
        table_name = "travel_data"
        travel_data_attribute = 'single_vehicle_to_work_travel_cost'
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )
        travel_data_attribute_mat = travel_data_set.get_attribute_as_matrix(travel_data_attribute, fill=0)
        
        # determine location to store and read attribute matrix
        location1 = os.path.join(self.tempDir, 'attrib_matrix1.txt')
        location2 = os.path.join(self.tempDir, 'attrib_matrix2.txt')
        
        # store attribute matrix
        savetxt( location1 , travel_data_attribute_mat, fmt="%i")
        savetxt( location2 , travel_data_attribute_mat, fmt="%i")
        
        # read attribute matrix
        matrix1 = genfromtxt( location1 )
        matrix2 = genfromtxt( location2 )
        
        # compare both matices
        result = (matrix1 == matrix2)
        
        self.assertTrue(result.all())
        
        print "Leaving test run"
        
if __name__ == "__main__":
    opus_unittest.main()