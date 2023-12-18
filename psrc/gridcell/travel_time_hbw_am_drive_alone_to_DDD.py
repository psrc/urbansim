# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class travel_time_hbw_am_drive_alone_to_DDD(Variable):
    """Travel time to the zone whose ID is the DDD.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "travel_time_hbw_am_drive_alone_to_" + str(int(number))
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("zone_id"), \
                "psrc.zone." + self.variable_name]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, self.variable_name)


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    def test_1(self):
        variable_name = "psrc.gridcell.travel_time_hbw_am_drive_alone_to_1"
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1, 2, 3, 4]),
                "zone_id": array([1, 1, 3, 1]),
            }
        )
        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1, 2, 3]),
                "travel_time_hbw_am_drive_alone_to_1": array([1.1, 2.2, 3.3]),
                "travel_time_hbw_am_drive_alone_to_3": array([0.1, 0.2, 0.3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(variable_name)
        
        should_be = array([1.1, 1.1, 3.3, 1.1])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + variable_name)

    def test_3(self):
        variable_name = "psrc.gridcell.travel_time_hbw_am_drive_alone_to_3"
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1, 2, 3]),
                "zone_id": array([1, 1, 3]),
            }
        )
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id': array([1, 2, 3]),
                "travel_time_hbw_am_drive_alone_to_1": array([1.1, 2.2, 3.3]),
                "travel_time_hbw_am_drive_alone_to_3": array([0.1, 0.2, 0.3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(variable_name)
        
        should_be = array([0.1, 0.1, 0.3])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + variable_name)


if __name__=='__main__':
    opus_unittest.main()