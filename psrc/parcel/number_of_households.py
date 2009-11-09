# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class number_of_households(Variable):
    """Number of households in a given gridcell"""

    _return_type="int32"
    
    def dependencies(self):
        return [attribute_label("household", "parcel_id"), \
                my_attribute_label("parcel_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, constant=1)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('household').size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.number_of_households"
    def test(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4])
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'parcel':parcels,
                'household':{
                    'parcel_id':array([1, 2, 3, 4, 2, -1])
                    }
                },
            dataset = 'parcel'
            )
            
        should_be = array([1,2,1,1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-20),
            'Error in ' + self.variable_name)
            

if __name__=='__main__':
    opus_unittest.main()