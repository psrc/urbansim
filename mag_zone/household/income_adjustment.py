# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.simulation_state import SimulationState
from numpy import where

class income_adjustment(Variable):

    """
    Adjusts income based on aggregate forecast of income contained in annual_income_adjustment dataset.
    """

    def compute(self, dataset_pool):
        # get adjustment dataset and proper income adjustment factor
        income_adjustment_dataset = dataset_pool.get_dataset('annual_income_adjustment')
        current_year = SimulationState().get_current_time()
        adjustment_index = where(income_adjustment_dataset.get_attribute('year')==current_year)
        income_adjustment = income_adjustment_dataset.get_attribute('income_adjustment_factor')[adjustment_index][0]
        # get income to adjust
        income = self.get_dataset().get_attribute("income")
        # adjust and return income
        return income * income_adjustment
        


from numpy import array, ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    
    variable_name = "mag_zone.household.income_adjustment"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')  
        storage.write_table(
            table_name='households',
            table_data={
                        "household_id":array([1,2,3,4,5,6,7,8,9,10]),
                        "income":array      ([1.5,9.4,2.6,5.3,8.8,3.3,4.6,10.4,3.4,6.2]),
                       }
                            )
        storage.write_table(
            table_name='annual_income_adjustments',
            table_data={
                        "annual_income_adjustment_id":array([1,2,3,4,5,6,7,8,9,10,11]),
                        "year":array([0,1,2,3,4,5,6,7,8,9,10]),
                        "income_adjustment_factor":array([0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001]),
                       }
                            )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)
        
        should_be = array([0.0015,0.0094,0.0026,0.0053,0.0088,0.0033,0.0046,0.0104,0.0034,0.0062])
        
        self.assert_(ma.allclose(values, should_be,), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()




