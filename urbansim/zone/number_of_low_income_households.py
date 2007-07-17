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

class number_of_low_income_households(Variable):
    """Number of low-income households in this zone"""

    _return_type="int32"
    is_low_income = "is_low_income"

    def dependencies(self):
        return [attribute_label("household", self.is_low_income), 
                attribute_label("household", "zone_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.is_low_income)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_low_income_households"
    
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(
            'zones',
            {
                'zone_id': array([1, 2, 3, 4]),
            }
        )
        storage._write_dataset(
            'households',
            {
                'household_id': array([1,2,3,4,5,6]),
                'zone_id': array([1, 2, 3, 4, 2, 2]),
                'income': array([1000, 5000, 3000, 10000, 1000, 8000]), # high income: > 5000
            }
        )
        storage._write_dataset(
            'urbansim_constants',
            {
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
        
        should_be = array([1,1,0,0])
        self.assert_(ma.allclose(values, should_be, rtol=1e-20), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()