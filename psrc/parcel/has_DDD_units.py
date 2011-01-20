# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class has_DDD_units(Variable):
    """Boolean indicating whether the parcel has DDD residential units"""

    residential_units = "residential_units"

    def __init__(self, number):
        Variable.__init__(self)
        self.tnumber = number

    def dependencies(self):
        return [my_attribute_label(self.residential_units)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.residential_units) == self.tnumber

    def post_check(self, values, dataset_pool):
        self.do_check("x == True or x == False", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.has_2_units"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3]),
                    'residential_units':array([1, 2, 5]),
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'parcel':parcels
                },
            dataset = 'parcel'
            )
            
        should_be = array([False, True, False])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()