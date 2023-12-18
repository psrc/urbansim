# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os, sys
# from opus_core.tests import opus_unittest
import numpy
from numpy import *
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from opus_core.store.csv_storage import csv_storage
from opus_core import paths

class ManipulateTravelDataTest(object):#(opus_unittest.OpusTestCase):
    """ This test validates the generated xml MATSim configuration while using pyxb's own validation process.
    """
    
    def __init__(self):
        print("Entering setup")
        self.origin_zone_id = 'from_zone_id'
        self.destination_zone_id = 'to_zone_id'
        self.travel_data_attribute = 'single_vehicle_to_work_travel_cost'
        
        # manipulation values
        self.cbd = '129'                                # central business district zone id
        self.preferential_zone = '20' # 20, 100, 110    # zone id of prefered zone
        self.low_travel_cost = '3.47'                   # low travel costs for prefered zone to cbd
        self.high_travel_cost = '1689.19'               # high travel costs for other zones to cbd
        print("Leaving setup")
    
    def test_run(self):
        print("Entering test run")
        
        path = paths.get_opus_home_path('opus_matsim', 'tmp')
        # check if travel data exsits
        travel_data = os.path.join( path, "travel_data.csv" )
        if not os.path.exists(travel_data):
            print("Travel Data not found!!!")
            sys.exit()
        
        in_storage = csv_storage(storage_location = path)
        table_name = "travel_data"
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )
        
        origin_zones = travel_data_set.get_attribute_as_column(self.origin_zone_id)
        l = numpy.atleast_1d(origin_zones).tolist()
        origin_list = set(l) # removes duplicates and sorts the list in ascending order
        # destination_list = len(origin_list) * self.cbd # creates a list that contains the zone id of the cbd an has the same length as "origin_list"

        # set high travel costs for all origin to cbd pairs
        for id in origin_list:
            travel_data_set.set_values_of_one_attribute_with_od_pairs(self.travel_data_attribute, self.high_travel_cost, id, self.cbd)
        # adjust cbd to cbd
        travel_data_set.set_values_of_one_attribute_with_od_pairs(self.travel_data_attribute, 0.0, self.cbd, self.cbd)
        # adjust prefered zone to cbd
        travel_data_set.set_values_of_one_attribute_with_od_pairs(self.travel_data_attribute, self.low_travel_cost, self.preferential_zone, self.cbd)
        
        w = travel_data_set.get_index_by_origin_and_destination_ids(110, 129)
        x = travel_data_set.get_index_by_origin_and_destination_ids(129, 129)
        y = travel_data_set.get_index_by_origin_and_destination_ids(20, 129)
        z = travel_data_set.get_index_by_origin_and_destination_ids(20, 20)
        
        print(w)
        print(x)
        print(y)
        print(z) 
        
        origin_zones = travel_data_set.get_attribute_as_column(self.origin_zone_id)
        destination_zones = travel_data_set.get_attribute_as_column(self.destination_zone_id)
        
        my_travel_data_attr_mat = travel_data_set.get_attribute_as_matrix('travel_data.single_vehicle_to_work_travel_cost', 
                                                                   fill=999)
        my_travel_data_attr_mat[origin_zones, destination_zones] = 1.03
        
        
        
        cbd_ids = where(origin_zones == 129)
        

        print("Leaving test run")
        
if __name__ == "__main__":
    # opus_unittest.main()
    mtd = ManipulateTravelDataTest()
    mtd.test_run()