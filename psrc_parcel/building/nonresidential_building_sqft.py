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
from urbansim.functions import attribute_label
from numarray import zeros, where

class nonresidential_building_sqft(Variable):
    """total building_sqft in nonresidential class. """
   
    def dependencies(self):
        return [my_attribute_label("building_class_id"), 
                attribute_label("building_use", "class_id"),
                "psrc_parcel.building_use.class_name"]
        
    def compute(self,  dataset_pool):
        building_use = dataset_pool.get_dataset("building_use")
        building_class_ids = building_use.get_attribute("class_id")[
             where(building_use.get_attribute("class_name") == "nonresidential")
            ]
        buildings = self.get_dataset()
        building_sqft = buildings.get_attribute("building_sqft")
        results = zeros(buildings.size())
        for class_id in building_class_ids:
            index = buildings.get_attribute("building_class_id") == class_id
            results[index] = building_sqft[index]
        return results
    
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array, arange
    from numarray.ma import allclose
    from opus_core.resources import Resources
    from urbansim.datasets.building_dataset import BuildingDataset
    from psrc_parcel.datasets.building_use_classification_dataset import BuildingUseClassificationDataset
    from opus_core.storage_factory import StorageFactory
    import numarray.strings as strarray
    
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.building.nonresidential_building_sqft"
        def test(self):
#            building_id = array([1, 2, 3, 4])
            
            storage1 = StorageFactory().get_storage('dict_storage')
            table1 = 'building_use'
            
            storage1.write_dataset(
                Resources({
                    'out_table_name':table1,
                    'values': {"class_id":array([1,2]), 
                               "class_name": strarray.array(["nonresidential","residential"])
                               },
                    })
                )
    
            building_uses = BuildingUseClassificationDataset(in_storage=storage1, 
                                                          in_table_name=table1)        
            storage2 = StorageFactory().get_storage('dict_storage')
            builing_table_name='building'
            storage2.write_dataset(
                Resources({
                    'out_table_name':builing_table_name,
                    'values': {"building_id":array([1,2,3,4]),
                               "building_class_id":array([1,1,2,1]),
                               "building_sqft":array([0, 100, 70, 29])},
                })
            )

            buildings = BuildingDataset(in_storage=storage2, 
                                        in_table_name=builing_table_name)


            buildings.compute_variables(self.variable_name, 
                                        resources=Resources({'building_use':building_uses}))
            values = buildings.get_attribute(self.variable_name)
            
            should_be = array([0,100,0,29])
            
            self.assertEqual(allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()