# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import array
# from scipy.ndimage import sum as ndimage_sum
from opus_core.ndimage import sum as ndimage_sum

class employment_within_DDD_minutes_travel_time_hbw_am_drive_alone(Variable):
    """total number of jobs for zones within DDD minutes travel time,
    The travel time used is for the home-based-work am trips by auto with
    drive-alone.
    """
    def __init__(self, number):
        self.tnumber = number
        Variable.__init__(self)

    def dependencies(self):
        return ["travel_data.am_single_vehicle_to_work_travel_time",
                "urbansim.zone.number_of_jobs"]

    def compute(self, dataset_pool):
        zone_ids = self.get_dataset().get_id_attribute()
        travel_data = dataset_pool.get_dataset('travel_data')
        within_indicator = (travel_data.get_attribute('am_single_vehicle_to_work_travel_time') <= self.tnumber)

        to_zone_id = travel_data.get_attribute("to_zone_id")
        zone_index = self.get_dataset().get_id_index(to_zone_id)
        num_jobs = self.get_dataset().get_attribute('number_of_jobs')[zone_index]

        from_zone_id = travel_data.get_attribute("from_zone_id")
        results = array(ndimage_sum((within_indicator * num_jobs).astype("int32"), labels = from_zone_id, index=zone_ids))

        return results


from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    def get_values(self, number):
        self.variable_name = "eugene.zone.employment_within_%s_minutes_travel_time_hbw_am_drive_alone" % number
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='zones',
            table_data={
                "zone_id":array([1,3]),
                "number_of_jobs":array([10, 1]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([3,3,1,1]),
                "to_zone_id": array([1,3,1,3]),
                "am_single_vehicle_to_work_travel_time": array([1.1, 2.2, 3.3, 4.4]),
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
        values = self.get_values(2)
        should_be = array([0, 10])
        self.assert_(ma.allequal(values, should_be),
                     msg="Error in " + self.variable_name)

    def test_to_4(self):
        values = self.get_values(4)
        should_be = array([10, 11])
        self.assert_(ma.allequal(values, should_be),
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()