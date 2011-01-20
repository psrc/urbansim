# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from abstract_within_walking_distance import abstract_within_walking_distance

class total_buildings_SSS_space_where_tv_within_walking_distance( abstract_within_walking_distance ):
    """Caclulate the buildings space of the given type within the walking distance range. Only buildings
    are counted that have total_value > 0."""
    
    _return_type = "float32"
    
    def __init__(self, type):
        self.dependent_variable = "buildings_%s_space_where_total_value" % type
        abstract_within_walking_distance.__init__(self)

    def post_check(self, values, dataset_pool):
        self.do_check( "x >= 0", values )


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.total_buildings_residential_space_where_tv_within_walking_distance"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                'buildings_residential_space_where_total_value': array([100.0, 500.0, 1000.0, 1500.0]),
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
        
        should_be = array( [1800.0, 3100.0, 4600.0, 6000.0] )
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()