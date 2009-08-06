# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class is_building_type_SSS(Variable):
    """ Is this building of a building type SSS."""

    
    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        Variable.__init__(self)
        
    def dependencies(self):
        return [attribute_label("building_type", "building_type_name")]
        
    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("building_type_name") == self.building_type_name][0]
        return self.get_dataset().get_attribute(building_types.get_id_name()[0]) == code

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.resources import Resources
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_zone.building.is_building_type_commercial"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
                table_name=building_types_table_name,
                table_data={
                    'building_type_id':array([0,2]), 
                    'building_type_name': array(['foo', 'commercial'])
                    }
            )

        buildings_table_name = 'buildings'        
        storage.write_table(
                table_name=buildings_table_name,
                table_data={
                    'building_id':array([1,2,3]),
                    'building_type_id': array([2,0,2])
                    }
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)
        buildings = BuildingDataset(in_storage=storage, in_table_name=buildings_table_name)
        
        buildings.compute_variables(self.variable_name, resources=Resources({'building_type':building_types}))
        
        values = buildings.get_attribute(self.variable_name)
        should_be = array([1,0,1])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()