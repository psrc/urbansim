# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import where, zeros

class units_per_acre(Variable):
    """
    """
    ## TODO: it should calculate units_per_acre density for template whose density name is not
    ## 'units_per_acre but contains residential components (mixed use)
    _return_type = "float32"
    def dependencies(self):
        return ["development_template.density_type",
                "development_template.density",
                 ]

    def compute(self, dataset_pool):
        dp = self.get_dataset()
        results = zeros(dp.size(), dtype=self._return_type)
        idx = where(dp.get_attribute("density_type") == 'units_per_acre')[0]
        results[idx] = dp.get_attribute("density")[idx].astype(self._return_type)
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
        
        should_be = array([0.2, 0, 1.5, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    