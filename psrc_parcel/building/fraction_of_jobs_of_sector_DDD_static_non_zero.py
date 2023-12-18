# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where
from psrc_parcel.building.fraction_of_jobs_of_sector_DDD_static import fraction_of_jobs_of_sector_DDD_static

class fraction_of_jobs_of_sector_DDD_static_non_zero(fraction_of_jobs_of_sector_DDD_static):
    """ Like its parent but sets a tiny value to all zeros so that no combination is excluded.
    """
    _return_type="float32"

    def __init__(self, *args):
        super(fraction_of_jobs_of_sector_DDD_static_non_zero, self).__init__(*args)
        self.sector_building_type_distribution[self.sector_id][where(self.sector_building_type_distribution[self.sector_id] == 0)] = 0.1
                

from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.building.fraction_of_jobs_of_sector_9_static_non_zero"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
  
        storage.write_table(
                 table_name='buildings',
                 table_data={
                    'building_id':       array([1, 2, 3, 4, 5, 6, 7]),
                    'building_type_id':  array([3, 22, 3, 5, 13, 13, 8])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        buildings = dataset_pool.get_dataset('building')
        
        values = buildings.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([21.1, 0.1, 21.1, 1.2, 40.4, 40.4, 2.3 ])/100.0
        self.assertTrue(ma.allclose(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()