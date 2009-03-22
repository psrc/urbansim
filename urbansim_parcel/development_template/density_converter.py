# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import where, ones

class density_converter(Variable):
    """
    return constants to convert density to a sqft basis 
    units_per_acre -> units_per_sqft,
    far (floor area ratio) -> far
    """
    _return_type = "float32"
    ACRE_TO_SQFT = 43560.00
    def dependencies(self):
        return ["development_template.density_type",
                 ]

    def compute(self, dataset_pool):
        dt = self.get_dataset()
        results = ones(dt.size(), dtype=self._return_type)
        idx = where(dt.get_attribute("density_type") == 'units_per_acre')[0]
        results[idx] = 1 / self.ACRE_TO_SQFT
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={            
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'density_type': array(['units_per_acre', 'far', 'units_per_acre', 'far']),
                'density':array([0.2, 10, 1.5, 7.2], dtype='float32')
            },
#            'development_template_component':
#            {
#                'template_id': array([1,2,3,4,4]),
#                "component_id":array([1,2,3,4,1]),
#                "percent_of_building_sqft":array([100, 100, 100, 20, 80])
#            },
#            'building_component':
#            {
#                "component_id":array([1,  2,  3,  4]),
#                "sqft_per_unit":  array([1600,  1,  2000,  1]),
#                "construction_cost_per_unit":array([100000,  200,  300000,  100])
#            }
            }
        )
        
        should_be = array([1 / 43560.00, 1, 1 / 43560.00, 1])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    