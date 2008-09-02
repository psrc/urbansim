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

from numpy import where
from opus_core.variables.variable import Variable

class total_SSS_job_space(Variable):
    """ Total number_of jobs of type SSS that fit into each zone."""

    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        Variable.__init__(self)

    def dependencies(self):
        return ["pseudo_building.job_spaces_capacity", "pseudo_building.building_type_id", "job_building_type.name"]

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('job_building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("name") == self.building_type_name][0]
        bldgs = dataset_pool.get_dataset('pseudo_building')
        capacity = where(bldgs.get_attribute('building_type_id') == code, bldgs.get_attribute("job_spaces_capacity"), 0)
        ds = self.get_dataset()
        return ds.sum_over_ids(bldgs.get_attribute(ds.get_id_name()[0]), capacity)

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
             "job_spaces_capacity": array([20, 3, 0, 35, 200])
             },
            'zone':
            {
             "zone_id":array([1,2,3]),
             },
            'job_building_type':
            {
             "id":array([1,2]),
             "name":array(["commercial", "industrial"])
             },
             
           }
        )
        
        should_be = array([20, 35, 0])
        instance_name = 'urbansim_zone.zone.total_commercial_job_space'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
if __name__=='__main__':
    opus_unittest.main()