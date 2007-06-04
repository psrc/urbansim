#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from developable_maximum_industrial_sqft import developable_maximum_industrial_sqft

class developable_maximum_residential_units(developable_maximum_industrial_sqft):
    """How many residential units are at most developable for each zone."""

    units = "buildings_residential_units"
    total_maximum = "total_maximum_development_residential"


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.developable_maximum_residential_units"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "buildings_residential_units": array([10, 20, 0, 55]),
                "total_maximum_development_residential": array([20, 100, 10, 0])}
             }, 
            dataset = "zone")
        should_be = array([10, 80, 10, 0])
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()