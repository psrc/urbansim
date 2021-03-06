# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
import opus_matsim.tests as test_dir
from opus_core.tests import opus_unittest
from opus_core.store.csv_storage import csv_storage
from urbansim.datasets.travel_data_dataset import TravelDataDataset
import numpy
from opus_core.logger import logger
from opus_core import paths

class MatrixTest(opus_unittest.OpusTestCase):
    """ Testing import of MATSim travel data into UrbanSim
    """

    def setUp(self):
        print "Entering setup"
        # get sensitivity test path
        self.test_dir_path = test_dir.__path__[0]
        # get location to travel data table
        self.input_directory = os.path.join( self.test_dir_path, 'testdata')
        logger.log_status("input_directory: %s" % self.input_directory)
        # check source file
        if not os.path.exists( self.input_directory ):
            raise('File not found! %s' % self.input_directory)
        
        print "Leaving setup"
    
    def test_run(self):
        print "Entering test run"
        
        # This test checks if the pre-computed MATSim travel data 
        # is loaded correctly into UrbanSim. Therefore the UrbanSim
        # travel data matrix is converted into a numpy array and two 
        # predefined values are checked whether they match with MATSim data.
        #
        # Here an example:
        # my_list = [[1,2,3],
        #           [4,5,6],
        #           [7,8,9]]
        #
        # my_list[0][1] should be = 2
        # my_list[2][2] should be = 9
        
        table_name = 'travel_data'
        travel_data_attribute = 'single_vehicle_to_work_travel_cost'
        # location of pre-calculated MATSim travel costs
        in_storage = csv_storage(storage_location = self.input_directory)
        # create travel data set (travel costs)
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )
        travel_data_attribute_mat = travel_data_set.get_attribute_as_matrix(travel_data_attribute, fill=31)
        
        # converting from numpy array into a 2d list
        travel_list = numpy.atleast_2d(travel_data_attribute_mat).tolist()
        
        # get two values for validation
        value1 = int(travel_list[1][1]) # should be = 0
        value2 = int(travel_list[2][1]) # should be = 120
        
        logger.log_status('First validation value should be 0. Current value is %i' % value1)
        logger.log_status('Second validation value should be 120. Current value is %i' % value2)
        
        self.assertTrue( value1 == 0 )
        self.assertTrue( value2 == 120 )
            
        # self.dump_travel_list(travel_list) # for debugging
        
        print "Leaving test run"
        
    def dump_travel_list(self, travel_list):
        ''' Dumping travel_list for debugging reasons...
        '''
        
        dest = paths.get_opus_home_path( 'opus_matsim', 'tmp')
        if not os.path.exists(dest):
            os.makedirs(dest)
                
        travel = os.path.join(dest, 'travelFile.txt')
        f = open(travel, "w")
        f.write( str(travel_list) )
        f.close()
        
if __name__ == "__main__":
    #mt = MatrixTest() # for debugging
    #mt.test_run()     # for debugging
    opus_unittest.main()