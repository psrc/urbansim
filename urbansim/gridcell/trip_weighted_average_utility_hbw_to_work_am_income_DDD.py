# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class trip_weighted_average_utility_hbw_to_work_am_income_DDD(Variable):
    """Looks up the variable with the same name that is in zone.  """

    def __init__(self, number):
        self.tnumber = number
        self.twauht_work_am_income = \
                "trip_weighted_average_utility_hbw_to_work_am_income_%d" % int(self.tnumber)
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("zone_id"), 
                attribute_label("zone", self.twauht_work_am_income)]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.twauht_work_am_income)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        zone_id = array([1, 1, 3, 2])
        twauht_work_ai_3 = array([4.1, 5.3, 6.2])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id": array([1,2,3,4]),
                    "zone_id": zone_id
                    }, 
                "zone":{ 
                    "zone_id": array([1,2,3]),
                    "trip_weighted_average_utility_hbw_to_work_am_income_3": twauht_work_ai_3
                }
            }
        )
        
        should_be = array([4.1, 4.1, 6.2, 5.3])
        instance_name = "urbansim.gridcell.trip_weighted_average_utility_hbw_to_work_am_income_3"    
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()