# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import where, float32
from opus_core.logger import logger

class industrial_sqft_per_job_within_walking_distance(Variable):
    """
    """

    industrial_sqft_within_walking_distance = "industrial_sqft_within_walking_distance"
    number_of_industrial_jobs = "number_of_industrial_jobs"
    number_of_industrial_jobs_wwd = "number_of_industrial_jobs_within_walking_distance"
    industrial_sqft = "industrial_sqft"
    
    def dependencies(self):
        return [my_attribute_label(self.number_of_industrial_jobs), 
                my_attribute_label(self.industrial_sqft_within_walking_distance), 
                my_attribute_label(self.number_of_industrial_jobs_wwd), 
                my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        nj = self.get_dataset().get_attribute(self.number_of_industrial_jobs_wwd)
        sqft = self.get_dataset().get_attribute(self.industrial_sqft_within_walking_distance)
        regional_average = self.get_dataset().get_attribute(self.industrial_sqft).sum()/ \
                           float(self.get_dataset().get_attribute(self.number_of_industrial_jobs).sum())
        return where(sqft < 5000, regional_average, ma.filled(sqft/ 
                                                           ma.masked_where(nj==0,nj.astype(float32)),0))
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'industrial_sqft': array([30, 1000, 50, 2000]),
                    'number_of_industrial_jobs': array([100,0,10,500]),
                },
                'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                    "acres": array([105.0]),
                }
            }
        )
        
        should_be = array([3080.0/610.0, 5030.0/600.0, 3080.0/610.0, 7050.0/1510.0])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()
        