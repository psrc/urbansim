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

from psrc.zone.abstract_trip_mode import AbstractTripMode

class trip_mode_share_ride3(AbstractTripMode):
    """ Trips on a bike"""
    def __init__(self):
        AbstractTripMode.__init__(self, matrices = [
                                      'hbw_daily_share_ride3_person_trip_table',
                                      'hbnw_daily_share_ride3_person_trip_table',
                                      'nhb_daily_share_ride3_person_trip_table'
                                  ])

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.zone.trip_mode_share_ride3"
                              
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id': array([1, 2]),
            }
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                "from_zone_id": array([1,1,2,2]),
                "to_zone_id":array([1,2,1,2]),
                "hbw_daily_share_ride3_person_trip_table": array([1.1, 2.2, 3.3, 4.4]),
                "hbnw_daily_share_ride3_person_trip_table": array([2.0, 3.0, 1.0, 0.0]),
                "nhb_daily_share_ride3_person_trip_table": array([12.8, 4.5, 1.2, 8.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        zone = dataset_pool.get_dataset('zone')
        zone.compute_variables(self.variable_name, 
                               dataset_pool=dataset_pool)
        values = zone.get_attribute(self.variable_name)
        
        should_be = array([25.6, 17.9])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()