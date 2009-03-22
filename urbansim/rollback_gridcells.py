# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, clip, int32
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange

class RollbackGridcells(object):
    """Uses the development_event_history and baseyear's gridcell dataset
    to produce, and save to the urbansim cache, the data for gridcell 
    dataset prior to the baseyear.
    """
    attributes_to_unroll = ['commercial_sqft', 'industrial_sqft', 'governmental_sqft', 'residential_units',
                            'commercial_improvement_value', 'industrial_improvement_value',
                            'governmental_improvement_value', 'residential_improvement_value']
    # atributes that re-use the change type of other attributes
    change_types_attributes = {'commercial_improvement_value': 'commercial_sqft', 
                               'industrial_improvement_value': 'industrial_sqft',
                               'governmental_improvement_value': 'governmental_sqft',
                               'residential_improvement_value':'residential_units'}
    
    def unroll_gridcells_for_one_year(self, gridcells, dev_event_history, year_of_gridcells):
        events_idx = where(dev_event_history.get_attribute('scheduled_year') == year_of_gridcells)[0]
        if events_idx.size > 0:
            self._compute_change_type_code(dev_event_history)
            for attr in self.attributes_to_unroll:
                self._unroll_field(attr, gridcells, dev_event_history, events_idx)
            self._unroll_development_type_id(gridcells, dev_event_history, events_idx)
        
    def _unroll_development_type_id(self, gridcells, dev_event_history, events_idx):
        """Unroll the development_type_id changes.
        """
        grid_ids = dev_event_history.get_attribute('grid_id')[events_idx]
        grid_idx = gridcells.get_id_index(grid_ids)
        dev_type_ids = dev_event_history.get_attribute('starting_development_type_id')[events_idx]
        gridcells.set_values_of_one_attribute('development_type_id', dev_type_ids,
                                              index=grid_idx)
        
    def _unroll_field(self, attr_name, gridcells, dev_event_history, events_idx):
        """Unroll the values for this field, based upon its change_type.
        """
        grid_ids = dev_event_history.get_attribute('grid_id')[events_idx]
        grid_idx = gridcells.get_id_index(grid_ids)
        attr_values = gridcells.get_attribute_by_index(attr_name, grid_idx)
        change_amounts = dev_event_history.get_attribute(attr_name)[events_idx]
        change_attribute_name = '%s_change_type_code' % self.change_types_attributes.get(attr_name, attr_name)
        change_type_codes = dev_event_history.get_attribute(change_attribute_name)[events_idx]
        idx_add = where(change_type_codes == DevelopmentEventTypeOfChange.ADD)[0]
        idx_delete = where(change_type_codes == DevelopmentEventTypeOfChange.DELETE)[0]
        idx_replace = where(change_type_codes == DevelopmentEventTypeOfChange.REPLACE)[0]
        attr_values[idx_add] = clip(attr_values[idx_add] - change_amounts[idx_add].astype(int32),
                           0, attr_values[idx_add].max())
        attr_values[idx_delete] = attr_values[idx_delete] + change_amounts[idx_delete].astype(int32)
        attr_values[idx_replace] = change_amounts[idx_replace].astype(int32)
        gridcells.set_values_of_one_attribute(attr_name, attr_values, index=grid_idx)

    def _compute_change_type_code(self, dev_event_history):
        for attr in self.attributes_to_unroll:
            dev_event_history.get_change_type_code_attribute(self.change_types_attributes.get(attr, attr))
            
from opus_core.tests import opus_unittest

from numpy import ma
from numpy import array

from opus_core.storage_factory import StorageFactory


class RollbackGridcellsTests(opus_unittest.OpusTestCase):
    def test_unrolling(self):
        from urbansim.datasets.gridcell_dataset import GridcellDataset
        from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
        
        storage = StorageFactory().get_storage('dict_storage')

        gridcells_table_name = 'gridcells'        
        storage.write_table(
            table_name = gridcells_table_name,
            table_data = {
                'grid_id':array([1,2,3]),
                'development_type_id':array([3,3,3]),
                'commercial_sqft':array([50,50,50]),
                'industrial_sqft':array([100,100,100]),
                # Rest of this data is not used by unit tests, but is required for unrolling
                'governmental_sqft':array([0,0,0]),
                'residential_units':array([0,0,0]),
                'commercial_improvement_value':array([0,0,0]),
                'industrial_improvement_value':array([0,0,0]),
                'governmental_improvement_value':array([0,0,0]),
                'residential_improvement_value':array([0,0,0]),
                },
            )

        dev_event_history_table_name = 'dev_event_history'        
        storage.write_table(
            table_name = dev_event_history_table_name,
            table_data = {
                'scheduled_year':array([1999,1999,1998,1998]),
                'grid_id':array([1,3,2,3]),
                'starting_development_type_id':array([3,3,2,1]),
                'commercial_sqft':array([10,20,30,40]),
                'commercial_sqft_change_type':array(['A','A','A','A']),
                'industrial_sqft':array([20,200,99,50]),
                'industrial_sqft_change_type':array(['A','D','R','A']),
                # Rest of this data is not used by unit tests, but is required for unrolling
                'governmental_sqft':array([0,0,0,0]),
                'residential_units':array([0,0,0,0]),
                'commercial_improvement_value':array([0,0,0,0]),
                'industrial_improvement_value':array([0,0,0,0]),
                'governmental_improvement_value':array([0,0,0,0]),
                'residential_improvement_value':array([0,0,0,0]),
                },
            )

        gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)
        dev_event_history = DevelopmentEventDataset(in_storage=storage, in_table_name=dev_event_history_table_name)

        roller = RollbackGridcells()
        
        roller.unroll_gridcells_for_one_year(gridcells, dev_event_history, 2000)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([50,50,50])))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([100,100,100])))
        self.assert_(ma.allequal(gridcells.get_attribute('development_type_id'),
                              array([3,3,3])))
        
        roller.unroll_gridcells_for_one_year(gridcells, dev_event_history, 1999)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([40,50,30])),
                     'Unexpected results for 1999: expected %s; received %s' % 
                     (array([40,50,30]), gridcells.get_attribute('commercial_sqft')))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([80,100,300])))
        self.assert_(ma.allequal(gridcells.get_attribute('development_type_id'),
                              array([3,3,3])))
        
        roller.unroll_gridcells_for_one_year(gridcells, dev_event_history, 1998)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([40,20,0])))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([80,99,250])))
        self.assert_(ma.allequal(gridcells.get_attribute('development_type_id'),
                              array([3,2,1])))
                              

if __name__ == '__main__':
    opus_unittest.main()