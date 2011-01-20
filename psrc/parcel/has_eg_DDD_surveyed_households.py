# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_eg_DDD_surveyed_households(Variable):
    '''has equal to or more than DDD households in parcel? '''
    cars = 'cars'
    
    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number
        
    def dependencies(self):
        return [my_attribute_label('number_of_surveyed_households')]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute('number_of_surveyed_households') >= self.tnumber

    def post_check(self, values, dataset_pool):
        self.do_check('x == 0 or x==1', values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from psrc.parcel.number_of_surveyed_households import number_of_surveyed_households
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = 'psrc.parcel.has_eg_1_surveyed_households'
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
        
        sid = number_of_surveyed_households.surveyed_households_starting_id
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'parcel':parcels,
                'household':{
                'parcel_id':array([1, 2, 3, 4, 2, 2]),
                    'household_id':array([sid, sid+11, sid-1, sid-5, sid+7, sid-6]), 
                    }
                },
            dataset = 'parcel'
            )
            
        should_be = array([1,1,0,0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-20),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()