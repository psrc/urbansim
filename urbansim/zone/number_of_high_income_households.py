# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_high_income_households(Variable):
    """Number of mid-income households in this zone"""

    _return_type="int32"
    is_high_income = "is_high_income"

    def dependencies(self):
        return [attribute_label("household", self.is_high_income), 
                attribute_label("household", "zone_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.is_high_income)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_high_income_households"
    
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name = 'zones',
            table_data = {
                'zone_id': array([1, 2, 3, 4]),
            }
        )
        storage.write_table(
            table_name = 'households',
            table_data = {
                'household_id': array([1,2,3,4,5,6]),
                'zone_id': array([1, 2, 3, 4, 2, 2]),
                'income': array([1000, 5000, 3000, 10000, 1000, 8000]), # high income: > 5000
            }
        )
        storage.write_table(
            table_name = 'urbansim_constants',
            table_data = {
                "low_income_fraction": array([0.25]),
                'mid_income_fraction': array([0.3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        zones = dataset_pool.get_dataset('zone')
        zones.compute_variables(self.variable_name, 
                                dataset_pool=dataset_pool)
        values = zones.get_attribute(self.variable_name)
        
        should_be = array([0,1,0,1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-20), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()