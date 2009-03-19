# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.gridcell.buildings_SSS_units import buildings_SSS_units as gridcell_buildings_SSS_units
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class buildings_SSS_units(gridcell_buildings_SSS_units):
    """Sum of residential units from buildings of given type across zones."""
        
    def dependencies(self):
        return [attribute_label("building", self.is_type_variable), 
                attribute_label("building", "residential_units" ),
                attribute_label("building", "zone_id")]
 
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from numpy import array
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.buildings_residential_units"

    def test_my_inputs(self):
        """Total number of commercial units of buildings.
        """
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
            table_name = building_types_table_name,
            table_data = {
                'building_type_id':array([1,2]), 
                'name': array(['foo', 'residential'])
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
                    'zone_id':array([2,3,1,1,2,1]),
                    'residential_units':array([100, 350, 1000, 0, 430, 95])
                    },
                'building_type': building_types
                }, 
            dataset = 'zone'
            )
            
        should_be = array([0, 0, 350])

        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()