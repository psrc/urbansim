# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class pseudo_building_id(Variable):
    """Id within the pseudo-buildings given a zone and residential building type. """

    def dependencies(self):
        return ['household.zone_id', 'job_building_type.name']

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('job_building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("name") == 'home_based'][0]
        pbldgs = dataset_pool.get_dataset('pseudo_building')
        return pbldgs.get_ids_of_locations_and_type(self.get_dataset().get_attribute('zone_id'), code)
                            
                            
from numpy import array, arange
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone', 'urbansim'],
            test_data={
                'household':{
                    'household_id': array([1,2,3]),
                    'zone_id':      array([12,10,15]),
                },
                'job_building_type':{
                    "name": array(["commercial", "home_based", "industrial"]),
                    "id": array([1,2,3])
                },
                'pseudo_building': {
                    'pseudo_building_id': arange(10)+1,
                    'zone_id':            array([5, 5, 10, 10, 10, 12, 12, 15, 15, 15]),
                    'building_type_id':   array([1, 2, 3,   2,  1,  2,  1,  2,  3,  1]),   
                                    }
            }
        )
        
        should_be = array([6, 4, 8])
        
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
