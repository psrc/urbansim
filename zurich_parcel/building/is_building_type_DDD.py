# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_building_type_DDD(Variable):
    """ Is this building of a building type DDD."""
    
    def __init__(self, building_type):
        self.building_type = building_type
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("building_type_id")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("building_type_id") == self.building_type

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.building.is_building_type_3"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
                   table_name=building_types_table_name,
                   table_data={
                    'building_type_id':array([1, 2, 3, 4]), 
                    'generic_building_type_id': array([2,3,1,1])
                    }
                )

        buildings_table_name = 'buildings'        
        storage.write_table(
                 table_name=buildings_table_name,
                 table_data={
                    'building_id':      array([1, 2, 3, 4, 5, 6]),
                    'building_type_id': array([2, 1, 2, 4, 3, 3])
                    }
                )
        dataset_pool = DatasetPool(package_order=['zurich_parcel', 'urbansim'], storage=storage)
        buildings = dataset_pool.get_dataset('building')
        
        values = buildings.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([True, False, True, False, False, False])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()