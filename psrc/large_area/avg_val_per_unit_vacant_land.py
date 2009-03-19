# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from avg_val_per_unit_SSS import avg_val_per_unit_SSS

class avg_val_per_unit_vacant_land(avg_val_per_unit_SSS):
    """average value per unit of vacant_land"""
    
    _return_type="float32"

    def __init__(self):
        self.type = "vacant_land"
        avg_val_per_unit_SSS.__init__(self, self.type)
        self.value = "total_value_vacant_land = large_area.aggregate(urbansim.zone.total_value_vacant_land, intermediates=[faz])"
        self.space = "vacant_land_space = large_area.aggregate(urbansim.zone.vacant_land_sqft, intermediates=[faz])"
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.large_area.avg_val_per_unit_vacant_land"
 
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='large_areas',
            table_data={
                "large_area_id":array([1, 2, 3])
                },
        )
        storage.write_table(
            table_name='fazes',
            table_data={
                "faz_id":array([1,2,3,4]),
                "large_area_id":array([1,2,3,3]),
                },
        )
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": array([1,2,3,4,5]),
                "faz_id":array([1,2,2,3,4]),
                "total_value_vacant_land":array([10, 11, 12, 13, 14]),
                "vacant_land_sqft":array([10, 1, 2, 1, 0])    
                },
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        large_area = dataset_pool.get_dataset('large_area')
        large_area.compute_variables(self.variable_name,
                                     dataset_pool=dataset_pool)
        values = large_area.get_attribute(self.variable_name)
            
        should_be = array([1, 23/3.0, 27])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()