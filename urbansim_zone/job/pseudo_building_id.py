# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, where
from opus_core.variables.variable import Variable

class pseudo_building_id(Variable):
    """Id within the pseudo-buildings given a zone and building types. """

    def dependencies(self):
        return ['job.zone_id', 'job.building_type', 'job_building_type.name']

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('job_building_type')
        pbldgs = dataset_pool.get_dataset('pseudo_building')
        jobs = self.get_dataset()
        job_bts = jobs.get_attribute('building_type')
        zones = jobs.get_attribute('zone_id')
        codes = building_types.get_id_attribute()
        result = zeros(jobs.size(), dtype='int32')
        for code in codes:
            if code not in job_bts:
                continue
            idx = where(job_bts == code)[0]
            result[idx] = pbldgs.get_ids_of_locations_and_type(zones[idx], code)
        return result
                            
                            
from numpy import array, arange
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone', 'urbansim'],
            test_data={
                'job':{
                    'job_id': array([1,2,3]),
                    'zone_id':      array([12,10,15]),
                    'building_type':array([3,1,1]),
                },
                'job_building_type':{
                    "name": array(["commercial", "residential", "industrial"]),
                    "id": array([1,2,3])
                },
                'pseudo_building': {
                    'pseudo_building_id': arange(11)+1,
                    'zone_id':            array([5, 5, 10, 10, 10, 12, 12, 12, 15, 15, 15]),
                    'building_type_id':   array([1, 2, 3,   2,  1,  2,  1,  3,  2,  3,  1]),   
                                    }
            }
        )
        
        should_be = array([8, 5, 11])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
