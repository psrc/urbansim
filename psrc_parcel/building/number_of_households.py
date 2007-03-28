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
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_households(Variable):
    """Number of households in a given building"""

    _return_type="Int32"
    
    def dependencies(self):
        return [attribute_label("household", "building_id"), \
                my_attribute_label("building_id")]

    def compute(self,  dataset_pool):
        households = dataset_pool.get_dataset("household")
        return self.get_dataset().sum_dataset_over_ids(households, constant=1)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("household").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array, arange
    from numpy import ma
    from opus_core.resources import Resources
    from urbansim.datasets.building_dataset import BuildingDataset
    from urbansim.datasets.household_dataset import HouseholdDataset
    from opus_core.storage_factory import StorageFactory    
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.building.number_of_households"
        def test(self):
#            building_id = array([1, 2, 3, 4])
            
            storage1 = StorageFactory().get_storage('dict_storage')
            hh_table_name = 'households'
            
            storage1.write_dataset(
                Resources({
                    'out_table_name':hh_table_name,
                    'values': {"household_id":arange(1,7), 
                               "building_id": array([1, 2, 3, 4, 2, -1])
                               },
                    })
                )
    
            households = HouseholdDataset(in_storage=storage1, 
                                          in_table_name=hh_table_name)        
            storage2 = StorageFactory().get_storage('dict_storage')
            builing_table_name='building'
            storage2.write_dataset(
                Resources({
                    'out_table_name':builing_table_name,
                    'values': {"building_id":array([1,2,3,4])},
                })
            )

            buildings = BuildingDataset(in_storage=storage2, 
                                        in_table_name=builing_table_name)


            buildings.compute_variables(self.variable_name, 
                                        resources=Resources({'household':households}))
            values = buildings.get_attribute(self.variable_name)
            
            should_be = array([1,2,1,1])
            
            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()