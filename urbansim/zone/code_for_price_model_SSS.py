# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.code_for_price_model_SSS import code_for_price_model_SSS as gridcell_code_for_price_model_SSS
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class code_for_price_model_SSS(gridcell_code_for_price_model_SSS):
    """Returns code according to vacant_land_and_building_types table for zones of the given type, 
    otherwise some other number."""
        
    def dependencies(self):
        return [my_attribute_label(self.has_type), 
                attribute_label("building_type", "name")]

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.code_for_price_model_commercial"

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
                    'zone_id':array([1,2,3]),
                    },
                'building': {
                    'building_type_id':array([1,2,1,2,1,1]),
                    'zone_id':array([2,3,1,1,2,1])
                    },
                'building_type': building_types
                }, 
            dataset = 'zone'
            )
            
        should_be = array([2, 1, 2])

        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()