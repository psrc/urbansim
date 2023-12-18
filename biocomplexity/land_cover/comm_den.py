# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize


class comm_den(Variable):
    """Commercial density - commercial square feet in pixel in
    current year. This is similar to the logit variable CD1,
    but is not normalized with a log function."""
    
    commercial_sqft = "commercial_sqft"
    industrial_sqft = "industrial_sqft"
    governmental_sqft = "governmental_sqft"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975
    _return_type = "float32"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.commercial_sqft),
                attribute_label("gridcell", self.industrial_sqft),
                attribute_label("gridcell", self.governmental_sqft),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool): 
        urbansim_commercial_sqft = dataset_pool.get_dataset('gridcell').get_attribute(self.commercial_sqft)
        urbansim_industrial_sqft = dataset_pool.get_dataset('gridcell').get_attribute(self.industrial_sqft)
        urbansim_governmental_sqft = dataset_pool.get_dataset('gridcell').get_attribute(self.governmental_sqft)
        
        total_sqft = urbansim_commercial_sqft+urbansim_industrial_sqft+urbansim_governmental_sqft
        
        new_size = total_sqft.size+1
        total_sqft = resize(total_sqft, new_size)
        total_sqft[-1] = -9999
        
        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        return take(total_sqft, lct_gridid_mapping_index) / self.acres_per_gridcell
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.comm_den"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct":array([1, 2, 3]),
                "devgrid_id":array([1, 1, 2])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "commercial_sqft": array([1, 5, 3]),
                "industrial_sqft": array([2, 3, 5]),
                "governmental_sqft": array([4, 7, 6])}}, 
            dataset = "land_cover")
        should_be = array([7, 7, 15]) / comm_den.acres_per_gridcell
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()