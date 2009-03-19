# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import where
from numpy import ma

class n_recent_SSS(Variable):
    """Number of residential units per each gridcell built in the last
    N years, where N is the values of the recent_years field of the 
    uransim_constants table. It uses the buildings table.
    """

    _return_type="int32"

    def __init__(self, units):
        self.units = units
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("building", "building_age"), attribute_label("building", "grid_id"),
                attribute_label("building", self.units)]

    def compute(self, dataset_pool):
        recent_years = dataset_pool.get_dataset('urbansim_constant')["recent_years"]
        buildings = dataset_pool.get_dataset('building')
        age = buildings.get_attribute("building_age")
        values = buildings.get_attribute(self.units)
        values = where(ma.filled(age, recent_years+1) <= recent_years, values, 0)
        return self.get_dataset().sum_over_ids(buildings.get_attribute("grid_id"), values)

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from opus_core.simulation_state import SimulationState

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        grid_id = array([1,  1,  2, 3, 1,  2])
        units = array([100, 40, 33, 0, 30,  10])
        SimulationState().set_current_time(2000)
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell": { 
                    "grid_id": array([1,2,3])
                    },
                "building": {
                    "building_id": array([1,2,3,4,5,6]),
                    "grid_id": grid_id,
                    "year_built": array([1980, 1945, 2000, 1997, 1000, 1970]),
                    "residential_units": units
                    },
                "urbansim_constant": {
                    "recent_years": array([3]),
                    "absolute_min_year": array([1800])
                }
            }
        )

        should_be = array([0, 33, 0]) 
        instance_name = 'urbansim.gridcell.n_recent_residential_units'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()