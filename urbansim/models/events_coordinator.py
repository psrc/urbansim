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

from numpy import array, logical_and, logical_or, zeros, where, arange, concatenate
from numpy import ma
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.development_type_dataset import DevelopmentTypeDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from opus_core.storage_factory import StorageFactory
from opus_core.misc import unique_values
from opus_core.model import Model
from opus_core.logger import logger

class EventsCoordinator(Model):
    """Update the location_set to reflect the changes after the development_event_set.
    
    TODO: At the moment, the event coordinator assumes that *all* development events have
    the same type_of_change for all attributes, for all events.  This restriction will 
    change once we replace the development_events and development_event_history tables with 
    the new gridcell_changes, job_changes, and development_constraint_changes tables.
    """
    
    model_name = "events_coordinator"

    def _set_development_types_for_sqft_and_units(self, location_set, development_type_set, index=None):
         """Figure out what development type a gridcell is.
         This decision is based on the number of units and the square feet in the gridcell. 
         Each development type has a range of unit and square feet values corresponding to it.
         GridcellDataset's attribute development_type_id is modified to reflect this change. 
         """
         #TODO this development_type assignment scheme is ad-hoc; may only work for PSRC sheme

         #if there is no match, assign to default_devtype
         default_devtype = 24
         
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
         location_set.compute_variables("urbansim.gridcell.non_residential_sqft")
         nonres_sqft = location_set.get_attribute_by_index("non_residential_sqft", index)
         com_sqft = location_set.get_attribute_by_index("commercial_sqft", index)
         ind_sqft = location_set.get_attribute_by_index("industrial_sqft", index) 
         gov_sqft = location_set.get_attribute_by_index("governmental_sqft", index) 
         
         gridcell_dev_type = zeros((index.size,)) + default_devtype # set to the default value of 24
         
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
         

         #if gridcell's devtype is larger than 24, keep it unchanged
         undevelopable_index = where(location_set.get_attribute('development_type_id')[index] > default_devtype)[0]
         gridcell_dev_type[undevelopable_index] = location_set.get_attribute('development_type_id')[index][undevelopable_index]

         location_set.set_values_of_one_attribute("development_type_id", gridcell_dev_type, index=index)
          
    def run(self, model_configuration, location_set, development_event_set, development_type_set, current_year):
        """Modify locations to reflect these development events, including
        updating their development_type value. 
        Returns tuple of (indices of locations that were modified,
        indices of development events that were processed).
        """
        # need to load first before using development_event_set.size()
        if not development_event_set: 
            return array([], dtype='int32'), array([], dtype='int32')

        #dict use to calculate the change in improvement value, the dict is because 
        #    the names are different in gridcell and development types
        improvement_values_to_change = {}
        attributes_to_change = []
        project_type_config = model_configuration['development_project_types']
        for project_type in project_type_config:
            units_variable = project_type_config[project_type]['units']
            if units_variable in development_event_set.get_primary_attribute_names():
                attributes_to_change.append(units_variable)
                improvement_values_to_change['%s_improvement_value' % project_type] = units_variable
            
        development_event_set.load_dataset_if_not_loaded(attributes=attributes_to_change)
        if not development_event_set.size(): 
            return array([], dtype='int32'), array([], dtype='int32')
        location_set.load_dataset_if_not_loaded(attributes=(attributes_to_change 
                                                            + improvement_values_to_change.keys()))
        gc_idx, events_idx = array([], dtype='int32'), array([], dtype='int32')
        for type_of_change in [DevelopmentEventTypeOfChange.DELETE,
                               DevelopmentEventTypeOfChange.ADD,
                               DevelopmentEventTypeOfChange.REPLACE]:
            gc_idx_new, events_idx_new = self.process_events(model_configuration,
                                                             location_set, development_event_set, 
                                                             development_type_set,
                                                             attributes_to_change, improvement_values_to_change,
                                                             type_of_change, current_year)
            gc_idx = concatenate((gc_idx, gc_idx_new))
            events_idx = concatenate((events_idx, events_idx_new))
        return unique_values(gc_idx), unique_values(events_idx)
        
    def process_events(self, model_configuration, 
                       location_set, development_event_set, 
                       development_type_set, 
                       attributes_to_change, improvement_values_to_change,
                       type_of_change, year):
        """
        Process all events of this particular type_of_change for this year.
        The default type_of_change, for when the development events do not have a 'type_of_change' attribute,
        is DevelopmentEventTypeOfChange.ADD.  Return tuple of (set of gridcells modified,
        indices of events processed).
        """
        if 'type_of_change' in development_event_set.get_primary_attribute_names():
            event_type_of_changes = development_event_set.get_attribute('type_of_change')
        else:
            default_type_of_change = model_configuration[self.model_name]['default_type_of_change']
            event_type_of_changes = zeros(development_event_set.size()) + default_type_of_change
        idx_of_events_to_process = where(logical_and(development_event_set.get_attribute("scheduled_year") == year,
                                                     event_type_of_changes == type_of_change))[0]
        if idx_of_events_to_process.size == 0:
            return array([], dtype='int32'), array([], dtype='int32')
        gc_idx_to_process = location_set.get_id_index(
            development_event_set.get_attribute_by_index(location_set.get_id_name()[0], idx_of_events_to_process))
        
        if type_of_change == DevelopmentEventTypeOfChange.ADD:
            type_of_change_str = 'add'
        elif type_of_change == DevelopmentEventTypeOfChange.DELETE:
            type_of_change_str = 'delete'
        elif type_of_change == DevelopmentEventTypeOfChange.REPLACE:
             type_of_change_str = 'replace'
        logger.log_status('Processing %d %s events' % (len(gc_idx_to_process), type_of_change_str))
        
        for attribute_name in attributes_to_change:
            attribute_values = location_set.get_attribute(attribute_name)
            if type_of_change == DevelopmentEventTypeOfChange.ADD:
                attribute_values[gc_idx_to_process] = attribute_values[gc_idx_to_process] + \
                                development_event_set.get_attribute_by_index(attribute_name, 
                                                                              idx_of_events_to_process)
            elif type_of_change == DevelopmentEventTypeOfChange.DELETE:
                attribute_values[gc_idx_to_process] = 0
            elif type_of_change == DevelopmentEventTypeOfChange.REPLACE:
                attribute_values[gc_idx_to_process] = development_event_set.get_attribute_by_index(attribute_name, 
                                                                                                    idx_of_events_to_process)

            # TODO: DGS asks "Is this next statement necessary? The gridcell values are changed
            # as a side-effect of changing the attribute_values, since dataset.get_attribute
            # returns a reference, not a copy.
            location_set.set_values_of_one_attribute(attribute_name, attribute_values)
                
        for improvement_value_name in improvement_values_to_change.keys():
            attribute_values = location_set.get_attribute(improvement_value_name)
            change = development_event_set.get_attribute_by_index(improvement_value_name, idx_of_events_to_process) * \
                   development_event_set.get_attribute_by_index(improvement_values_to_change[improvement_value_name],
                                                                 idx_of_events_to_process)
            attribute_values[gc_idx_to_process] = change + attribute_values[gc_idx_to_process]
            location_set.set_values_of_one_attribute(improvement_value_name, attribute_values)                    
                
        self._set_development_types_for_sqft_and_units(location_set, development_type_set, gc_idx_to_process)
        return gc_idx_to_process, idx_of_events_to_process
        
        
