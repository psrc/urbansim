# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import where, zeros, bool8

class is_pre_DDD(Variable):
    """Returns a boolean indicating if the parcel was built before 1940"""
    
    def __init__(self, number):
        self.year = number
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("year_built")]

    def compute(self, dataset_pool):
        year_built = self.get_dataset().get_attribute("year_built")
        results = zeros(year_built.size, dtype=bool8)
        results[where(year_built<self.year)] = 1
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.is_pre_1940"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'year_built':array([1940, 1941, 1930, 1990, 1911])
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            data_dictionary = {
                'parcel':parcels
                },
            dataset = 'parcel'
            )
            
        should_be = array([False, False, True, False, True])

        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()