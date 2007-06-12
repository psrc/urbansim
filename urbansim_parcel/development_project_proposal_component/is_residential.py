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

class is_residential(Variable):
    _return_type = "bool8"

    def dependencies(self):
        return [
                "_unit_name=development_project_proposal_component.disaggregate(building_type.unit_name)"
                ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.get_attribute("_unit_name") == 'residential_units'        

    def post_check(self, values, dataset_pool):
        self.do_check("x == True or x == False", values)

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
                "proposal_component_id": arange(5)+1,
                "building_type_id": array([1,3,2,1,2], dtype="int32")
             },
             'building_type':
             {
               "building_type_id": array([1,2,3], dtype="int32"),
                "unit_name": array(["residential_units", "building_sqft", "residential_units"])
             }
        })
        should_be = array([True, True, False, True, False])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
