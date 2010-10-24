# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, clip
from opus_core.ndimage import sum as ndimage_sum
from opus_core.misc import unique

class RollbackGridcellsFromBuildings(object):
    """Uses the buildings and baseyear's gridcell dataset
    to produce, and save to the urbansim cache, the data for gridcell 
    dataset prior to the baseyear.
    """
    def unroll_gridcells_for_one_year(self, gridcells, buildings, year_of_gridcells, dataset_pool=None):
        bldgs_idx = where(buildings.get_attribute('year_built') == year_of_gridcells)[0]
        if bldgs_idx.size > 0:
            self._unroll_field('commercial_sqft', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('industrial_sqft', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('governmental_sqft', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('residential_units', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('residential_improvement_value', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('commercial_improvement_value', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('industrial_improvement_value', gridcells, buildings, bldgs_idx, dataset_pool)
            self._unroll_field('governmental_improvement_value', gridcells, buildings, bldgs_idx, dataset_pool)
        
    def _unroll_field(self, attr_name, gridcells, buildings, bldgs_idx, dataset_pool=None):
        """Unroll the values for this field.
        """
        grid_ids = buildings.get_attribute('grid_id')[bldgs_idx]
        unique_grid_ids = unique(grid_ids)
        grid_idx = gridcells.get_id_index(unique_grid_ids)
        attr_values = gridcells.get_attribute_by_index(attr_name, grid_idx)
        buildings.compute_variables("urbansim.%s.%s" % (buildings.get_dataset_name(), attr_name), 
                                    dataset_pool=dataset_pool)
        # sum the amount over the same gridcells
        change_amounts = array(ndimage_sum(buildings.get_attribute(attr_name)[bldgs_idx], labels=grid_ids,
                                            index=unique_grid_ids))
        attr_values = clip(attr_values - change_amounts,
                           0, attr_values.max())
        gridcells.set_values_of_one_attribute(attr_name, attr_values, index=grid_idx)

    
from opus_core.tests import opus_unittest

from numpy import ma
from numpy import array

from opus_core.storage_factory import StorageFactory


class RollbackGridcellsFromBuildingsTests(opus_unittest.OpusTestCase):
    def test_unrolling(self):
        from urbansim.datasets.gridcell_dataset import GridcellDataset
        from urbansim.datasets.building_dataset import BuildingDataset
        from urbansim.datasets.building_type_dataset import BuildingTypeDataset
        from opus_core.datasets.dataset_pool import DatasetPool
        from numpy import arange
        
        storage = StorageFactory().get_storage('dict_storage')

        gridcells_table_name = 'gridcells'        
        storage.write_table(
            table_name = gridcells_table_name,
            table_data = {
                'grid_id':array([1,2,3]),
                'commercial_sqft':array([50,50,50]),
                'industrial_sqft':array([100,100,100]),
                'governmental_sqft':array([0,0,0]),
                'residential_units':array([10,0,0]),
                'commercial_improvement_value':array([0,0,0]),
                'industrial_improvement_value':array([0,0,0]),
                'governmental_improvement_value':array([0,0,0]),
                'residential_improvement_value':array([0,0,0]),
                },
            )

        building_table_name = 'buildings'        
        storage.write_table(
            table_name = building_table_name,
            table_data = {
                'building_id': arange(6)+1, 
                'year_built':array([1999,1999,1998,1998,1998,1999]),
                'grid_id':array([1,3,2,3,1,1]),
                'sqft':array([10,20,30,40,0,20]),
                'residential_units':array([0,0,0,0,5,0]),
                'improvement_value':array([0,0,0,0,0,0]),
                'building_type_id': array([1,2,1,2,3,1])
                },
            )
        building_types_table_name = 'building_types'        
        storage.write_table(
            table_name = building_types_table_name,
            table_data = {
                    'building_type_id':array([1,2,3,4]), 
                    'name': array(['industrial', 'commercial', 'residential', 'governmental'])
                    }
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)
        gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)
        buildings = BuildingDataset(in_storage=storage, in_table_name=building_table_name)
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset(building_types.get_dataset_name(), building_types)
        
        roller = RollbackGridcellsFromBuildings()
        
        roller.unroll_gridcells_for_one_year(gridcells, buildings, 2000, dataset_pool)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([50,50,50])))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([100,100,100])))
        self.assert_(ma.allequal(gridcells.get_attribute('residential_units'),
                              array([10, 0, 0])))
        
        roller.unroll_gridcells_for_one_year(gridcells, buildings, 1999, dataset_pool)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([50,50,30])),
                     'Unexpected results: expected %s; received %s' % 
                     (array([50,50,30]), gridcells.get_attribute('commercial_sqft')))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([70,100,100])))
        
        roller.unroll_gridcells_for_one_year(gridcells, buildings, 1998, dataset_pool)
        self.assert_(ma.allequal(gridcells.get_attribute('commercial_sqft'),
                              array([50,50,0])))
        self.assert_(ma.allequal(gridcells.get_attribute('industrial_sqft'),
                              array([70,70,100])))
        self.assert_(ma.allequal(gridcells.get_attribute('residential_units'),
                              array([5, 0, 0])))
                              

if __name__ == '__main__':
    opus_unittest.main()