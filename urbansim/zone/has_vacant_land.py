# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.has_vacant_land import has_vacant_land as gc_has_vacant_land
from .variable_functions import my_attribute_label

class has_vacant_land(gc_has_vacant_land):
    """Boolean indicating whether the gridcell has vacant land"""

    _return_type = "bool8"

    def dependencies(self):
        return [my_attribute_label(self.vacant_sqft)]


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.has_vacant_land"

    def test_my_inputs(self):
        vacant_sqft = array([1, 0, 5])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "vacant_land_sqft":vacant_sqft}}, 
            dataset = "zone")
        should_be = array([True, False, True])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()