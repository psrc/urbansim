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

from numpy import where, clip
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange

class RollbackGridcells(object):
    """Uses the development_event_history and baseyear's gridcell dataset
    to produce, and save to the urbansim cache, the data for gridcell 
    dataset prior to the baseyear.
    """
    def unroll_gridcells_for_one_year(self, gridcells, dev_event_history, year_of_gridcells):
        events_idx = where(dev_event_history.get_attribute('scheduled_year') == year_of_gridcells)[0]
        if events_idx.size > 0:
            self._unroll_field('commercial_sqft', gridcells, dev_event_history, events_idx)
            self._unroll_field('industrial_sqft', gridcells, dev_event_history, events_idx)
            self._unroll_field('governmental_sqft', gridcells, dev_event_history, events_idx)
            self._unroll_field('residential_units', gridcells, dev_event_history, events_idx)
            self._unroll_field('residential_improvement_value', gridcells, dev_event_history, events_idx)
            self._unroll_field('commercial_improvement_value', gridcells, dev_event_history, events_idx)
            self._unroll_field('industrial_improvement_value', gridcells, dev_event_history, events_idx)
            self._unroll_field('governmental_improvement_value', gridcells, dev_event_history, events_idx)
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
        Currently only works for change_type of ADD.
        TODO: Have this work for other change_type values.
        """
        grid_ids = dev_event_history.get_attribute('grid_id')[events_idx]
        grid_idx = gridcells.get_id_index(grid_ids)
        attr_values = gridcells.get_attribute_by_index(attr_name, grid_idx)
        change_amounts = dev_event_history.get_attribute(attr_name)[events_idx]
        attr_values = clip(attr_values - change_amounts,
                           0, attr_values.max())
        gridcells.set_values_of_one_attribute(attr_name, attr_values, index=grid_idx)

    
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
        storage._write_dataset(
            out_table_name = gridcells_table_name,
            values = {
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
        storage._write_dataset(
            out_table_name = dev_event_history_table_name,
            values = {
                'scheduled_year':array([1999,1999,1998,1998]),
                'grid_id':array([1,3,2,3]),
                'starting_development_type_id':array([3,3,2,1]),
                'commercial_sqft':array([10,20,30,40]),
                # Rest of this data is not used by unit tests, but is required for unrolling
                'industrial_sqft':array([0,0,0,0]),
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
                     'Unexpected results: expected %s; received %s' % 
                     (array([40,50,30]), gridcells.get_attribute('commercial_sqft')))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([100,100,100])))
        self.assert_(ma.allequal(gridcells.get_attribute('development_type_id'),
                              array([3,3,3])))
        
        roller.unroll_gridcells_for_one_year(gridcells, dev_event_history, 1998)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([40,20,0])))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([100,100,100])))
        self.assert_(ma.allequal(gridcells.get_attribute('development_type_id'),
                              array([3,2,1])))
                              

if __name__ == '__main__':
    opus_unittest.main()