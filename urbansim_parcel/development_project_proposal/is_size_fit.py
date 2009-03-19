# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import bool8, zeros, bool8, logical_and

class is_size_fit(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints
    """

    def dependencies(self):
        return ["vacant_land_area=development_project_proposal.disaggregate(urbansim_parcel.parcel.vacant_land_area)",
                "land_area_min=development_project_proposal.disaggregate(urbansim_parcel.development_template.land_sqft_min)",
                "land_area_max=development_project_proposal.disaggregate(urbansim_parcel.development_template.land_sqft_max)",
                 ]

    def compute(self, dataset_pool):
        dp = self.get_dataset()
        results = zeros(dp.size(), dtype=bool8)
        results[logical_and(dp.get_attribute("vacant_land_area") >= dp.get_attribute("land_area_min"),
                              dp.get_attribute("vacant_land_area") <= dp.get_attribute("land_area_max") )] = 1
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x in (0, 1)", values)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'land_sqft_min': array([0, 10, 1000, 0]),
                'land_sqft_max': array([0, 1999, 2000, 10]),                
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "vacant_land_area":array([10, 1000,  2000]),
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            }
            }
        )
        
        should_be = array([0, 1,  0, 1,  1, 1, 0, 0, 0, 1, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    