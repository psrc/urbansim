# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_number_of_agents_with_same_attribute_value import abstract_number_of_agents_with_same_attribute_value

class same_sector_employment_within_walking_distance(abstract_number_of_agents_with_same_attribute_value):
    """Sum over c in cell.walking_radius, count of j in c.placed_jobs where j.sector = job.sector."""
        
    agent_attribute_name = "job.sector_id"
    agent_dependencies = ['urbansim_parcel.job.grid_id']
    choice_set_dependencies = ['urbansim_parcel.building.grid_id']
    #unique_agent_attribute_value = range(1, 20)
    geography_dataset_name = 'gridcell'
    expression_agents_of_attribute_by_geography = "'agents_of_attribute_%(agent_attribute_value)s = urbansim.gridcell.sector_%(agent_attribute_value)s_employment_within_walking_distance'"
                                       
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import arange, array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "job":{ 
                'job_id':     array([1, 2, 3, 4, 5, 6]),
                'building_id':array([1, 1, 5, 3, 3, 3]),
                'sector_id':  array([1, 1, 2, 1, 3, 3]),
                }, 
             "building":{ 
                 'building_id': array([1, 2, 3, 4, 5,]),
                 'grid_id':     array([1, 2, 2, 3, 4,]),
                },
             'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    },
             'urbansim_constant':{
                 "walking_distance_circle_radius": array([150]), 
                 'cell_size': array([150]),
                 "acres": array([105.0]),
             }
         })
        ## mind the mirror of gridcells in waling_distance calculus
        should_be = array([[7, 5, 5, 2, 1], 
                           [7, 5, 5, 2, 1],
                           [0, 1, 1, 1, 3],
                           [7, 5, 5, 2, 1],
                           [2, 6, 6, 0, 2],
                           [2, 6, 6, 0, 2]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
