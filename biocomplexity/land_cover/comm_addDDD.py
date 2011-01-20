# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize


class comm_addDDD(Variable):
    """Commercial square feet recently added in pixel between prev_year and this_year"""
    commercial_sqft = "commercial_sqft"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975

    def __init__(self, number):
        self.lag_year = int(number)
        self.commercial_sqft_lag = self.commercial_sqft + "_lag" + str(self.lag_year)
        Variable.__init__(self) # init commercial_sqft_lag first before call this, to use in dependencies

    def dependencies(self):
        return [attribute_label("gridcell", self.commercial_sqft),
                attribute_label("gridcell", self.commercial_sqft_lag),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool): 
        urbansim_commercial_sqft = dataset_pool.get_dataset('gridcell').get_attribute(self.commercial_sqft)
        urbansim_commercial_sqft_lag = dataset_pool.get_dataset('gridcell').get_attribute( \
                                                self.commercial_sqft_lag)
        urbansim_commercial_sqft_delta = urbansim_commercial_sqft-urbansim_commercial_sqft_lag
        
        new_size = urbansim_commercial_sqft_delta.size+1
        urbansim_commercial_sqft_delta = resize(urbansim_commercial_sqft_delta, new_size)
        urbansim_commercial_sqft_delta[-1] = -9999

        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        return take(urbansim_commercial_sqft_delta, lct_gridid_mapping_index)



from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.comm_add4"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct":array([1, 2, 3]),
                "devgrid_id":array([1, 1, 2])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "commercial_sqft": array([2, 7, 5]),
                "commercial_sqft_lag4": array([1, 5, 3])}}, 
            dataset = "land_cover")
        should_be = array([2-1, 2-1, 7-5])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()