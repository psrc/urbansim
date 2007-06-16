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

from scipy.ndimage import correlate
from numpy import ma

from opus_core.variables.variable import Variable

class wwd(Variable):
    """Returns function of variable over gridcells within walking distance.
         
    The mode may be any of the "boundary condition" modes supported by
    numpy's correlate function.
    """
    def __init__(self, variable_name, mode='reflect'):
        self.inner_dataset = variable_name.get_dataset_name()
        self.variable_name = variable_name
        self.mode = mode
        Variable.__init__(self)
        
    def dependencies(self):
        return [self.variable_name.get_full_name()]
        
    def compute(self, dataset_pool):
        inner_variable = self.get_dataset().get_2d_attribute(self.variable_name)
        walking_distance_footprint = dataset_pool.get_dataset('urbansim_constant')["walking_distance_footprint"]
        summed = correlate(ma.filled(inner_variable, 0.0),
                           walking_distance_footprint,
                           mode=self.mode)
        return self.get_dataset().flatten_by_id(summed)
    
from opus_core.tests import opus_unittest

from numpy import array

from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    def skip_test_aggregate_sum(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                'attr': array([10,20,30,40]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')

        # Test variable specifying to use sum.
        variable_name = 'urbansim.func.wwd(urbansim.gridcell.attr)'
        gridcell.compute_variables(variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(variable_name)
        
        should_be = array([80, 110, 140, 170])
        self.assert_(ma.allequal(values, should_be), 
                     msg="Error in " + variable_name)
                     

if __name__ == "__main__":
    opus_unittest.main()    