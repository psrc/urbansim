# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import array

class income_category(Variable):
    """
    return 1 for low income
    2 for mid income
    3 for high income
    low, mid, high income percentage is defined in urbansim_constants
    """

    def dependencies(self):
        return [my_attribute_label("income")]

    def compute(self, dataset_pool):
        hhs = self.get_dataset()
        if hhs.mid_income_level < 0: # income levels not computed yet
            hhs.calculate_income_levels(dataset_pool.get_dataset('urbansim_constant'))
        bins = array([hhs.low_income_level, hhs.mid_income_level])
        results = hhs.categorize("income", bins) + 1

        return results

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.income_category"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'income': array([50, 100, 200, 300]),
            }
        )
        
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "low_income_fraction": array([.25]),
                'mid_income_fraction': array([.25]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)

        should_be = array( [1, 1, 2, 3] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()