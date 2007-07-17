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
from opus_core.variables.variable import ln
from urbansim.functions import attribute_label
from numpy import reshape, where

class housing_affordability(Variable):
    """ housing_affordability=ln(income-housing_cost+1) if income-housing_cost>0,
        else, housing_affordability=income - housing_cost""" 
    _return_type="float32"
    housing_cost = "housing_cost"
    hh_income = "income"

    
    def dependencies(self):
        return [attribute_label("gridcell", self.housing_cost), 
                attribute_label("household", self.hh_income)]
        
    def compute(self, dataset_pool):
        inc = reshape(self.get_dataset().get_attribute_of_dataset(self.hh_income),
                             (self.get_dataset().get_reduced_n(), 1))
        cost = self.get_dataset().get_2d_dataset_attribute(self.housing_cost)
        I = inc-cost
        affordability = where(I > 0, ln(I+1),I)
        return affordability

        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.cost_to_income_ratio"
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'total_annual_rent': array([1000, 10000, 100000]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3]),
                'income': array([1, 20, 500]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[1000, 10000, 100000], 
                           [50, 500, 5000 ], 
                           [2, 20, 200]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()