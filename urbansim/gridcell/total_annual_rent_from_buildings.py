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
from numpy import ma
from numpy import float32

class total_annual_rent_from_buildings(Variable):
    """Total annual rent computed by dividing the total residential value of the gridcell
    by the number of residential units (quantities derived from buildings), and then dividing that figure by the 
    property value to annual cost ratio."""
    _return_type="float32"
    avg_val_per_unit = "avg_val_per_unit_residential"

    def dependencies(self):
        return [my_attribute_label(self.avg_val_per_unit)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.avg_val_per_unit) / \
               float(dataset_pool.get_dataset('urbansim_constant')["property_value_to_annual_cost_ratio"])



from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.total_annual_rent_from_buildings"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage._write_dataset(
            'gridcells',
            {
                'grid_id': array([1,2,3]),
                'avg_val_per_unit_residential': array([25, 50, 75]),
            }
        )
        storage._write_dataset(
            'urbansim_constants',
            {
                'property_value_to_annual_cost_ratio': array([50]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([25/50.0, 1, 75/50.0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()