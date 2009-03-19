# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class percent_development_type_DDD_within_walking_distance(Variable):
    """There is exactly one variable corresponding to each defined development type dynamic_land_use_variables,
    where "?" is the development type group's NAME (e.g. residential, commercial).
    100 * [sum over c in cell.walking_radius of (if c.development_type.dynamic_land_use_variables == N then 1 else 0)] /
    (number of cells within walking distance)"""

    _return_type="float32"
    def __init__(self, type_id):
        self.type_id = type_id
        self.number_of_development_type_wwd = \
            "number_of_development_type_"+str(self.type_id)+"_within_walking_distance"
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.number_of_development_type_wwd)]

    def compute(self, dataset_pool):
        urbansim_constant = dataset_pool.get_dataset('urbansim_constant')
        return 100.0*self.get_dataset().get_attribute(self.number_of_development_type_wwd)/ \
                                             float(urbansim_constant["walking_distance_footprint"].sum())


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "randstad.gridcell.percent_development_type_12_within_walking_distance"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                'number_of_development_type_12_within_walking_distance': array([3, 5, 1, 0])
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
        
        should_be = array( [3/5.0*100.0, 
                            5/5.0*100.0, 
                            1/5.0*100.0, 
                            0/5.0*100.0] )
        
        self.assert_(ma.allclose( values, should_be, rtol=1e-7), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()