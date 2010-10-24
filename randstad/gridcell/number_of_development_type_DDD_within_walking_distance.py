# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.ndimage import correlate
from numpy import ma

class number_of_development_type_DDD_within_walking_distance(Variable):
    """Total number of locations within walking distance that are of DDD development type"""

    def __init__(self, type_id):
        self.type_id = type_id
        self.is_development_type = "is_development_type_" + str(self.type_id)
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.is_development_type)]

    def compute(self, dataset_pool):
        summed = correlate(ma.filled(self.get_dataset().get_2d_attribute(self.is_development_type),0.0), \
                           dataset_pool.get_dataset('urbansim_constant')["walking_distance_footprint"], mode="reflect")
        return self.get_dataset().flatten_by_id(summed)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from numpy import array

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "randstad.gridcell.number_of_development_type_11_within_walking_distance"
    #"1" in this case is the group number. was originally DDD, but have to specify it since this is a test, and the
    #"parent code" isn't actually invoked
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                'is_development_type_11': array([1, 1, 1, 0])
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
                "acres": array([105.0]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([5, 4, 4, 2])
        
        self.assert_(ma.allclose( values, should_be, rtol=1e-7), 
                     msg = "Error in " + self.variable_name)

    
if __name__=='__main__':
    opus_unittest.main()