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
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class TravelDataDataset(UrbansimDataset):
    """Set of travel data logsums."""

    id_name_default = ["from_zone_id", "to_zone_id"]
    in_table_name_default = "travel_data"
    out_table_name_default = "travel_data"
    dataset_name = "travel_data"
    
    def number_of_logsums(self):
        """Return the number of logsums in this travel data set"""
        n = 0
        # use self.get_primary_attribute_names() so that we count the logsums whether or not they have been loaded already
        for name in self.get_primary_attribute_names():
            if name.startswith("logsum"): 
                n=n+1
        return n
        


from opus_core.tests import opus_unittest
from numpy import array, ma
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
        
    def test_travel_data(self):
        # create a simple travel data set and check one attribute
        storage = StorageFactory().get_storage('dict_storage')

        travel_data_table_name = 'travel_data'        
        storage.write_table(
                table_name=travel_data_table_name,
                table_data={
                    "from_zone_id": array([1,1,2,2]),
                    "to_zone_id": array([1,2,1,2]),
                    "logsum0": array([-3.0, -6.0, -9.0, -12.0]),
                    "logsum1": array([-4.0, -7.0, -10.0, -13]),
                    "logsum2": array([-5.0, -8.0, -11.0, -14.0])          
                    }
            )

        travel_data = TravelDataDataset(in_storage=storage, in_table_name=travel_data_table_name)
        
        travel_data.load_dataset(attributes='*')
        
        self.assertNotEqual(travel_data.size(), 0, msg = "No data loaded - expected data to be loaded at this point.")
        
        k = len(travel_data.get_attribute_names())
        self.assertEqual(k, 5, msg = "Number of attributes should be 5 but is " + str(k) + ".")
        
        k = len(travel_data.get_primary_attribute_names())
        self.assertEqual(k, 5, msg = "Number of stored attributes should be 5 but is " + str(k) + ".")
        
        n = travel_data.number_of_logsums()
        self.assertEqual(n, 3, msg = "Number of logsums should be 3 but is " + str(k) + ".")
        
        results = travel_data.get_attribute('logsum0')
        
        should_be = array([-3.0, -6.0, -9.0, -12.0])       
        
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-7), True, 
                          msg = "query results should be %s but is %s." % (should_be, results))
 
                    

if __name__=="__main__":
    opus_unittest.main()
    

        