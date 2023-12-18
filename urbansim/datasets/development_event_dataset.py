# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import zeros, logical_or, logical_not, ones

class DevelopmentEventTypeOfChange(object):
    ADD = 1
    DELETE = 2
    REPLACE = 3
    available_change_types = {'A': ADD, 'D': DELETE, 'R': REPLACE}
    info_string = {ADD: 'add', DELETE: 'delete', REPLACE: 'replace'}
    
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

    def translate_change_type_to_code(self, attribute, default_value=DevelopmentEventTypeOfChange.ADD):
        """ Takes values in '%s_change_type' % attribute (which are expected to be characters contained in 
        DevelopmentEventTypeOfChange.available_change_types.keys()) and translates them to numerical code
        that corresponds to DevelopmentEventTypeOfChange.available_change_types.values().
        If the dataset does not contain the change_type attribute, it returns the default_value.
        """
        type_code_values = (default_value * ones(self.size())).astype("int16")
        if '%s_change_type' % attribute in self.get_known_attribute_names():
            type_change = self.get_attribute('%s_change_type' % attribute)
            for type_char, type_code in DevelopmentEventTypeOfChange.available_change_types.items():
                type_code_values[type_change == type_char] = type_code
        return type_code_values
                    
    def get_change_type_code_attribute(self, attribute, default_value=DevelopmentEventTypeOfChange.ADD):
        code_attr_name = '%s_change_type_code' % attribute
        if not code_attr_name in self.get_known_attribute_names():
            type_code_values = self.translate_change_type_to_code(attribute, default_value)
            self.add_attribute(name=code_attr_name, data=type_code_values)
        return self.get_attribute(code_attr_name)
        
from opus_core.tests import opus_unittest
import os
import shutil
import tempfile

from numpy import array
from numpy import ma

from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory

class DevelopmentEventDatasetTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def get_new_development_events_dataset(self, data):
        storage = StorageFactory().get_storage('dict_storage')

        development_events_table = 'development_events'
        storage.write_table(table_name=development_events_table, table_data=data)

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
        self.assertTrue(ma.allequal(ds.get_attribute('attr'), array([4,6,7])))
        self.assertEqual(3*2, ds.get_id_attribute().size)

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
        self.assertTrue(raised_exception)

if __name__ == '__main__':
    opus_unittest.main()




