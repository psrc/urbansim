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

from opus_core.variable import Variable
from variable_functions import my_attribute_label

class occupied_sqft(Variable):
    """Number of households in a given parcel"""

    _return_type="Int32"
    
    def dependencies(self):
        return ["sanfrancisco.business.building_id", 
                "sanfrancisco.business.sqft", 
                my_attribute_label("building_id")]

    def compute(self,  dataset_pool):
        businesses = dataset_pool.get_dataset("business")
        return self.get_dataset().sum_dataset_over_ids(businesses, "sqft")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("business").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from sanfrancisco.datasets.building_dataset import BuildingDataset
    from sanfrancisco.datasets.business_dataset import BusinessDataset
    from opus_core.storage_factory import StorageFactory   
    
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.building.occupied_sqft"
        def test(self):
            storage1 = StorageFactory().get_storage('dict_storage')
            bs_table_name = 'business'
            
            storage1.write_dataset(
                Resources({
                    'out_table_name':bs_table_name,
                    'values': {"business_id": array([1,2,3,4,5,6]),
                               "sqft":        array([0,1,4,0,2,5]),
                               "building_id": array([2,1,3,2,1,2])
                               },
                    })
                )
    
            bs = BusinessDataset(in_storage=storage1, 
                                          in_table_name=bs_table_name)

            storage2 = StorageFactory().get_storage('dict_storage')
            building_table_name='building'
            storage2.write_dataset(
                Resources({
                    'out_table_name':building_table_name,
                    'values':{"building_id": array([1,2,3]),},
                })
            )

            buildings = BuildingDataset(in_storage=storage2, 
                                        in_table_name=building_table_name)
            
            buildings.compute_variables(self.variable_name, 
                                        resources=Resources({'business':bs}))
            values = buildings.get_attribute(self.variable_name)
            should_be = array([3,5,4])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()