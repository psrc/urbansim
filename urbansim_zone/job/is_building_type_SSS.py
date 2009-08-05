# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class is_building_type_SSS(Variable):
    """ Is this a job of a building type SSS."""
    
    _return_type='bool8'

    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        Variable.__init__(self)

    def dependencies(self):
        return ["urbansim_zone.job.building_type_id", "building_type.name",
                "building_type.building_type_id"]

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("name") == self.building_type_name]
        return self.get_dataset().get_attribute("building_type_id") == code

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_zone.job.is_building_type_commercial"

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone','urbansim'],
            test_data={
            'building_type': {
                'building_type_id':array([1,2]),
                'name': array(['foo', 'commercial'])
                },
            'job': {
                    'job_id': array([1,2,3]),
                    'building_id':array([3,1,2])
                    },
            'building': {
                    'building_id': array([1,2,3]),
                    'building_type_id': array([2,1,2])        
                    }
            })

        should_be = array([1,1,0])
        tester.test_is_equal_for_family_variable(self, should_be, self.variable_name)


if __name__=='__main__':
    opus_unittest.main()