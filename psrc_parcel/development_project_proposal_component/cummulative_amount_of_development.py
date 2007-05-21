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

from numpy import array
from opus_core.variables.variable import Variable
from opus_core.simulation_state import SimulationState

class cummulative_amount_of_development(Variable):
    """
    Percent of development amount according to velocity function, given start year of the project and current year.
    """
    _return_type="int32"
    
    def dependencies(self):
        return [
                "_start_year = development_project_proposal_component.disaggregate(development_project_proposal.start_year)",
                "_velocity = development_project_proposal_component.disaggregate(velocity_function.annual_construction_schedule)"
                ]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        current_year = SimulationState().get_current_time()
        velocity = ds.get_attribute("_velocity")
        index = current_year - ds.get_attribute("_start_year")
        def get_one_velocity(velocity_string, idx):
            a = array(eval(velocity_string))
            if idx >= a.size:
                return 100
            return a[idx]
        result = array(map(lambda vel, i: get_one_velocity(vel,i), velocity, index))
        ds.touch_attribute("_start_year") # in order to always recompute (because the simulation year can change)
        return result
    
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
                "start_year": array([2005, 2007, 2005, 2006, 2006])
            },
            'development_project_proposal_component':
            {
                "proposal_component_id": arange(8)+1,
                 "proposal_id":           array([3, 3, 5, 2, 5, 1, 3, 1]),
                 "velocity_function_id":  array([1, 2, 3, 1, 3, 2, 1, 3])
             },
            'velocity_function':
            {
                 "velocity_function_id": arange(3)+1,
                 "annual_construction_schedule": array(["[0, 50, 100]", "[100]", "[25, 50, 75, 100]"])
        
            }
        })
        SimulationState().set_current_time(2007)
        should_be = array([100, 100,  50,  0, 50, 100, 100, 75])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()

        