# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import logical_and
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_potential_SSS_job_movers(Variable):
    """Number of jobs of given type that should potentially move. Expects attribute 'potential_movers'
    of job set that has 1's for jobs that should move, otherwise 0's."""
    _return_type="int32"

    def __init__(self, type):
        self.is_type = "is_building_type_%s" % type
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label('job', "grid_id"), attribute_label('job', "potential_movers"),
                attribute_label('job', self.is_type)]

    def compute(self, dataset_pool):
        job = dataset_pool.get_dataset('job')
        is_mover = logical_and(job.get_attribute(self.is_type), job.get_attribute("potential_movers"))
        return self.get_dataset().sum_over_ids(job.get_attribute(self.get_dataset().get_id_name()[0]), is_mover)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('job').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test(self):
        zone_id = array([1, 2, 3, 4, 5])
        job_zone_id = array([1, 2, 3, 4, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":zone_id
                    }, 
                "job":{
                    "job_id":array([1,2,3,4,5,6]),
                    "grid_id":job_zone_id,
                    "potential_movers": array([1,1,0,0,0,1]),
                    "is_building_type_commercial": array([1,0,1,1,0,0])
                }
            }
        )
        
        should_be = array([1,0,0,0,0])
        instance_name = "urbansim.gridcell.number_of_potential_commercial_job_movers"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()