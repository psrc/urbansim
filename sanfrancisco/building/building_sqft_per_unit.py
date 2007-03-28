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
from numpy.ma import masked_where, filled
from numpy import Float32

class building_sqft_per_unit(Variable):
    """ (building_sqft) / residential_units."""
    
    building_sqft = "building_sqft"
    residential_units = "residential_units"
    
    def dependencies(self):
        return [my_attribute_label(self.building_sqft), \
                my_attribute_label(self.residential_units)]
        
    def compute(self,  dataset_pool):
        buildings = self.get_dataset()
        residential_units = buildings.get_attribute(self.residential_units)
        return filled(buildings.get_attribute(self.building_sqft) / \
                      masked_where(residential_units==0, residential_units.astype(Float32)), 0.0)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
        
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy.ma import allclose
    from opus_core.resources import Resources    
    from sanfrancisco.datasets.building_dataset import BuildingDataset
    from opus_core.storage_factory import StorageFactory
    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.building.building_sqft_per_unit"

        def test_my_inputs(self):
            storage2 = StorageFactory().get_storage('dict_storage')
            building_table_name='building'
            storage2.write_dataset(
                Resources({
                    'out_table_name':building_table_name,
                    'values': {"building_id":array([1,2,3,4,5]),
                               "residential_units":array([2,0,1,4,7]),
                               "building_sqft":array([1000,0,2000,1000,7000]),
                               },
                })
            )

            buildings = BuildingDataset(in_storage=storage2, 
                                        in_table_name=building_table_name)

            buildings.compute_variables(self.variable_name)
            values = buildings.get_attribute(self.variable_name)

            should_be = array([500, 0, 2000, 250, 1000])
            
            self.assertEqual(allclose(values, should_be), \
                             True, msg = "Error in " + self.variable_name)
            
    unittest.main()