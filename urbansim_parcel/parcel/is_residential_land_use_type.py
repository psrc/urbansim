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

from numpy import zeros, logical_or
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_residential_land_use_type(Variable):
    """ Is this parcel of a land use type residential."""
        
    def dependencies(self):
        return ["_is_residential = parcel.disaggregate(generic_land_use_type.unit_name == 'residential_units', [land_use_type])"]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_is_residential")

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.parcel.is_residential_land_use_type"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        land_use_types_table_name = 'land_use_types'        
        storage.write_table(
                   table_name=land_use_types_table_name,
                   table_data={
                    'land_use_type_id':array([1, 2, 3, 4, 5]),
                    'generic_land_use_type_id': array([2,2,4,4, 1])
                    }
                )
        gen_land_use_types_table_name = 'generic_land_use_types'        
        storage.write_table(
                   table_name=gen_land_use_types_table_name,
                   table_data={
                    'generic_land_use_type_id':array([1, 2, 4]),
                    'unit_name': array(['foo', 'building_sqft', 'residential_units'])
                    }
                )
        parcel_table_name = 'parcels'        
        storage.write_table(
                 table_name=parcel_table_name,
                 table_data={
                    'parcel_id':array([1,2,3, 4, 5, 6]),
                    'land_use_type_id': array([2,1,2, 4, 3, 5])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        parcels = dataset_pool.get_dataset('parcel')
        
        values = parcels.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([False, False, False, True, True, False])
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()