# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize


class devt(Variable):
    """Land cover development type id"""

    development_type_id = "development_type_id"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975
    
    def dependencies(self):
        return [attribute_label("gridcell", self.development_type_id),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool): 
        urbansim_development_type_id = dataset_pool.get_dataset('gridcell').get_attribute(self.development_type_id)
        devt_new_size = urbansim_development_type_id.size + 1
        urbansim_development_type_id = resize(urbansim_development_type_id, devt_new_size)
        urbansim_development_type_id[-1] = -9999
        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        return take(urbansim_development_type_id, lct_gridid_mapping_index)
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.devt"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                #"lct":array([1, 2, 3]),
                "devgrid_id":array([1, 1, 2, -9999])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "development_type_id": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([1, 1, 5, -9999])
        
        self.assertTrue(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()
