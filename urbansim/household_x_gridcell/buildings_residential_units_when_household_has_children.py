# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class buildings_residential_units_when_household_has_children(Variable):
    """Number of residential units in the cell (derived from buildings), given that the decision-making household has children.
    [if hh.children > 0 then cell.residential_units else 0]"""    

    gc_residential_units = "buildings_residential_space"
    hh_children = "is_without_children"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_residential_units), \
                attribute_label("household", self.hh_children)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_residential_units,
                                            self.hh_children, do_logical_not=True)               

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.buildings_residential_units_when_household_has_children"
    
    def test_full_tree(self):
        residential_units = array([12, 0, 5, 100])
        children = array([1, 0, 0, 3, 0, 2])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                "buildings_residential_space":residential_units}, \
            "household":{ \
                "children":children}}, \
            dataset = "household_x_gridcell")
        should_be = array([[12,0,5,100], [0,0,0,0], [0,0,0,0], [12,0,5,100], [0,0,0,0], [12,0,5,100]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                         True, msg = "Error in " + self.variable_name)

    def test_my_inputs(self):
        """Number of residential units in the cell, given that the decision-making household has children,
           or 0 if the decision-making household is without children.
        """
        residential_units = array([12, 0, 5, 100])
        is_without_children = array([0, 1, 1, 0, 1, 0])
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ \
                "buildings_residential_space":residential_units}, \
            "household":{ \
                "is_without_children":is_without_children}}, \
            dataset = "household_x_gridcell")
        should_be = array([[12,0,5,100], [0,0,0,0], [0,0,0,0], [12,0,5,100], [0,0,0,0], [12,0,5,100]])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()