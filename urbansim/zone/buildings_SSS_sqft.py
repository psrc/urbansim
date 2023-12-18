# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.buildings_SSS_sqft import buildings_SSS_sqft as gridcell_buildings_SSS_sqft
from urbansim.functions import attribute_label

class buildings_SSS_sqft(gridcell_buildings_SSS_sqft):
    """Sum of building space of given type across zones."""
        
    def dependencies(self):
        return [attribute_label("building", self.sqft_variable), 
                attribute_label("building", "zone_id")]

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.buildings_commercial_sqft"

    def test_my_inputs(self):
        """Total number of commercial sqft of buildings.
        """
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
                table_name=building_types_table_name,
                table_data={
                    'building_type_id':array([1,2]), 
                    'name': array(['foo', 'commercial'])
                    },
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'zone':{
                    'zone_id':array([1,2,3]),
                    },
                'building': {
                    'building_type_id':array([1,2,1,2,1,1]),
                    'zone_id':array([2,3,1,1,2,1]),
                    'sqft':array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': building_types
                }, 
            dataset = 'zone'
            )
            
        should_be = array([0, 0, 350])

        self.assertTrue(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()