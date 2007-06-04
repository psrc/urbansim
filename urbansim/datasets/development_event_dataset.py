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

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import zeros, logical_or, logical_not

class DevelopmentEventDataset(UrbansimDataset):
    """Set of development events.
    """

    id_name_default = ["grid_id", "scheduled_year"]
    in_table_name_default = "development_events"
    out_table_name_default = "development_events"
    dataset_name = "development_event"

    def remove_non_recent_data(self, current_year, recent_years):
        """Removes records that are not in the "recent years".
        """
        years = self.get_attribute("scheduled_year")
        filter = zeros(self.size())
        for year in range(current_year-recent_years, current_year+1):
            filter = logical_or(filter, years==year)
        self.remove_elements(logical_not(filter))

class DevelopmentEventTypeOfChange(object):
    ADD = 1
    DELETE = 2
    REPLACE = 3

from opus_core.tests import opus_unittest
import os
import shutil
import tempfile

from numpy import array
from numpy import ma

from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration


class DevelopmentEventDatasetTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def get_new_development_events_dataset(self, data):
        storage = StorageFactory().get_storage('dict_storage')

        development_events_table = 'development_events'
        storage._write_dataset(development_events_table, data)

        development_events_dataset = DevelopmentEventDataset(
            in_storage = storage,
            in_table_name = development_events_table,
            id_name = ['grid_id','scheduled_year']
            )

        return development_events_dataset

    def test_can_create_test_dataset(self):
        data = {
            'grid_id':array([1,2,3]),
            'scheduled_year':array([1998,2000,2001]),
            'attr':array([4,6,7])
            }
        ds = self.get_new_development_events_dataset(data)
        self.assert_(ma.allequal(ds.get_attribute('attr'), array([4,6,7])))
        self.assertEquals(3*2, ds.get_id_attribute().size)

    def write_dataset_to_cache(self, dataset, cache_dir, year):
        # save to flt file with this year.
        SimulationState().set_current_time(year)
        year_dir = os.path.join(cache_dir, str(year))
        #os.makedirs(year_dir)
        flt_storage = StorageFactory().get_storage('flt_storage', subdir='store',
            storage_location=year_dir)
        dataset.write_dataset(out_storage=flt_storage,
                              out_table_name='development_events')

    def test_type_of_change(self):
        type_of_changes = DevelopmentEventTypeOfChange()
        self.assertEqual(type_of_changes.ADD, 1)
        self.assertEqual(type_of_changes.REPLACE, 3)
        raised_exception = False
        try:
            type_of_changes.NOT_A_MODE
        except:
            raised_exception = True
        self.assert_(raised_exception)

if __name__ == '__main__':
    opus_unittest.main()




