# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, logical_and, logical_or, zeros, where, arange, clip #@UnresolvedImport
from numpy import ma #@UnresolvedImport
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.development_type_dataset import DevelopmentTypeDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from opus_core.storage_factory import StorageFactory
from opus_core.model import Model
from opus_core.logger import logger

class EventsCoordinator(Model):
    """Update the location_set to reflect the changes after the development_event_set.
    """
    model_name = "events_coordinator"
    #if there is no match, assign to default_devtype
    default_devtype = 24
    
    def _set_development_types_for_sqft_and_units(self, location_set, development_type_set, index=None):
        """Figure out what development type a gridcell is.
        This decision is based on the number of units and the square feet in the gridcell. 
        Each development type has a range of unit and square feet values corresponding to it.
        GridcellDataset's attribute development_type_id is modified to reflect this change. 
        """
        #TODO this development_type assignment scheme is ad-hoc; may only work for PSRC sheme
   

        
        location_set.load_dataset_if_not_loaded(attributes=["residential_units", "industrial_sqft", 
                                              "commercial_sqft", "governmental_sqft"])
        
        #because of lazy loading, to get development_type_set.size() we may need to access an array first
        min_units = development_type_set.get_attribute("min_units")
        max_units = development_type_set.get_attribute("max_units")
        min_sqft = development_type_set.get_attribute("min_sqft")
        max_sqft = development_type_set.get_attribute("max_sqft")
        ids = development_type_set.get_attribute("development_type_id")
        
        if index is None:
            index = arange(location_set.size())
        
        units = location_set.get_attribute_by_index("residential_units", index)
        location_set.compute_variables("urbansim.%s.non_residential_sqft" % location_set.get_dataset_name())
        nonres_sqft = location_set.get_attribute_by_index("non_residential_sqft", index)
        # these are unused?
        com_sqft = location_set.get_attribute_by_index("commercial_sqft", index)
        ind_sqft = location_set.get_attribute_by_index("industrial_sqft", index) 
        gov_sqft = location_set.get_attribute_by_index("governmental_sqft", index) 
        
        gridcell_dev_type = zeros((index.size,)) + self.default_devtype # set to the default value
        
        # go through the developmenttypes and assign them to the gridcells
        development_type_set.compute_variables(["urbansim.development_type.is_in_development_type_group_residential",
                                                "urbansim.development_type.is_in_development_type_group_mixed_use",
                                                "urbansim.development_type.is_in_development_type_group_commercial",
                                                "urbansim.development_type.is_in_development_type_group_industrial",
                                                "urbansim.development_type.is_in_development_type_group_governmental"
                                                ])
        #name_list1 = ['R1','R2','R3','R4','R5','R6','R7','R8','M1','M2','M3','M4','M5','M6','M7','M8']
        # devtypes in development type group residential apply the following rules
        for dt_index in where(logical_or(development_type_set.get_attribute("is_in_development_type_group_residential"), 
                                         development_type_set.get_attribute("is_in_development_type_group_mixed_use")))[0]:
            where_this_type = where(logical_and(min_units[dt_index] <= units, units <= max_units[dt_index]) * 
                                    logical_and(min_sqft[dt_index] <= nonres_sqft, nonres_sqft <= max_sqft[dt_index])
                                    )
            gridcell_dev_type[where_this_type] = ids[dt_index]
        
        #name_list2 = ['C1','C2','C3']
        # devtypes in in development type group commercial apply the following rules
        for dt_index in where(development_type_set.get_attribute("is_in_development_type_group_commercial"))[0]:
            where_this_type = where(logical_and(min_units[dt_index] <= units, units <= max_units[dt_index]) * 
                                    logical_and(min_sqft[dt_index] <= nonres_sqft, nonres_sqft <= max_sqft[dt_index])
                                    )
            gridcell_dev_type[where_this_type] = ids[dt_index]
        
        #name_list3 = ['I1','I2','I3']
        # devtypes in in development type group industrial apply the following rules
        for dt_index in where(development_type_set.get_attribute("is_in_development_type_group_industrial"))[0]:
            where_this_type = where(logical_and(min_units[dt_index] <= units, units <= max_units[dt_index]) * 
                                    logical_and(min_sqft[dt_index] <= nonres_sqft, nonres_sqft <= max_sqft[dt_index])
                                    )
            gridcell_dev_type[where_this_type] = ids[dt_index]
   
        #name_list4 = ['GV']
        # devtypes in in development type group governmental apply the following rules
        for dt_index in where(development_type_set.get_attribute("is_in_development_type_group_governmental"))[0]:
            where_this_type = where(logical_and(min_units[dt_index] <= units, units <= max_units[dt_index]) * 
                                    logical_and(min_sqft[dt_index] <= nonres_sqft, nonres_sqft <= max_sqft[dt_index])
                                    )
            gridcell_dev_type[where_this_type] = ids[dt_index]
        
   
        #if gridcell's devtype is larger than the default, keep it unchanged
        undevelopable_index = where(location_set.get_attribute('development_type_id')[index] > self.default_devtype)[0]
        gridcell_dev_type[undevelopable_index] = location_set.get_attribute('development_type_id')[index][undevelopable_index]
   
        location_set.set_values_of_one_attribute("development_type_id", gridcell_dev_type, index=index)
          
    def run(self, location_set, development_event_set, 
            development_type_set, current_year, model_configuration = None,
            development_models = None, models_configuration = None):
        """Modify locations to reflect these development events, including
        updating their development_type value. 
        Returns tuple of (indices of locations that were modified,
        indices of development events that were processed).
        """
        # argument check to resolve configuration of development project types
        if development_models is not None and models_configuration is None:
            raise StandardError('Configurations that pass a list of development'
                                ' models (argument: "development_models") must '
                                'also pass a reference to the entire models '
                                'configuration (argument: "models_'
                                'configuration") note: plural model[s].')

        dev_model_configs = {}
        model_config_used = None
        if development_models is None: # assume this means that we use old conf
            # try to get a reference to the external information for development
            # project types
            try: 
                dev_model_configs = model_configuration['development_project_types']
                model_config_used = model_configuration
            except:
                dev_model_configs = models_configuration['development_project_types']
                model_config_used = models_configuration
        else:
            # pull in information from the specified development project models
            model_config_used = models_configuration
            for dev_proj_model in development_models:
                model_conf = model_config_used[dev_proj_model]
                proj_type = model_conf['controller']['init']['arguments']['project_type'].strip('\'"')
                dev_model_configs[proj_type] = {}
                dev_model_configs[proj_type]['units'] = model_conf['controller']['init']['arguments']['units'].strip('\'"')
                dev_model_configs[proj_type]['residential'] = model_conf['controller']['init']['arguments']['residential']
                dev_model_configs[proj_type]['categories'] = model_conf['controller']['prepare_for_estimate']['arguments']['categories']

        # need to load first before using development_event_set.size()
        if not development_event_set or (development_event_set.size() == 0): 
            return array([], dtype='int32'), array([], dtype='int32')

        improvement_values_to_change = {}
        attributes_to_change = []

        for project_type in dev_model_configs:
            units_variable = dev_model_configs[project_type]['units']
            if units_variable in development_event_set.get_primary_attribute_names():
                attributes_to_change.append(units_variable)
                improvement_values_to_change[units_variable] = '%s_improvement_value' % project_type
                
        return self.process_events(model_config_used, location_set, development_event_set, 
                                                             development_type_set,
                                                             attributes_to_change, improvement_values_to_change, 
                                                             current_year)
        
    def process_events(self, model_configuration, 
                       location_set, development_event_set, 
                       development_type_set, 
                       attributes_to_change, improvement_values_to_change, year):
        """
        Process all events of this particular type_of_change for this year.
        The default type_of_change, for when the development events do not have a 'change_type' attribute,
        is set in model_configuration or DevelopmentEventTypeOfChange.ADD.  Return tuple of (set of gridcells modified,
        indices of events processed).
        """
        idx_of_events_this_year = development_event_set.get_attribute("scheduled_year") == year
        if idx_of_events_this_year.sum() == 0:
            return array([], dtype='int32'), array([], dtype='int32')
        idx_of_events_to_process = zeros(development_event_set.size(), dtype='bool8')
        gc_idx_to_process = zeros(location_set.size(), dtype='bool8')
        location_ids_in_event_set = development_event_set.get_attribute(location_set.get_id_name()[0])
        
        for attribute_name in attributes_to_change:
            attribute_values = location_set.get_attribute(attribute_name)
            event_attribute_values = development_event_set.get_attribute(attribute_name)
            event_type_of_changes = development_event_set.get_change_type_code_attribute(attribute_name,
                                            default_value=model_configuration[self.model_name].get('default_type_of_change',
                                                                                       DevelopmentEventTypeOfChange.ADD))
            improvement_value_attribute = improvement_values_to_change[attribute_name]
            improvement_values = location_set.get_attribute(improvement_value_attribute)
            event_improvement_values = development_event_set.get_attribute(improvement_value_attribute)
            idx_add = logical_and(idx_of_events_this_year, event_type_of_changes == DevelopmentEventTypeOfChange.ADD)
            idx_delete = logical_and(idx_of_events_this_year, event_type_of_changes == DevelopmentEventTypeOfChange.DELETE)
            idx_replace = logical_and(idx_of_events_this_year, event_type_of_changes == DevelopmentEventTypeOfChange.REPLACE)
            logger.log_status('Processing %s: %d %s events, %d %s events, %d %s events.' % (attribute_name, 
                            idx_add.sum(), DevelopmentEventTypeOfChange.info_string[DevelopmentEventTypeOfChange.ADD],
                            idx_delete.sum(), DevelopmentEventTypeOfChange.info_string[DevelopmentEventTypeOfChange.DELETE],
                            idx_replace.sum(), DevelopmentEventTypeOfChange.info_string[DevelopmentEventTypeOfChange.REPLACE],
                                                                                            ))
            idx_of_events_to_process = idx_of_events_to_process + idx_add + idx_delete + idx_replace
            #add
            gc_idx_to_process_add = location_set.get_id_index(location_ids_in_event_set[idx_add])
            attribute_values[gc_idx_to_process_add] = attribute_values[gc_idx_to_process_add] + \
                                                                            event_attribute_values[idx_add]
            improvement_values[gc_idx_to_process_add] = improvement_values[gc_idx_to_process_add] + \
                                            event_improvement_values[idx_add] * event_attribute_values[idx_add]
            gc_idx_to_process[gc_idx_to_process_add] = True
            #demolish
            if idx_delete.sum() > 0:
                gc_idx_to_process_delete = location_set.get_id_index(location_ids_in_event_set[idx_delete])
                attribute_values[gc_idx_to_process_delete] = clip(attribute_values[gc_idx_to_process_delete] - \
                                  event_attribute_values[idx_delete], 0, attribute_values[gc_idx_to_process_delete].max())
                improvement_values[gc_idx_to_process_delete] = clip(improvement_values[gc_idx_to_process_delete] - \
                                  event_improvement_values[idx_delete] * event_attribute_values[idx_delete], 0, 
                                                                improvement_values[gc_idx_to_process_delete].max())
                gc_idx_to_process[gc_idx_to_process_delete] = True
            # replace
            gc_idx_to_process_replace = location_set.get_id_index(location_ids_in_event_set[idx_replace])
            attribute_values[gc_idx_to_process_replace] = event_attribute_values[idx_replace]
            improvement_values[gc_idx_to_process_replace] = event_improvement_values[idx_replace] * \
                                                                    event_attribute_values[idx_replace]
            gc_idx_to_process[gc_idx_to_process_replace] = True
            
            location_set.set_values_of_one_attribute(attribute_name, attribute_values)
            location_set.set_values_of_one_attribute(improvement_value_attribute, improvement_values)
            
                     
        gc_idx_to_process = where(gc_idx_to_process)[0]
        self._set_development_types_for_sqft_and_units(location_set, development_type_set, gc_idx_to_process)
        return gc_idx_to_process, where(idx_of_events_to_process)[0]
        
        
