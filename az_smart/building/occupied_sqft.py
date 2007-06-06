#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class occupied_sqft(Variable):
    """Number of households in a given parcel"""

    _return_type="int32"
    
    def dependencies(self):
        return ["az_smart.business.building_id", 
                "az_smart.business.sqft", 
                my_attribute_label("building_id")]

    def compute(self,  dataset_pool):
        businesses = dataset_pool.get_dataset("business")
        return self.get_dataset().sum_dataset_over_ids(businesses, "sqft")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("business").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources
    from az_smart.datasets.building_dataset import BuildingDataset
    from az_smart.datasets.business_dataset import BusinessDataset
    from opus_core.storage_factory import StorageFactory   
    
    class Tests(unittest.TestCase):
        variable_name = "az_smart.building.occupied_sqft"
        def test(self):
            storage = StorageFactory().get_storage('dict_storage')
            bs_table_name = 'business'
            
            storage.write_table(
                    table_name=bs_table_name,
                    table_data={"business_id": array([1,2,3,4,5,6]),
                               "sqft":        array([0,1,4,0,2,5]),
                               "building_id": array([2,1,3,2,1,2])
                               },
                )
    
            bs = BusinessDataset(in_storage=storage, 
                                          in_table_name=bs_table_name)

            storage = StorageFactory().get_storage('dict_storage')
            building_table_name='building'
            storage.write_table(
                    table_name=building_table_name,
                    table_data={"building_id": array([1,2,3]),},
            )

            buildings = BuildingDataset(in_storage=storage, 
                                        in_table_name=building_table_name)
            
            buildings.compute_variables(self.variable_name, 
                                        resources=Resources({'business':bs}))
            values = buildings.get_attribute(self.variable_name)
            should_be = array([3,5,4])
            
            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()