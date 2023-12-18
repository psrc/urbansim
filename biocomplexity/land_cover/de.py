# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label


class de(Variable):
    """It is de4 (see deDDD)
    """
    def dependencies(self):
        # lag variables of each of below gridcells variables
        return [my_attribute_label("de4")] 
    
    def compute(self, dataset_pool):         
        return self.get_dataset().get_attribute("de4")
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.de"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "devgrid_id":array([1, 1, 2, 2, 3])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "residential_units": array([2, 5, 4]),
                "commercial_sqft": array([4, 2, 3]),
                "industrial_sqft": array([2, 3, 5]),
                "governmental_sqft": array([4, 7, 6]),
                "residential_units_lag4": array([1, 5, 3]),
                "commercial_sqft_lag4": array([1, 2, 3]),
                "industrial_sqft_lag4": array([2, 3, 5]),
                "governmental_sqft_lag4": array([4, 7, 6])}}, 
            dataset = "land_cover")
        should_be = array([1, 1, 0, 0, 1])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()
