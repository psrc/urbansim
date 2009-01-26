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

from numpy import ma
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label


class building_age(Variable):
    """The age of a building in this gridcell, computed by subtracting the year built
    from the current simulation year. For gridcells with invalid year built the average
    year built computed over within walking distance is taken. If a gridcells doesn't
    have any valid year built wwd, an average year built computed over the whole region is taken."""

    building_age = "building_age_masked"
    age_wwd = "average_building_age_within_walking_distance"

    def dependencies(self):
        return [my_attribute_label(self.building_age), my_attribute_label(self.age_wwd)]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        age = ds.get_attribute(self.building_age)
        result = ma.filled(age, -1)
        mask = ma.getmask(age)
        if mask is not ma.nomask and mask.any():
            # If there are bad ages then mask won't be ma.nomask and will have some non-False values.  In this case compute
            # the average age for all buildings, then find the ages of buildings within walking distance, and use those
            # to fill in the bad values.
            whole_area_average_age = int(age.sum()/float(ds.size() - age.mask.sum()))
            age_wwd_values = ma.filled(ds.get_attribute(self.age_wwd), whole_area_average_age)
            result[mask] = age_wwd_values[mask]
        return result

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from opus_core.simulation_state import SimulationState

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'year_built': array([1995, 1799, 2006, 0])
                    },
                'urbansim_constant':{
                    'absolute_min_year': array([1800]),
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )

        SimulationState().set_current_time(2005)
        should_be = array([10, 10, 0, 0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

    def test_my_inputs_with_no_mask(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'relative_x': array([1,2,1,2]),
                    'relative_y': array([1,1,2,2]),
                    'year_built': array([1995, 1801, 2006, 2009])
                    },
                'urbansim_constant':{
                    'absolute_min_year': array([1800]),
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
            }
        )

        SimulationState().set_current_time(2009)
        should_be = array([14, 208, 3, 0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()