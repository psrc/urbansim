# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class home_zone_id_from_parcel_id(Variable):
    """The zone_id of household's home compute through its parcel_id."""
    
    def dependencies(self):
        return [my_attribute_label('parcel_id'), 
                attribute_label('parcel', 'zone_id')]
        
    def compute(self, dataset_pool):
        parcels = dataset_pool.get_dataset('parcel')
        return self.get_dataset().get_join_data(parcels, name='zone_id')
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = 'psrc.household.home_zone_id_from_parcel_id'
    
    def test_my_inputs(self):
        zone_id = array([1,1,3,2])
        parcel_id = array([1,2,3,4])
        
        parcel_storage = StorageFactory().get_storage('dict_storage')
        parcel_table_name = 'parcel'
        parcel_storage.write_table(
                table_name=parcel_table_name,
                table_data={
                    'parcel_id':parcel_id,
                    'zone_id':zone_id
                    }
            )
        
        parcels = ParcelDataset(in_storage=parcel_storage, in_table_name=parcel_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {'household':{ \
                'parcel_id':parcel_id}, \
             'parcel':parcels}, 
            dataset = 'household')
        should_be = zone_id
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                         True, msg = 'Error in ' + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()