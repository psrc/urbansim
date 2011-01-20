# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class park_sqft_wwd_when_household_has_children(Variable):
    """park sqft in the cell, given that the decision-making household has children.
    """    

    gc_vacant_land = "sum_buildings_park_space_within_walking_distance"
    hh_children = "is_without_children"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_vacant_land), \
                attribute_label("household", self.hh_children)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_vacant_land,
                                            self.hh_children, do_logical_not=True)               

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.park_sqft_wwd_when_household_has_children"
    
    def test_full_tree(self):
        sqft = array([12, 0, 5, 100])
        children = array([1, 0, 0, 3, 0, 2])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                "sum_buildings_park_space_within_walking_distance":sqft}, \
            "household":{ \
                "children":children}}, \
            dataset = "household_x_gridcell")
        should_be = array([[12,0,5,100], [0,0,0,0], [0,0,0,0], [12,0,5,100], [0,0,0,0], [12,0,5,100]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                         True, msg = "Error in " + self.variable_name)

    def test_my_inputs(self):
        """Number of park sqft in the cell, given that the decision-making household has children,
           or 0 if the decision-making household is without children.
        """
        residential_units = array([12, 0, 5, 100])
        is_without_children = array([0, 1, 1, 0, 1, 0])
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                "sum_buildings_park_space_within_walking_distance":residential_units}, \
            "household":{ \
                "is_without_children":is_without_children}}, \
            dataset = "household_x_gridcell")
        should_be = array([[12,0,5,100], [0,0,0,0], [0,0,0,0], [12,0,5,100], [0,0,0,0], [12,0,5,100]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()