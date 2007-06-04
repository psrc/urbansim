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
from urbansim.functions import attribute_label

class income_and_ln_lot_acres(Variable):
    """ income * ln_built_sf"""
    _return_type="float32"
    parcel_lot_acres = "lot_acres"
    hh_income = "income"
    
    def dependencies(self):
        return ["parcel_ln_lot_acres = ln(urbansim.parcel.lot_acres)",
                attribute_label("household", self.hh_income)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_income, 
                        "parcel_ln_lot_acres")


from math import log

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household_x_parcel.income_and_ln_lot_acres"
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='parcels',
            table_data={
                'parcel_id':array([1,2,3,4]),
                'lot_acres':array([1000, 1000, 3000, 2000])
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'income':array([1000, 300000, 50000, 0, 10550])
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        household_x_parcel = dataset_pool.get_dataset('household_x_parcel')
        household_x_parcel.compute_variables(self.variable_name,
                                             dataset_pool=dataset_pool)
        values = household_x_parcel.get_attribute(self.variable_name)
            
        should_be = array([[1000*log(1000), 1000*log(1000), 1000*log(3000), 1000*log(2000)], 
                           [300000*log(1000), 300000*log(1000), 300000*log(3000),300000*log(2000) ], 
                           [50000*log(1000), 50000*log(1000), 50000*log(3000),50000*log(2000)], 
                           [0, 0, 0, 0], 
                           [10550*log(1000), 10550*log(1000), 10550*log(3000), 10550*log(2000)]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()