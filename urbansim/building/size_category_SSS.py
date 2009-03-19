# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import where
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class size_category_SSS(Variable):
    """Create categories according to the sizes of buildings for this building type. 
    For buildings that are not of this type it returns 0."""
    
    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        self.is_building_type = "is_building_type_%s" % building_type_name
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.is_building_type), my_attribute_label("building_size")]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        categories = ds.categorize(attribute_name="building_size", 
                                             bins=ds.get_categories(self.building_type_name))+1 
        return where(ds.get_attribute(self.is_building_type), categories, 0)

from opus_core.tests import opus_unittest
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.resources import Resources
from numpy import array, arange
from numpy import ma
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name_prefix = "urbansim.building.size_category"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
                table_name=building_types_table_name,
                table_data={
                    'building_type_id':array([1,2]), 
                    'name': array(['residential', 'commercial']),
                    'units': array(['residential_units', 'commercial_sqft'])
                    }
            )

        buildings_table_name = 'buildings'        
        storage.write_table(
                table_name=buildings_table_name,
                table_data={
                    'building_id': arange(7)+1,
                    'building_type_id': array([1,2,1,2,1,1,2]),
                    'sqft': array([100, 350, 1000, 0, 430, 95, 750]),
                    'residential_units': array([300, 0, 100, 0, 1300, 600, 10])
                    },
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)
        buildings = BuildingDataset(in_storage=storage, in_table_name=buildings_table_name,
            resources=Resources({
                'building_categories': {
                    'residential': array([200, 500, 1200]),
                    'commercial': array([200, 500])
                    }
                })
            )
        
        variable_names = map(lambda type: '%s_%s' % (self.variable_name_prefix, type), ['commercial', 'residential'])
        buildings.compute_variables(variable_names, resources=Resources({'building_type': building_types}))

        should_be_residential = array([2, 0, 1, 0, 4, 3, 0])
        should_be_commercial = array([0, 2, 0, 1, 0, 0, 3])
        values_commercial = buildings.get_attribute(variable_names[0])
        values_residential = buildings.get_attribute(variable_names[1])
        
        self.assert_(ma.allequal(values_commercial, should_be_commercial),
            'Error in ' + variable_names[0])
        self.assert_(ma.allequal(values_residential, should_be_residential),
            'Error in ' + variable_names[1])


if __name__=='__main__':
    opus_unittest.main()