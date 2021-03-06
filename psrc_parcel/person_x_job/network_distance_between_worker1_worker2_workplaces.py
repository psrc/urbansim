# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class network_distance_between_worker1_worker2_workplaces(abstract_travel_time_variable):
    """single vehicle travel distance from the workplace of worker 1 or worker 2 if worker 2 or worker 1."""

    agent_zone_id = "(psrc.person.worker1==1) * (psrc_parcel.person.workplace_of_worker2) + (psrc.person.worker2==1) * (psrc_parcel.person.workplace_of_worker1)"
    location_zone_id = "urbansim_parcel.job.zone_id"
    travel_data_attribute = "urbansim.travel_data.single_vehicle_to_work_travel_distance"

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


#class Tests(opus_unittest.OpusTestCase):
#    variable_name = "psrc_parcel.person_x_job.network_distance_between_worker1_worker2_workplaces"
#
#    def test_my_inputs(self):
#        storage = StorageFactory().get_storage('dict_storage')
#
#        storage.write_table(
#            table_name='persons',
#            table_data={
#                'person_id':array([1, 2, 3, 4, 5, 6]),
#                'household_id':array([1, 1, 2, 3, 3, 3]),
#                'job_id':array([1, 2, 3, 2, 3, 1]),
#                'member_id':array([1, 2, 1, 1, 2, 3]),
#                },
#        )
#        storage.write_table(
#            table_name='jobs',
#            table_data={
#                'job_id':array([1, 2, 3]),
#                'zone_id':array([1, 2, 3]),
#                },
#        )
#        storage.write_table(
#            table_name='households',
#            table_data={
#                'household_id':array([1,2,3,4,5]),
#                'zone_id':array([3, 1, 1, 1, 2]),
#                },
#        )
#        storage.write_table(
#            table_name='travel_data',
#            table_data={
#                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
#                'to_zone_id':  array([1,3,1,3,2,1,3,2,2]),
#                'single_vehicle_to_work_travel_distance':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
#            }
#        )
#
#        dataset_pool = DatasetPool(package_order=['psrc_parcel', 'psrc', 'urbansim'],
#                                   storage=storage)
#
#        person_x_job = dataset_pool.get_dataset('person_x_job')
#        person_x_job.compute_variables(self.variable_name,
#                                       dataset_pool=dataset_pool)
#        values = person_x_job.get_attribute(self.variable_name)
#
#        should_be = array([[1.1, 7.8, 2.2],
#                           [1.1,7.8, 2.2],
#                           [3.3, 0.5, 4.4],
#                           [3.3, 0.5, 4.4],
#                           [3.3, 0.5, 4.4],
#                           [3.3, 0.5, 4.4]])
#        print values
#        self.assert_(ma.allclose(values, should_be, rtol=1e-3),
#                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()