from opus_core.tests import opus_unittest

from opus_core.store.dict_storage import dict_storage
from opus_core.session_configuration import SessionConfiguration

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
        
class EventsCoordinatorTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = dict_storage()
        self.storage.write_table(
            table_name='development_type_groups', 
            table_data={
                "group_id":array([1,2,3,4]),
                "name":array(['residential', 'commercial', 
                                      'industrial', 'governmental']), 
            }
        )
        run_configuration = AbstractUrbansimConfiguration()
        self.model_configuration = run_configuration['models_configuration']
        SessionConfiguration(new_instance=True,
                             package_order=run_configuration['dataset_pool_configuration'].package_order,
                             in_storage=self.storage)
        
    def tearDown(self):
        del self.storage
        
        
    def _create_simple_gridcell_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'residential_units': array([2, 1, 12, 20]),
                'commercial_sqft': array([3, 1,  0, 4]),
                'industrial_sqft': array([0, 10, 0, 4]),
                'governmental_sqft': array([0, 0, 0, 0]),
                'commercial_improvement_value': array([1, 2, 3, 389]),
                'industrial_improvement_value': array([1, 2, 3, 78]),
                'residential_improvement_value': array([1, 2, 3, 3]),
                'development_type_id': array([1, 3, 5, 6]),
                'grid_id': array([1, 2, 3, 4])
                }
            )
            
        return GridcellDataset(in_storage=storage, in_table_name='gridcells')
    
    def _create_simple_development_event_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='dev_events',
            table_data={
                "residential_units": array([2,  0,  11, 10]),
                "commercial_sqft": array( [0,  11, 0, 0]),
                "industrial_sqft": array( [0,  11, 0, 0]),
                "commercial_improvement_value": array([1, 2, 3, 0]),
                "industrial_improvement_value": array([1, 2, 3, 0]),
                "residential_improvement_value": array([1, 2, 3, 10]),
                "scheduled_year": array([2000, 2000, 2001, 2001]),
                "grid_id": array([1,2,3, -1]),
                # default type_of_change is ADD
                }
            )
            
        return DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
    
    def _create_simple_development_types_set(self, dev_type_data=None):
        storage = StorageFactory().get_storage('dict_storage')
        
        class mock_developmenttype(DevelopmentTypeDataset):
            groups = {
                      #"development_type_id":"group_id"
                      1:[1,2],
                      2:[2],
                      3:[2]
                      }
            
            def get_types_for_group(self, group):
                ids = arange(self.size())+1
                is_group = array(map(lambda idx: group in self.groups[idx], ids))
                return ids[where(is_group)]
            
        #example dev_type_data
        if dev_type_data is None:
            dev_type_data = {
                'development_type_id':array([1,2,3]),
                'min_units':array([2,  0,  11]),
                'max_units':array([10, 20, 20]),
                'min_sqft':array( [0,  11, 0]),
                'max_sqft':array( [10, 50, 10]),
                }
                                               
        storage.write_table(table_name='dev_types', table_data=dev_type_data)
                                               
        return mock_developmenttype(in_storage=storage, in_table_name='dev_types', other_in_table_names=[], use_groups=False)   

    def test_simple_development_event_processor(self):
        gridcell_set = self._create_simple_gridcell_set()
        dev_events_set = self._create_simple_development_event_set()
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(gridcell_set, dev_events_set, dev_types_set, 2000,
                                model_configuration = self.model_configuration)

        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_units"), array( [4, 1, 12, 20]))) 
        self.assert_(ma.allclose(gridcell_set.get_attribute("commercial_sqft"), array( [3, 12, 0, 4])))
        self.assert_(ma.allclose(gridcell_set.get_attribute("industrial_sqft"), array( [0, 21, 0, 4]))) 
        self.assert_(ma.allclose(gridcell_set.get_attribute("commercial_improvement_value"), array( [1, 24, 3, 389]))) 
        self.assert_(ma.allclose(gridcell_set.get_attribute("industrial_improvement_value"), array( [1, 24, 3, 78]))) 
        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_improvement_value"), array( [3, 2, 3, 3])))
        self.assert_(ma.allclose(gridcell_set.get_attribute("development_type_id"), array( [1, 2, 5, 6]))) 
        self.assert_(ma.allclose(gridcell_set.get_attribute("grid_id"), array( [1, 2, 3, 4]))) 
        
    def test_replace_type_of_changes(self):
        values = self.do_type_of_changes_test(DevelopmentEventTypeOfChange.REPLACE)
        self.assert_(ma.allclose(values, array( [10, 1, 30, 20]))) 
        
    def test_delete_type_of_changes(self):
        values = self.do_type_of_changes_test(DevelopmentEventTypeOfChange.DELETE)
        self.assert_(ma.allclose(values, array( [0, 1, 0, 20]))) 
        
    def test_add_type_of_changes(self):
        values = self.do_type_of_changes_test(DevelopmentEventTypeOfChange.ADD)
        self.assert_(ma.allclose(values, array( [12, 1, 42, 20]))) 
        
    def do_type_of_changes_test(self, type_of_change):
        storage = StorageFactory().get_storage('dict_storage')
        
        gridcell_set = self._create_simple_gridcell_set()
                                        
        storage.write_table(
            table_name='dev_events',
            table_data={
                'residential_units': array([10, 30]),
                'commercial_sqft': array( [0,  0]),
                'industrial_sqft': array( [0,  0]),
                'commercial_improvement_value': array([1, 3]),
                'industrial_improvement_value': array([1, 3]),
                'residential_improvement_value': array([1, 3]),
                'scheduled_year': array([2000, 2000]),
                'grid_id': array([1,3]),
                'residential_units_change_type_code':array([type_of_change, type_of_change]),
                'commercial_sqft_change_type_code':array([type_of_change, type_of_change]),
                'industrial_sqft_change_type_code':array([type_of_change, type_of_change])
                }
            )                                        
        dev_events_set = DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
        
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(gridcell_set, dev_events_set, dev_types_set, 2000, model_configuration = self.model_configuration)
        
        return gridcell_set.get_attribute("residential_units")
        
    def test_mix_of_type_of_changes(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        gridcell_set = self._create_simple_gridcell_set()
        
        storage.write_table(
            table_name='dev_events',
            table_data={
                "residential_units":array([10, 20, 30]),
                "commercial_sqft":array([0, 11, 0]),
                "industrial_sqft":array([0, 11, 0]),
                "commercial_improvement_value":array([1, 2, 3]),
                "industrial_improvement_value":array([1, 2, 3]),
                "residential_improvement_value":array([1, 2, 3]),
                "scheduled_year":array([2000, 2000, 2000]),
                "grid_id":array([1,2,3]),
                "residential_units_change_type_code":array([
                    DevelopmentEventTypeOfChange.REPLACE, 
                    DevelopmentEventTypeOfChange.ADD, 
                    DevelopmentEventTypeOfChange.DELETE,
                    ])
                }
            )
                                        
        dev_events_set = DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
        
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(gridcell_set, dev_events_set, dev_types_set, 2000, model_configuration = self.model_configuration)
                                
        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_units"), array( [10, 1+20, 0, 20]))) 
        
    def test_different_changes_for_different_units(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        gridcell_set = self._create_simple_gridcell_set()
        
        storage.write_table(
            table_name='dev_events',
            table_data={
                "residential_units":array([10, 20, 6]),
                "commercial_sqft":array([4, 11, 1]),
                "industrial_sqft":array([0, 11, 0]),
                "commercial_improvement_value":array([1, 2, 3]),
                "industrial_improvement_value":array([1, 2, 3]),
                "residential_improvement_value":array([3, 5, 7]),
                "scheduled_year":array([2000, 2000, 2000]),
                "grid_id":array([1,2,3]),
                "residential_units_change_type_code":array([
                    DevelopmentEventTypeOfChange.REPLACE, 
                    DevelopmentEventTypeOfChange.ADD, 
                    DevelopmentEventTypeOfChange.DELETE,
                    ]),
                "commercial_sqft_change_type_code":array([
                    DevelopmentEventTypeOfChange.DELETE, 
                    DevelopmentEventTypeOfChange.ADD, 
                    DevelopmentEventTypeOfChange.REPLACE,
                    ])
                }
            )
                                        
        dev_events_set = DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
        
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(gridcell_set, dev_events_set, dev_types_set, 2000, model_configuration = self.model_configuration)
                                
        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_units"), array( [10, 1+20, 6, 20])))
        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_improvement_value"), array( [30, 102, 0, 3])))
        self.assert_(ma.allclose(gridcell_set.get_attribute("commercial_sqft"), array( [0, 12, 1, 4])))
        self.assert_(ma.allclose(gridcell_set.get_attribute("commercial_improvement_value"), array( [0, 24, 3, 389]))) 
        
    def test_assignment_of_development_types_in_RAM(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'residential_units':array([2, 1, 12, 20]), 
                'industrial_sqft':array([0, 10, 0, 4]), 
                'commercial_sqft':array([3, 1,  0, 4]), 
                'governmental_sqft':array([0, 0,  0, 0]), 
                'development_type_id':array([-1, -1, -1, -1]), 
                'grid_id':array([1, 2, 3, 4]),
                }
            )
        gridcell_set = GridcellDataset(in_storage=storage, in_table_name='gridcells')
        
        dev_type_data = {
            'development_type_id':array([1,2,3]), 
            'min_units':array([2,  0,  11]), 
            'max_units':array([10, 20, 20]), 
            'min_sqft':array([0,  11, 0]), 
            'max_sqft':array( [10, 15, 10])
            }
        dev_set = self._create_simple_development_types_set(dev_type_data)

        EventsCoordinator()._set_development_types_for_sqft_and_units(gridcell_set, dev_set)
        self.assertEqual(ma.allclose(gridcell_set.get_attribute("development_type_id"), array([1,2,3,3])), True)
        

if __name__=="__main__":
    opus_unittest.main()
