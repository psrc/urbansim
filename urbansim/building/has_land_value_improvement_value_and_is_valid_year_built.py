# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import logical_and
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class has_land_value_improvement_value_and_is_valid_year_built(Variable):
    """Return 0 where land_value<=0 or improvement_value<=0 or year_built < urbansim_constant["absolute_min_year"] otherwise 1.
    """
    _return_type="bool8"
    is_valid_year_built = "is_valid_year_built"
    land_value = "land_value"
    improvement_value = "improvement_value"

    def dependencies(self):
        return [my_attribute_label(self.is_valid_year_built), my_attribute_label(self.land_value),
                my_attribute_label(self.improvement_value)]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return logical_and(logical_and(ds.get_attribute(self.is_valid_year_built),
                           ds.get_attribute(self.land_value) > 0), 
                           ds.get_attribute(self.improvement_value) > 0)
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.building.has_land_value_improvement_value_and_is_valid_year_built"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='buildings',
            table_data={
                'building_id': array([1,2,3,4, 5, 6]),
                'year_built': array([1995, 2000, 2005, 0, 1800, 1799]),
                'land_value': array([0,10,500,20,0,9]),
                'improvement_value': array([2,0,10,10,0,70])
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "absolute_min_year": array([1800]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        buildings = dataset_pool.get_dataset('building')
        buildings.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = buildings.get_attribute(self.variable_name)
        
        should_be = array([False, False, True, False, False, False])
        
        self.assertTrue(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()