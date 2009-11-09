# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.is_vacant_land import is_vacant_land as gridcell_is_vacant_land

class is_vacant_land(gridcell_is_vacant_land):
    """Returns 1 if vacant land (contains no buildings), otherwise 0."""

    number_of_buildings = "zone.number_of_agents(building)"
    
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.is_vacant_land"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
            table_name = building_types_table_name,
            table_data = {
                'building_type_id':array([1,2]), 
                'name': array(['foo', 'commercial'])
                }
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'zone':{
                    'zone_id':array([1,2,3,4]),
                    },
                'building': {
                    'building_type_id': array([1,2,1,2,1,1]),
                    'zone_id':          array([2,3,1,1,2,1])
                    },
                'building_type': building_types
                }, 
            dataset = 'zone'
            )
            
        should_be = array([0, 0, 0, 1])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()