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
        return [attribute_label('job', "zone_id"), attribute_label('job', "potential_movers"),
                attribute_label('job', self.is_type)]

    def compute(self, dataset_pool):
        job = dataset_pool.get_dataset('job')
        is_mover = logical_and(job.get_attribute(self.is_type), job.get_attribute("potential_movers"))
        return self.get_dataset().sum_over_ids(job.get_attribute(self.get_dataset().get_id_name()[0]), is_mover)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('job').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_potential_commercial_job_movers"
    def test(self):
        zone_id = array([1, 2, 3, 4, 5])
        job_zone_id = array([1, 2, 3, 4, 2, 2])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "zone_id":zone_id}, 
             "job":{ 
                 "zone_id":job_zone_id,
                 "potential_movers": array([1,1,0,0,0,1]),
                 "is_building_type_commercial": array([1,0,1,1,0,0])}}, 
            dataset = "zone")
        should_be = array([1,0,0,0,0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=0), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()