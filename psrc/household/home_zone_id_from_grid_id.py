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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class home_zone_id_from_grid_id(Variable):
    """The zone_id of household's home."""
    
    def dependencies(self):
        return [my_attribute_label("grid_id"), 
                attribute_label("gridcell", "zone_id")]
        
    def compute(self, dataset_pool):
        gridcells = dataset_pool.get_dataset('gridcell')
        return self.get_dataset().get_join_data(gridcells, name="zone_id")
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.home_zone_id_from_grid_id"
    
    def test_my_inputs(self):
        zone_id = array([2,1,3])
        grid_id = array([1,1,2,3])

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"household":{ \
                "grid_id":array([2, 1, 3, 4])}, \
             "gridcell":{
                "grid_id":array([1,2,3,4]),
                "zone_id":array([1,1,3,2])
                         }
             }, 
            dataset = "household")
        should_be = array([1, 1, 3, 2])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()