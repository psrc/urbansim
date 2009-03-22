# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import zeros, logical_or
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_land_use_type_SSS(Variable):
    """ Is this parcel of a land use type SSS."""

    
    def __init__(self, land_use_name):
        self.land_use_name = land_use_name
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("land_use_type", "land_use_name"), my_attribute_label("land_use_type_id")]
        
    def compute(self, dataset_pool):
        land_types = dataset_pool.get_dataset('land_use_type')
        parcels = self.get_dataset()
        codes = land_types.get_id_attribute()[land_types.get_attribute("land_use_name") == self.land_use_name]
        result = zeros(parcels.size(), dtype='bool8')
        for code in codes:
            result = logical_or(result, parcels.get_attribute("land_use_type_id") == code)
        return result

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.parcel.is_land_use_type_vacant"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        land_use_types_table_name = 'land_use_types'        
        storage.write_table(
                   table_name=land_use_types_table_name,
                   table_data={
                    'land_use_type_id':array([0, 2, 3, 4]), 
                    'land_use_name': array(['foo', 'vacant', 'commercial', 'vacant'])
                    }
                )

        parcel_table_name = 'parcels'        
        storage.write_table(
                 table_name=parcel_table_name,
                 table_data={
                    'parcel_id':array([1,2,3, 4, 5, 6]),
                    'land_use_type_id': array([2,0,2, 4, 3, 3])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        parcels = dataset_pool.get_dataset('parcel')
        
        values = parcels.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([1,0,1, 1, 0, 0])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()