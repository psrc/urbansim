# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_DDD_cars(Variable):
    """Percent of households within the walking radius that are designated as low-income, given that 
    the decision-making household is low-income.
    [trip_weighted_average_time_hbw_from_home_am_transit_walk if hh.has_0_cars is true else 0]"""    
    
    twh_tw = \
      "trip_weighted_average_time_hbw_from_home_am_transit_walk"

    def __init__(self, number):
        self.tnumber = number
        self.hh_has_some_cars = "has_%d_cars" % (self.tnumber)
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("household", self.hh_has_some_cars),
                "psrc.gridcell." + self.twh_tw ]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(self.twh_tw, self.hh_has_some_cars)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.opus_package_info import package
    
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_gridcell.trip_weighted_average_time_hbw_from_home_am_transit_walk_if_has_0_cars"
    
    def test_my_inputs(self):
        trip_weighted_average_time_hbw_from_home_am_transit_walk = array([50, 0, 15])
        has_0_cars = array([1, 0, 1, 1])
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                 "trip_weighted_average_time_hbw_from_home_am_transit_walk":trip_weighted_average_time_hbw_from_home_am_transit_walk}, \
             "household":{ \
                 "has_0_cars":has_0_cars}}, \
            dataset = "household_x_gridcell")
        should_be = array([[50, 0, 15], [0, 0, 0], [50, 0, 15], [50, 0, 15]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-10), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()