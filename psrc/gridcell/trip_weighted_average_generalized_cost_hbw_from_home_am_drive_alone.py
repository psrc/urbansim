# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone(Variable):
    """Value of this variable from this gridcell's zone."""

    def dependencies(self):
        return [my_attribute_label("zone_id"), \
                "psrc.zone.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone"]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().get_join_data(zones, "trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone")


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.gridcell.trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1, 2, 3]),
                'zone_id': array([1, 1, 3]),
            }
        )
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id': array([1, 2, 3]),
                "trip_weighted_average_generalized_cost_hbw_from_home_am_drive_alone": array([4.1, 5.3, 6.2]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([4.1, 4.1, 6.2])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()