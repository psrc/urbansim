# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class residential_units_when_has_eg_DDD_households(Variable):
    """"""

    def __init__(self, number):
        self.condition = "has_eg_%s_households" % number
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("residential_units"),
                my_attribute_label(self.condition)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("residential_units") * \
               self.get_dataset().get_attribute(self.condition)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.residential_units_when_has_eg_2_households"
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        parcels_table_name = 'parcels'

        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'residential_units':array([1, 1, 3, 2, 3]),
                    'number_of_households':array([2, 1, 3, 0, 5])
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'parcel':parcels
                },
            dataset = 'parcel'
            )

        should_be = array([1, 0, 3, 0, 3]) #would be a 2-D array if it spanned more than one 'directory'

        self.assert_(ma.allclose(values, should_be, rtol=1e-05),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()