# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import zeros


class is_in_development_type_group_SSS(Variable):
    """Returns a boolean indicating whether this gridcell's development type group is
    of given name (by SSS)."""
    _return_type = "bool8"
    gr_name = "name"
    development_type_id = "development_type_id"

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("development_group", "group_id"),
                attribute_label("development_group", self.gr_name),
                my_attribute_label(self.development_type_id),
                attribute_label("development_type", "development_type_id")]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        groups = dataset_pool.get_dataset('development_group')
        group_id = groups.get_id_attribute()[groups.get_attribute(self.gr_name)==self.group][0]
        devtypes = dataset.get_attribute(self.development_type_id)
        types_in_group = dataset_pool.get_dataset('development_type').get_types_for_group(group_id)
        result = zeros(dataset.size(),dtype=self._return_type)
        for type in types_in_group:
            result = result + (devtypes == type).astype(self._return_type)
        return result

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array, arange
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        tester = VariableTester(
            __file__,
            package_order=['urbansim', 'opus_core'],
            test_data={
                'gridcell':{
                    'grid_id': array([1,2,3,4]),
                    'development_type_id': array([1, 3, 2, 3]),
                    },
                'development_events':{
                    'grid_id': array([100,100,101,102]),
                    'scheduled_year': array([1999,1998,1999,1999]),
                    'starting_development_type_id': array([1, 3, 2, 3]),
                    'ending_development_type_id': array([1, 1, 2, 3]),
                    },
                'development_type':{
                    'development_type_id': array([1,2,3]),
                    'name': array(['low', 'medium', 'high']),
                    'min_units': array([1,2,10]),
                    'max_units': array([1,9,999]),
                    'min_sqft': array([1,100,1000]),
                    'max_sqft': array([99,999,99999]),
                    },
                'development_group':{
                    'group_id': array([1,2,3]),
                    'name': array(["mixed_use", "high_density_residential", 'other']),
                    },
                'development_type_group_definitions': {
                    'id': array([1,2,3,4]),
                    'group_id': array([1,2,2,3]),
                    'development_type_id': array([1,1,2,3]),
                }
            }
        )

        # Test variable 1
        should_be = array( [True, False, False, False] )
        instance_name1 = "urbansim.gridcell.is_in_development_type_group_mixed_use"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name1)

        # Test variable 2
        should_be = array( [True, False, True, False] )
        instance_name2 = "urbansim.gridcell.is_in_development_type_group_high_density_residential"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name2)

if __name__=='__main__':
    opus_unittest.main()