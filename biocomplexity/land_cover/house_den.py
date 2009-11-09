# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize


class house_den(Variable):
    """Housing density - number of residential units in pixel
    in current year. This is similar to the logit variable HD1,
    but is not normalized with a log function."""
    
    residential_units = "residential_units"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975
    _return_type = "float32"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.residential_units),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool): 
        urbansim_residential_units = dataset_pool.get_dataset('gridcell').get_attribute(self.residential_units)
        new_size = urbansim_residential_units.size+1
        urbansim_residential_units = resize(urbansim_residential_units, new_size)
        urbansim_residential_units[-1] = -9999
        
        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        return take(urbansim_residential_units, lct_gridid_mapping_index) / self.acres_per_gridcell
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.house_den"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct":array([1, 2, 3]),
                "devgrid_id":array([1,1,2])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "residential_units": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([1, 1, 5]) / house_den.acres_per_gridcell
        
        self.assert_(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()