# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_development_events(Variable):
    """Given an array of jobs and which grid id's they correspond to, 
    and another array of whether the specified jobs are commercial or not,
    computes the number of commercial jobs for each grid id"""

    _return_type="int32"

    def dependencies(self):
        return [attribute_label("development_event", 'grid_id'), 
                my_attribute_label("grid_id")]

    def compute(self, dataset_pool):
        events = dataset_pool.get_dataset('development_event')
        return self.get_dataset().sum_dataset_over_ids(events, constant=1)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3])
        events_grid_id = array([2, 1, 3, 1] )
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":array([1,2,3]),
                    "gridcell_grid_id":gridcell_grid_id 
                    }, 
                "development_event":{ 
                    "grid_id":events_grid_id, 
                    "scheduled_year":array([1999, 1990, 1993, 1997])
                }
            }
        )
        
        should_be = array([2, 1, 1])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()