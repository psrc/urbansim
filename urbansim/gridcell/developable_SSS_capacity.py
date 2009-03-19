# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class developable_SSS_capacity(Variable):
    """ Returns either developable_maximum_industrial/commercial_sqft/residential_units,
    depending on the building type. The values are clipped to 0.
    """

    def __init__(self, type):
        self.type = type
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("building_type", "name"), attribute_label("building_type", "units")]

    def compute(self, dataset_pool):
        bt = dataset_pool.get_dataset('building_type')
        ds = self.get_dataset()
        idx = bt.get_attribute("name") == self.type
        units_name = bt.get_attribute("units")[idx][0]
        dependent_variable = my_attribute_label("developable_maximum_%s" % units_name)
        if dependent_variable not in self.dependencies():
            ds.compute_variables([dependent_variable])
            self.add_dependencies([dependent_variable])
        return clip_to_zero_if_needed(ds.get_attribute(dependent_variable), "developable_%s_capacity" % self.type)




from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                'gridcell':{
                    'grid_id':array([1,2,3,4]),
                    'developable_maximum_commercial_sqft':array([1200, 16, 3900, 15]),
                    },
                'building_type': {
                    'building_type_id':array([1,2]),
                    'name': array(['residential', 'commercial']),
                    'units': array(['residential_units', 'commercial_sqft'])
                }
            }
        )

        should_be = array([1200, 16, 3900, 15])
        instance_name = "urbansim.gridcell.developable_commercial_capacity"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()