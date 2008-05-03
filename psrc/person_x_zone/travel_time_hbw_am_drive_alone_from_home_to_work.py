#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#
from psrc.abstract_variables.abstract_travel_time_variable import abstract_travel_time_variable

class travel_time_hbw_am_drive_alone_from_home_to_work(abstract_travel_time_variable):
    """am_total_transit_time_walk_from_home_to_work"""

    agent_zone_id = "psrc.person.home_zone_id"
    location_zone_id = "urbansim.zone.zone_id"
    travel_data_attribute = "urbansim.travel_data.am_single_vehicle_to_work_travel_time"

from numpy import array
from numpy import ma
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person_x_zone.travel_time_hbw_am_drive_alone_from_home_to_work"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='persons',
            table_data={
                'person_id':array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 2, 3, 3, 3]),
                'member_id':array([1, 2, 1, 1, 2, 3]),
                },
        )
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id':array([1, 2, 3]),
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'zone_id':array([3, 1, 1, 1, 2]),
                },
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        )

        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        person_x_zone = dataset_pool.get_dataset('person_x_zone')
        person_x_zone.compute_variables(self.variable_name,
                                        dataset_pool=dataset_pool)
        values = person_x_zone.get_attribute(self.variable_name)

        should_be = array([[1.1, 7.8, 2.2],
                           [1.1,7.8, 2.2],
                           [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4],
                           [3.3, 0.5, 4.4]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-3),
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()