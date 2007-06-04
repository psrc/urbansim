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

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class total_value_SSS(Variable):
    """Total value of given type of space (computed from buildings)."""

    def __init__(self, type):
        self.total_value = "total_%s_value" % type
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("building", self.total_value),
                attribute_label("building", "zone_id")]

    def compute(self, dataset_pool):
        buildings = dataset_pool.get_dataset('building')
        return self.get_dataset().sum_dataset_over_ids(buildings, self.total_value)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.total_value_industrial"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"building":{ 
                "total_industrial_value": array([10, 20, 0, 0, 5.5]), 
                "zone_id":                array([3,   3, 2, 1,  2])},
             "zone": {
                  "zone_id": array([1,2,3])}
             }, 
            dataset = "zone")
        should_be = array([0, 5.5, 30])

        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()