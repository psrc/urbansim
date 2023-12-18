# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from opus_core.misc import safe_array_divide
from numpy import ma

class average_building_age_SSS(Variable):
    """Computed by dividing sum of building ages of buildings of given type in the given cell by
        the total number of those buildings in the cell. For cells that have no buildings it returns -1."""

    building_age = "building_age"

    def __init__(self, type):
        self.number_of_buildings = "number_of_%s_buildings" % type
        self.is_building_type = "is_building_type_%s" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.number_of_buildings),
                attribute_label("building", self.building_age), attribute_label("building", self.is_building_type),
                attribute_label("building", "grid_id")]

    def compute(self, dataset_pool):
        nb = self.get_dataset().get_attribute(self.number_of_buildings)
        buildings = dataset_pool.get_dataset('building')
        age = buildings.get_attribute(self.building_age)*buildings.get_attribute(self.is_building_type)
        mask = ma.getmask(age)
        if mask is ma.nomask:
            donotcount=0
        else:
            mask=mask*buildings.get_attribute(self.is_building_type)
            # count number of buildings that have missing year_built and therefore won't be included in the average.
            donotcount = self.get_dataset().sum_over_ids(buildings.get_attribute("grid_id"), mask.astype("int8"))

        # fill -1 for masked values, in order to distinguish it from age=0.
        return safe_array_divide(self.get_dataset().sum_over_ids(buildings.get_attribute("grid_id"),
                                      age), nb - donotcount, -1)



from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from opus_core.simulation_state import SimulationState

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        SimulationState().set_current_time(2005)
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    "grid_id": array([1,2,3])
                    },
                "building":{
                    'building_id': array([1,2,3,4,5,6,7]),
                    "grid_id": array([1,1,2,3,1,2,1]),
                    "is_building_type_residential": array([1,0,1,1,1,0,1]),
                    "year_built": array([1995,2000,2006,0,10,0,2007])
                    },
                'urbansim_constant':{
                    "absolute_min_year": array([1800]),
                }
            }
        )

        should_be = array([5, 0, -1])
        instance_name = 'urbansim.gridcell.average_building_age_residential'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()