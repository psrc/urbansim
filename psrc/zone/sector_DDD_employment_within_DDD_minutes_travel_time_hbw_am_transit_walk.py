# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class sector_DDD_employment_within_DDD_minutes_travel_time_hbw_am_transit_walk(abstract_access_within_threshold_variable):
    """total number of sector DDD jobs for zones within DDD minutes travel time
    """
    def __init__(self, sector, threshold):
        self.threshold = threshold
        self.travel_data_attribute  = "travel_data.am_total_transit_time_walk"
        self.zone_attribute_to_access = "urbansim.zone.number_of_jobs_of_sector_" + str(sector)
        
        abstract_access_within_threshold_variable.__init__(self)

from numpy import array, ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    def get_values(self, sector, threshold):
        self.variable_name = "psrc.zone.sector_%s_employment_within_%s_minutes_travel_time_hbw_am_transit_walk" % (sector, threshold)
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,3]),
                "number_of_jobs_of_sector_2":array([10, 1]),
                "number_of_jobs_of_sector_3":array([7, 2]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([3,3,1,1]),
                "to_zone_id": array([1,3,1,3]),
                "am_total_transit_time_walk": array([1.1, 2.2, 3.3, 4.4]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name,
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        return values

    def test_to_2(self):
        values = self.get_values(2,2)
        should_be = array([0, 10])
        self.assertTrue(ma.allequal(values, should_be),
                     msg="Error in " + self.variable_name)

    def test_to_4(self):
        values = self.get_values(3, 4)
        should_be = array([7, 9])
        self.assertTrue(ma.allequal(values, should_be),
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()