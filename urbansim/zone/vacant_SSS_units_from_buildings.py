# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from variable_functions import my_attribute_label
from urbansim.gridcell.vacant_SSS_units_from_buildings import vacant_SSS_units_from_buildings as gc_vacant_residential_units

class vacant_SSS_units_from_buildings(gc_vacant_residential_units):
    """The residential_units (derived from the buildings table) - number_of_households. """

    def dependencies(self):
        return [my_attribute_label(self.number_of_households), 
                my_attribute_label(self.units)]

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_residential_units_from_buildings"

    def test_my_inputs(self):
        number_of_households = array([1225, 5000, 7500])
        residential_units = array([1995, 10000, 7500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_households": number_of_households, 
                "buildings_residential_space": residential_units}}, 
            dataset = "zone")
        should_be = array([770, 5000, 0])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)

    
if __name__=='__main__':
    opus_unittest.main()