# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import resize, array

class stratify_by_SSS_and_SSS(Variable):
    """ return stratum_id from the combination of var1 and var2,
    var1 and var2 have to be either single digit integar or boolean"""

    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.parcel.%s" % self.var1,
                "psrc.parcel.%s" % self.var2]

    def compute(self, dataset_pool):
        parcels = self.get_dataset()
        is_seattle = parcels.get_attribute(self.var1)
        is_sf = parcels.get_attribute(self.var2)
        results = resize(array([9 * 100], dtype="int32"), parcels.size())   #begin with a leading 9
        results += is_seattle * 10
        results += is_sf

        return results

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.stratify_by_is_in_city_seattle_and_is_single_family_unit"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        parcels_table_name = 'parcels'

        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'is_in_city_seattle':        array([1, 0, 1, 0, 3]),
                    'is_single_family_unit':array([1, 0, 0, 1, 3]),
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'parcel':parcels,},
            dataset = 'parcel'
            )

        should_be = array([911, 900, 910, 901, 933])

        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()