from opus_core.tests import opus_unittest

from opus_core.store.dict_storage import dict_storage
from opus_core.session_configuration import SessionConfiguration

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
        
class EventsCoordinatorTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.storage = dict_storage()
        self.storage._write_dataset(
            out_table_name = 'development_type_groups', 
            values = {
                "group_id":array([1,2,3,4]),
                "name":array(['residential', 'commercial', 
                                      'industrial', 'governmental']), 
            }
        )
        run_configuration = AbstractUrbansimConfiguration()
        self.model_configuration = run_configuration['models_configuration']
        SessionConfiguration(new_instance=True,
                             package_order=run_configuration['dataset_pool_configuration'].package_order,
                             package_order_exceptions=run_configuration['dataset_pool_configuration'].package_order_exceptions,
                             in_storage=self.storage)
        
    def tearDown(self):
        del self.storage
        
        
    def _create_simple_gridcell_set(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(out_table_name='gridcells',
            values = {
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
        
        storage._write_dataset(out_table_name='dev_events',
            values = {
                "residential_units": array([2,  0,  11]),
                "commercial_sqft": array( [0,  11, 0]),
                "industrial_sqft": array( [0,  11, 0]),
                "commercial_improvement_value": array([1, 2, 3]),
                "industrial_improvement_value": array([1, 2, 3]),
                "residential_improvement_value": array([1, 2, 3]),
                "scheduled_year": array([2000, 2000, 2001]),
                "grid_id": array([1,2,3]),
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
                                               
        storage._write_dataset(out_table_name='dev_types', values=dev_type_data)
                                               
        return mock_developmenttype(in_storage=storage, in_table_name='dev_types', other_in_table_names=[], use_groups=False)   

    def test_simple_development_event_processor(self):
        gridcell_set = self._create_simple_gridcell_set()
        dev_events_set = self._create_simple_development_event_set()
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(self.model_configuration, 
                                gridcell_set, dev_events_set, dev_types_set, 2000)

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
                                        
        storage._write_dataset(out_table_name='dev_events',
            values = {
                'residential_units': array([10, 30]),
                'commercial_sqft': array( [0,  0]),
                'industrial_sqft': array( [0,  0]),
                'commercial_improvement_value': array([1, 3]),
                'industrial_improvement_value': array([1, 3]),
                'residential_improvement_value': array([1, 3]),
                'scheduled_year': array([2000, 2000]),
                'grid_id': array([1,3]),
                'type_of_change':array([type_of_change, type_of_change])
                }
            )                                        
        dev_events_set = DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
        
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(self.model_configuration, gridcell_set, dev_events_set, dev_types_set, 2000)
        
        return gridcell_set.get_attribute("residential_units")
        
    def test_mix_of_type_of_changess(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        gridcell_set = self._create_simple_gridcell_set()
        
        storage._write_dataset(out_table_name='dev_events',
            values = {
                "residential_units":array([10, 20, 30]),
                "commercial_sqft":array([0, 11, 0]),
                "industrial_sqft":array([0, 11, 0]),
                "commercial_improvement_value":array([1, 2, 3]),
                "industrial_improvement_value":array([1, 2, 3]),
                "residential_improvement_value":array([1, 2, 3]),
                "scheduled_year":array([2000, 2000, 2000]),
                "grid_id":array([1,2,3]),
                "type_of_change":array([
                    DevelopmentEventTypeOfChange.REPLACE, 
                    DevelopmentEventTypeOfChange.ADD, 
                    DevelopmentEventTypeOfChange.DELETE,
                    ])
                }
            )
                                        
        dev_events_set = DevelopmentEventDataset(in_storage=storage, in_table_name='dev_events')
        
        dev_types_set = self._create_simple_development_types_set()
        
        EventsCoordinator().run(self.model_configuration, gridcell_set, dev_events_set, dev_types_set, 2000)
                                
        self.assert_(ma.allclose(gridcell_set.get_attribute("residential_units"), array( [10, 1+20, 0, 20]))) 
        
    def test_assignment_of_development_types_in_RAM(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(out_table_name='gridcells',
            values = {
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