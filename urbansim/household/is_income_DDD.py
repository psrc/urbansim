# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class is_income_DDD(Variable):
    """ Is this household income in the range specified by the income type DDD.
        This range is specified in urbansim_constant by the fuction get_income_range_for_type. """
    income = "income"
    
    def __init__(self, number):
        self.tnumber = number
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.income)]

    def compute(self, dataset_pool):
        min_income, max_income = dataset_pool.get_dataset('urbansim_constant').get_income_range_for_type(self.tnumber)
        return logical_and(self.get_dataset().get_attribute(self.income) >= min_income, 
                           self.get_dataset().get_attribute(self.income) < max_income)

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class MockConstant(object):
    def get_income_range_for_type(self, income_type):
        if income_type == 3: return (45000, 75000)
        raise StandardError("Income type should have been 3")

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_income_3"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'income': array([45000, 50000, 75000, 100000]),
            }
        )
        
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        dataset_pool._add_dataset('urbansim_constant', MockConstant())

        household = dataset_pool.get_dataset('household')
        household.compute_variables(self.variable_name, 
                                    dataset_pool=dataset_pool)
        values = household.get_attribute(self.variable_name)
        
        should_be = array( [1, 1, 0, 0] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()