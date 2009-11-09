# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import unique_values
from numpy import sqrt, arange, array, logical_or
from numpy import ma
from opus_core.logger import logger

class euclidean_distance_from_home_to_work(Variable):
    """euclidean distance from home to work, calculated from 
    the relative_x and relative_y of home and workplace gridcell,
    in the same unit of gridcell.
    """
    
    default_value = 999999
    agent_grid_id = "grid_id = person.disaggregate(urbansim_parcel.household.grid_id)"
    location_grid_id = "urbansim_parcel.job.grid_id"
    
    def dependencies(self):
        return [ self.agent_grid_id, self.location_grid_id,
                 "gridcell.relative_x", "gridcell.relative_y", 
                 #"urbansim_constant.cell_size",
             ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        gridcells = dataset_pool.get_dataset('gridcell')
        constants = dataset_pool.get_dataset('urbansim_constant')
        home_grid_id = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_grid_id,
                                                                                 interaction_dataset.get_2d_index_of_dataset1())
        workplace_grid_id = interaction_dataset.get_2d_dataset_attribute(self.location_grid_id)

        index_missing_value = logical_or( home_grid_id <= 0, workplace_grid_id <= 0 )        
        relative_x = gridcells.get_attribute("relative_x")
        relative_y = gridcells.get_attribute("relative_y")
        
        distance = ( sqrt( (relative_x[gridcells.try_get_id_index(home_grid_id.ravel())] - relative_x[gridcells.try_get_id_index(workplace_grid_id.ravel())])**2 \
                         + (relative_y[gridcells.try_get_id_index(home_grid_id.ravel())] - relative_y[gridcells.try_get_id_index(workplace_grid_id.ravel())])**2 
                          ) * constants['cell_size'] ).reshape(home_grid_id.shape)
        distance[index_missing_value] = self.default_value
        
        return distance
    

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "person":{ 
                'person_id':   array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 5, 3, 3, 3]),
                'member_id':   array([1, 2, 1, 1, 2, 3]),
              #homegrid_id:           6, 6,-1, 8, 8, 8
                }, 
             "job":{ 
                 'job_id': array([ 1, 2, 3, 4, 5]),
                 'grid_id':array([-1, 9, 3, 1, 6]),
                },
             "household":{
                 'household_id':array([1, 2, 3, 4,  5]),
                 'grid_id':     array([6, 1, 8, 4, -1]),
                 },
             "gridcell":{
                 'grid_id':          array([1,  2,   3,   4,   5,   6,   7,   8,   9]),
                 'relative_x':       array([1,  1,   1,   2,   2,   2,   3,   3,   3]),
                 'relative_y':       array([1,  2,   3,   1,   2,   3,   1,   2,   3]),                
             },
            "urbansim_constant":{
                 'cell_size':        array([150]),
             },
         })
        M = euclidean_distance_from_home_to_work.default_value
        should_be = array([[M,   sqrt((2-3)**2+(3-3)**2)*150, sqrt((2-1)**2+(3-3)**2)*150, sqrt((2-1)**2+(3-1)**2)*150, sqrt((2-2)**2+(3-3)**2)*150], 
                           [M,   sqrt((2-3)**2+(3-3)**2)*150, sqrt((2-1)**2+(3-3)**2)*150, sqrt((2-1)**2+(3-1)**2)*150, sqrt((2-2)**2+(3-3)**2)*150], 
                           [M,   M,                           M,                           M,                           M], 
                           [M,   sqrt((3-3)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-1)**2)*150, sqrt((3-2)**2+(2-3)**2)*150], 
                           [M,   sqrt((3-3)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-1)**2)*150, sqrt((3-2)**2+(2-3)**2)*150], 
                           [M,   sqrt((3-3)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-3)**2)*150, sqrt((3-1)**2+(2-1)**2)*150, sqrt((3-2)**2+(2-3)**2)*150], 
                           ])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
