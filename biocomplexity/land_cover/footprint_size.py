# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import logical_not, int32
from opus_core.variables.variable import Variable
from scipy.ndimage import correlate

class footprint_size(Variable):
    """How large is the area of valid data within the footprint
    eg: the 'real' footprint size."""
                                         
    def compute(self, dataset_pool): 
        fp = dataset_pool.get_dataset('constants')['FOOTPRINT']
        summed = correlate((logical_not(self.get_dataset().get_mask(is_2d_version=True))).astype(int32),
                                  fp,    
                                  mode='reflect')
        return self.get_dataset().flatten_by_id(summed)
        

from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "biocomplexity.land_cover.footprint_size"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='land_covers',
            table_data={
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
                "lct": array([-9999, 5, 3, 1])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['biocomplexity'],
                                   storage=storage)
        footprint = array([[0,1,0], [1,1,1], [0,1,0]])
        dataset_pool._add_dataset(
            'constant',
            {
                "FOOTPRINT": footprint,
                'AG': 10,
            }
        )

        gridcell = dataset_pool.get_dataset('land_cover')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([2, 4, 4, 5])
        
        self.assert_(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()