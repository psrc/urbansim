# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize


class house_addDDD(Variable):
    """Residential units recently added in pixel between prev_year and this_year"""
    residential_units = "residential_units"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975
    
    def __init__(self, number):
        self.lag_year = int(number)
        self.residential_units_lag = self.residential_units + "_lag" + str(self.lag_year)
        Variable.__init__(self) # init residential_units_lag first before call this, to use in dependencies
    
    def dependencies(self):
        # need dependency on commercial_sqft_lag_xxx too
        return [attribute_label("gridcell", self.residential_units),
                attribute_label("gridcell", self.residential_units_lag),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool): 
        urbansim_residential_units = dataset_pool.get_dataset('gridcell').get_attribute(self.residential_units)
        urbansim_residential_units_lag = dataset_pool.get_dataset('gridcell').get_attribute( \
                                                    self.residential_units_lag)
        urbansim_residential_units_delta = urbansim_residential_units-urbansim_residential_units_lag
        
        new_size = urbansim_residential_units_delta.size+1
        urbansim_residential_units_delta = resize(urbansim_residential_units_delta, new_size)
        urbansim_residential_units_delta[-1] = -9999
        
        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        return take(urbansim_residential_units_delta, lct_gridid_mapping_index)



from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.house_add5"

    def test_my_inputs(self):
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"land_cover":{
                "lct":array([1, 2, 3]),
                "devgrid_id":array([1, 1, 2])},
             "gridcell":{
                "grid_id": array([1, 2, 3]),
                "residential_units": array([8, 5, 3]),
                "residential_units_lag5": array([2, 1, 2])}}, 
            dataset = "land_cover")
        should_be = array([8-2, 8-2, 5-1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)

if __name__ == "__main__":
    opus_unittest.main()