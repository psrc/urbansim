# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class utility_for_transit_walk_DDD_cars(Variable):
    """utility_for_transit_walk if cars=DDD, 0 otherwise. basically asking, how useful would a transit walk
    be for a household with DDD cars?"""
    
    gc_utility_for_transit_walk = "utility_for_transit_walk"
    
    def __init__(self, number):
        Variable.__init__(self)
        self.has_cars = "has_%s_cars" % number
        
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_utility_for_transit_walk),
                attribute_label("household", self.has_cars)]
        
    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_utility_for_transit_walk,
                                            self.has_cars)

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.utility_for_transit_walk_0_cars"
    #EXAMPLE FOR TUTORIAL

    def test_my_inputs(self):
        utility_for_transit_walk = array([0.0, 0.250, 1])
        #two households, first has 2 cars, second has none. thus, the second household would 
        #have some use for a transit walk, whereas the first household could just drive...
        hh_cars = array([2, 0])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"gridcell":{ 
                "utility_for_transit_walk":utility_for_transit_walk}, 
             "household":{ 
                 "cars":hh_cars}}, 
            dataset = "household_x_gridcell")
        should_be = array([[0,  0,   0], 
                           [0, .250, 1]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()