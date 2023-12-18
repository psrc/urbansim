# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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
                "_velocity = urbansim_parcel.development_project_proposal_component.annual_construction_schedule"
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
        result = array(list(map(lambda vel, i: get_one_velocity(vel,i), velocity, index)))
        ds.touch_attribute("_start_year") # in order to always recompute (because the simulation year can change)
        return result
    
from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
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
                 "velocity_function_id":  array([1, 2, 3, 1, 3, 2, 1, 3]),
                 "annual_construction_schedule":  array(["[100]", "[50, 100]", "[50, 75, 100]", "[25, 50, 100]", "[25, 50, 75, 100]", "[20, 40, 60, 80, 100]", "[20, 40, 60, 80, 100]", "[20, 40, 60, 80, 100]"])
             },
        })
        SimulationState().set_current_time(2007)
        should_be = array([100, 100,  75,  25, 50, 60, 60, 60])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)
        
    def test_my_inputs2(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
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
                 "component_id":          array([3, 1, 4, 2, 4, 1, 3, 4]),
                 "annual_construction_schedule":  array(["[100]", "[50, 100]", "[50, 75, 100]", "[25, 50, 100]", "[25, 50, 75, 100]", "[20, 40, 60, 80, 100]", "[20, 40, 60, 80, 100]", "[20, 40, 60, 80, 100]"])
             },
            'development_template_component':
            {
                "component_id":          array([1, 2, 3, 4]),
                "velocity_function_id":  array([2, 1, 1, 3])
             },            
        })
        SimulationState().set_current_time(2007)
        should_be = array([100, 100,  75,  25, 50, 60, 60, 60])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()

        