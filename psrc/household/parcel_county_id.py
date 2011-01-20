# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import array

class parcel_county_id(Variable):
    """county id of household"""
       
    def dependencies(self):
        return [my_attribute_label("parcel_id"),
                "opus.psrc.parcel.county"
                ]
    
    def compute(self, dataset_pool):
        parcels = dataset_pool.get_dataset('parcel')
        county_str = self.get_dataset().get_join_data(parcels, "county")
        #convert from str to int
        return array([int(x) for x in county_str])

if __name__=='__main__':
    from opus_core.tests import opus_unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import ma
    from psrc.datasets.parcel_dataset import ParcelDataset
    from opus_core.storage_factory import StorageFactory
    
    class Tests(opus_unittest.OpusTestCase):
        variable_name = "psrc.household.parcel_county_id"

        def test_my_inputs( self ):
            storage = StorageFactory().get_storage('dict_storage')
            
            parcel_table_name = 'parcel'
            
            storage.write_table(
                    table_name=parcel_table_name,
                    table_data={
                        'parcel_id':array([1, 2, 3, 4]),
                        'county':array(['033', '031', '021', '033'])
                        },
                )
                
            parcels = ParcelDataset(in_storage=storage, in_table_name=parcel_table_name)

            values = VariableTestToolbox().compute_variable( self.variable_name, \
                data_dictionary = {
                    'household':{
                        'parcel_id':array([1, 1, 2, 3, 4]),
                        },
                     'parcel':parcels,
                     },
                dataset = 'household'
                )
            should_be = array( [33, 33, 31, 21, 33] )
            
            self.assert_(ma.allclose(values, should_be, rtol=1e-7),
                'Error in ' + self.variable_name)

    opus_unittest.main()