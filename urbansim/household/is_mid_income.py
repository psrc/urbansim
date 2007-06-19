#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_mid_income(Variable):
    """Is mid_income_level <= income > low_income_level."""

    income = "income"

    def dependencies(self):
        return [my_attribute_label(self.income)]

    def compute(self, dataset_pool):
        if self.get_dataset().mid_income_level < 0: # income levels not computed yet
            self.get_dataset().calculate_income_levels(dataset_pool.get_dataset('urbansim_constant'))
        income = self.get_dataset().get_attribute(self.income)
        return (income > self.get_dataset().low_income_level) & (income <= self.get_dataset().mid_income_level)


from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household.is_mid_income"

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
        
        should_be = array( [0, 0, 1, 1] )
        
        self.assert_(ma.allequal(values, should_be,), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()