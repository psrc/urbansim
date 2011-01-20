# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_number_of_agents_with_same_attribute_value import abstract_number_of_agents_with_same_attribute_value

class same_sector_employment_in_parcel(abstract_number_of_agents_with_same_attribute_value):
    """"""
        
    agent_attribute_name = "job.sector_id"
    agent_dependencies = ['urbansim_parcel.job.parcel_id']
    choice_set_dependencies = []
    #unique_agent_attribute_value = range(1, 20)
    geography_dataset_name = 'parcel'
    ## use default
    #expression_agents_of_attribute_by_geography = "'agents_of_attribute_%(agent_attribute_value)s = %(geography_dataset_name)s.aggregate(%(agent_attribute_name)s==%(agent_attribute_value)s)'"
                                       
    
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
                 'parcel_id':     array([1, 2, 2, 3, 4,]),
                },
             'parcel':{
                    'parcel_id': array([1,2,3,4]),
                    },
         })
        ## mind the mirror of gridcells in waling_distance calculus
        should_be = array([[2, 1, 1, 0, 0], 
                           [2, 1, 1, 0, 0],
                           [0, 0, 0, 0, 1],
                           [2, 1, 1, 0, 0],
                           [0, 2, 2, 0, 0],
                           [0, 2, 2, 0, 0]])
                            
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
