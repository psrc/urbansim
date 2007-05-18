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

class units_proposed(Variable):
    _return_type = "float32"

    def dependencies(self):
        return [
                "_units_proposed_in_proposal = development_project_proposal_component.disaggregate(psrc_parcel.development_project_proposal.units_proposed)",
                 my_attribute_label("percent_building_sqft")
                ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.get_attribute("_units_proposed_in_proposal")/100.0 * ds.get_attribute("percent_building_sqft")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 100 ", values)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim'],
            test_data={
            'development_project_proposal':
            {
                "proposal_id":    array([1,  2,    3,  4, 5]),
                "units_proposed": array([34, 250, 130, 0, 52])
            },
            'development_project_proposal_component':
            {
                "proposal_component_id": arange(8)+1,
                 "proposal_id":           array([3,   3, 5,  2,   5,   1, 3, 1]),
                 "percent_building_sqft": array([30, 25, 1, 100, 99, 100, 45, 0])
             }
        })
        should_be = array([130/100.0*30, 130/100.0*25,  52/100.0,  250, 52/100.0 * 99, 34, 130/100.0*45, 0])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
