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
from variable_functions import my_attribute_label

class building_sqft(Variable):
    _return_type = "float32"

    def dependencies(self):
        return [
                my_attribute_label("building_sqft_per_unit"),
                my_attribute_label("units_proposed")
                ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.get_attribute("building_sqft_per_unit") * ds.get_attribute("units_proposed")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 100 ", values)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_project_proposal_component':
            {
                "proposal_component_id": arange(8)+1,
                 "units_proposed":         array([100, 250, 130, 0,   52, 1, 20, 0]),
                 "building_sqft_per_unit": array([1,    1,  60,  25,  10, 2,  1,  1])
             }
        })
        should_be = array([100, 250,  130*60,  0, 52 * 10, 2, 20, 0])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
