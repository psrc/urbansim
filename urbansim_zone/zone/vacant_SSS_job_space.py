# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import clip_to_zero_if_needed
from variable_functions import my_attribute_label

class vacant_SSS_job_space(Variable):
    """ The total_SSS_job_space - number_of_SSS_jobs. """ 

    _return_type = "int32"
    
    def __init__(self, type):
        self.number_of_jobs = "number_of_%s_jobs" % type
        self.possible_jobs = "total_%s_job_space" % type
        self.variable_name = "vacant_%s_job_space" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs), 
                my_attribute_label(self.possible_jobs)]                             

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return  clip_to_zero_if_needed(ds.get_attribute(self.possible_jobs) - 
                    ds.get_attribute(self.number_of_jobs), self.variable_name)
    


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone', 'urbansim'],
            test_data={
             'pseudo_building':
                 {"pseudo_building_id":  array([1,2,3,4,5]),
                  "building_type_id":    array([1,  2, 1, 1,  2]),
                  "zone_id":             array([1,  1, 3, 2,  2]),
                  "job_spaces_capacity": array([20, 3, 10, 35, 200])
                },
            'zone':
            {
             "zone_id":array([1,2,3]),
             "number_of_commercial_jobs": array([12, 50, 0])
             },
            'job_building_type':
            {
             "id":array([1,2]),
             "name":array(["commercial", "industrial"])
             },
            }
        )
    
        should_be = array([20-12, 0, 10])
        instance_name = "urbansim_zone.zone.vacant_commercial_job_space"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()