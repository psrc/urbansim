# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
#from urbansim.zone.variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_low_income(Variable):
    """Is income <= low_income_level"""
    income = "income"

    def dependencies(self):
        return [attribute_label('household',self.income, 'mag_zone')]

    def compute(self, dataset_pool):
        if self.get_dataset().low_income_level < 0: # income levels not computed yet
            self.get_dataset().calculate_income_levels(dataset_pool.get_dataset('urbansim_constant'))
        return self.get_dataset().get_attribute(self.income) <= self.get_dataset().low_income_level


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_low_income"

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
                'mid_income_fraction': array([.5]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)
        
        should_be = array( [1, 1, 0, 0] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()