# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class trip_weighted_average_utility_hbw_from_home_am_income_DDD(Variable):
    """Looks up the variable with the same name that is in zone. """

    def __init__(self, number):
        self.tnumber = number
        self.twauhf_home_am_income = "trip_weighted_average_utility_hbw_from_home_am_income_%d" % int(self.tnumber)
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("zone", self.twauhf_home_am_income)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.twauhf_home_am_income)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        zone_id = array([1, 1, 3])
        twauhf_home_ai_2 = array([4.1, 5.3, 6.2])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3]),
                    "zone_id": zone_id
                    }, 
                "zone":{ 
                    "zone_id": array([1,2,3]),
                    "trip_weighted_average_utility_hbw_from_home_am_income_2": twauhf_home_ai_2
                }
            } 
        )
        
        should_be = array([4.1, 4.1, 6.2])
        instance_name = "urbansim.gridcell.trip_weighted_average_utility_hbw_from_home_am_income_2"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()