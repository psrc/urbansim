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

from cost_to_income_ratio import cost_to_income_ratio

class cost_from_buildings_to_income_ratio(cost_to_income_ratio):
    """ total_annual_rent_from_buildings /income """ 

    gc_total_annual_rent = "total_annual_rent_from_buildings"        

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.cost_from_buildings_to_income_ratio"
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage._write_dataset(
            'gridcells',
            {
                'grid_id': array([1,2,3]),
                'total_annual_rent_from_buildings': array([1000, 10000, 100000]),
            }
        )
        storage._write_dataset(
            'households',
            {
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