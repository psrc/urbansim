#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

class units_occupied(Variable):
    """number of units occupied for type SSS"""

#    def __init__(self, type):
#        Variable.__init__(self)
#        self.type = type

    def dependencies(self):
        return [
                "jobs = parcel.number_of_agents(job)",
                "households = parcel.number_of_agents(household)",
                "_units_occupied = parcel.jobs * parcel.sqft_per_job + households"  #ideally one or both of these will be zero
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_units_occupied")

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == True or x == False", values)


from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['az_smart', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1,   2,    3,  4]),
                "land_use_type_id": array([1,   2,    3,  5]),
                "sqft_per_job": array([1, 50,  200,  0],dtype=int32),
            },
            'job':
            {
                "job_id":array([1, 2, 3, 4]),
                "parcel_id":  array([1, 1, 2, 3]),
            },
            'household':
            {
                "household_id":array([1, 2, 3, 4]),
                "parcel_id":  array([4, 4, 2, 3]),
            },
        })
        should_be = array([2, 51, 201, 2]) #nonsense

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
