# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ma

class travel_time_to_cbd(Variable):
    """get travel_time_to_cbd from gridcell"""

    def dependencies(self):
        return [attribute_label('gridcell', "grid_id"),
                attribute_label('gridcell', "travel_time_to_cbd"),
                my_attribute_label('grid_id')]

    def compute(self, dataset_pool):
        gcs = dataset_pool.get_dataset('gridcell')
        parcels = self.get_dataset()
        return parcels.get_join_data(gcs, "travel_time_to_cbd")

    def post_check(self, values, dataset_pool):
        units_max = dataset_pool.get_dataset('gridcell').get_attribute("travel_time_to_cbd").max()
        self.do_check("0 <= x and x <= " + str(units_max), ma.filled(values,0))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.travel_time_to_cbd"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={'parcel_id':array([1,2,3,4,5]),
                                'grid_id':array([1, 1, 3, 2, 3])
                                },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = { 
                'gridcell':{
                    'grid_id':array([1, 2, 3]),
                    'travel_time_to_cbd':array([100, 1000, 1500]),
                    },
                'parcel':parcels,
                },
            dataset = 'parcel'
            )
            
        should_be = array([100.0, 100.0, 1500.0, 1000.0, 1500.0])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()