#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

class is_building_type_SSS(Variable):
    """ Is this pseudo-building of a building type SSS."""

    btype = "building_type_id"

    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        Variable.__init__(self)

    def dependencies(self):
        return ["pseudo_building.%s" % self.btype, "job_building_type.name"]

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('job_building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("name") == self.building_type_name]
        return self.get_dataset().get_attribute(self.btype) == code

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester


class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_zone','urbansim'],
            test_data={
            'pseudo_building':
            {"pseudo_building_id":array([1,2,3,4,5]),
             "building_type_id":    array([1,  2, 1, 1,  2]),
             "zone_id":             array([1,  1, 3, 2,  2]),
             },
            'job_building_type':
            {
             "id":array([1,2]),
             "name":array(["commercial", "industrial"])
             },
             
           }
        )
        
        should_be = array([1, 0, 1, 1, 0])
        instance_name = 'urbansim_zone.pseudo_building.is_building_type_commercial'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
if __name__=='__main__':
    opus_unittest.main()