# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class residential_units_when_has_eg_DDD_surveyed_households_and_is_in_county_DDD(Variable):
    """"""

    def __init__(self, number1, number2):
        self.condition1 = "has_eg_%s_surveyed_households" % number1
        self.condition2 = "is_in_county_%s" % number2
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("residential_units"),
                my_attribute_label(self.condition1),
                my_attribute_label(self.condition2),]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("residential_units") * \
               self.get_dataset().get_attribute(self.condition1) * \
               self.get_dataset().get_attribute(self.condition2)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.residential_units_when_has_eg_2_surveyed_households_and_is_in_county_033"
    #EXAMPLE FOR TUTORIAL
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        parcels_table_name = 'parcels'

        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'residential_units':array([1, 1, 3, 2, 3]),
                    'number_of_surveyed_households':array([2, 1, 3, 0, 5]),
                    'county':array(['033','061','035','033','033'])
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'parcel':parcels
                },
            dataset = 'parcel'
            )

        should_be = array([1, 0, 0, 0, 3]) #would be a 2-D array if it spanned more than one 'directory'

        self.assert_(ma.allclose(values, should_be, rtol=1e-05),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()