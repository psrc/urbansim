# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class housing_value(Variable):
    """ (land_value + improvement_value) / residential_units."""
    
    land_value = "land_value"
    improvement_value = "improvement_value"
    residential_units = "residential_units"
    
    def dependencies(self):
        return [my_attribute_label(self.land_value), \
                my_attribute_label(self.improvement_value), \
                my_attribute_label(self.residential_units)]
        
    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        residential_units = parcels.get_attribute(self.residential_units)
        return ma.filled((parcels.get_attribute(self.land_value) + \
                       parcels.get_attribute(self.improvement_value)) /\
                      ma.masked_where(residential_units==0, residential_units.astype(float32)), 0.0)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.housing_value"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'residential_units':array([2,0,1,4,7]),
                    'land_value':array([100,11,20,0,90]),
                    'improvement_value':array([20,10,17,40,17]),
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'parcel':parcels
                }, 
            dataset = 'parcel'
            )
            
        should_be = array([60, 0, 37, 10, 15.28571415])
        
        self.assert_(ma.allclose(values, should_be),
            'Error in ' + self.variable_name)
        

if __name__=='__main__':
    opus_unittest.main()