# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import clip_to_zero_if_needed

class total_SSS_sqft(Variable):
    """ total SSS_sqft """ 

    _return_type = "int32"
    
    def __init__(self, type):
        self.is_bt = "is_building_type_%s" % type
        Variable.__init__(self)

    def dependencies(self):
        return ["building.non_residential_sqft",
                "urbansim_zone.building.%s" % self.is_bt]                             

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.get_attribute("non_residential_sqft")*ds.get_attribute(self.is_bt)
    


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone', 'urbansim'],
            test_data={
             'building':
                 {"building_id":         array([1,  2, 3, 4,  5]),
                  "building_type_id":    array([1,  2, 1, 1,  2]),
                  "non_residential_sqft": array([2000, 3, 10, 35, 200]),
                },
            'building_type':
            {
             "building_type_id":array([1,2]),
             "building_type_name":array(["commercial", "industrial"])
             },
            }
        )
    
        should_be = array([2000, 0, 10, 35, 0])
        instance_name = "urbansim_zone.building.total_commercial_sqft"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()