# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class home_access_to_employment_DDD(Variable):
    """The accessibility to jobs in the given grid cell from employment (other jobs) for number of autos DDD.
    For example, if the possibilities for number of cars per household are 0, 1, 2, or 3+ (3 or more),
    then DDD can be 0, 1, 2, or 3.  Note that for this variable, the zone of the grid cell in which 
    the job is located is the destination zone in the travel data.  (So the name for this variable is misleading - it should
    be home_access_from_employment_DDD instead.)"""
    def __init__(self, n):
        self.num_cars = n
        self.home_access_to_employment = "home_access_to_employment_"+str(self.num_cars)
        Variable.__init__(self)
 
    def dependencies(self):
        return [attribute_label("zone",self.home_access_to_employment)] 
        
    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, name=self.home_access_to_employment)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        home_access_to_employment = array([1000.0, 5000.0, 12000.0])
        locations_in_zoneid = array([1, 1, 3, 2, 2])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "zone":{ 
                    "zone_id":array([1,2,3]),
                    "home_access_to_employment_2":home_access_to_employment
                    }, 
                "gridcell":{ 
                    "grid_id":array([1,2,3,4,5]),
                    "zone_id":locations_in_zoneid
                }
            }
        )
        
        should_be = array([1000.0, 1000.0, 12000.0, 5000.0, 5000.0])
        # The number of cars is 2 in this test    
        instance_name = "urbansim.gridcell.home_access_to_employment_2"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()