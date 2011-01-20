# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import take, where, arange, zeros, resize, array


class deDDD(Variable):
    """DE: has development event occurred between current and DDD year ago - binary
        Ths variable is computed base on observing any development in residential_units,
            governmental_sqft, industrial_sqft and commercial_sqft. If non of those
            has changed between the current year and previous year (using lag, lag_year means
            many year before current year), de has a zero value, otherwise a one.
    """

    commercial_sqft = "commercial_sqft"
    industrial_sqft = "industrial_sqft"
    governmental_sqft = "governmental_sqft"
    residential_units = "residential_units"
    land_cover_grid_id_index = "land_cover_grid_id_index"
    acres_per_gridcell = 5.55975
    
    def __init__(self, number):
        self.lag_year = int(number)
        self.residential_units_lag = self.residential_units + "_lag" + str(self.lag_year)
        self.commercial_sqft_lag = self.commercial_sqft + "_lag" + str(self.lag_year)
        self.industrial_sqft_lag = self.industrial_sqft + "_lag" + str(self.lag_year)
        self.governmental_sqft_lag = self.governmental_sqft + "_lag" + str(self.lag_year)
        Variable.__init__(self) # init self.xxx above first before call this, to use in dependencies
    
    def dependencies(self):
        # lag variables of each of below gridcells variables
        return [attribute_label("gridcell", self.commercial_sqft),
                attribute_label("gridcell", self.industrial_sqft),
                attribute_label("gridcell", self.governmental_sqft),
                attribute_label("gridcell", self.residential_units),
                attribute_label("gridcell", self.commercial_sqft_lag),
                attribute_label("gridcell", self.industrial_sqft_lag),
                attribute_label("gridcell", self.governmental_sqft_lag),
                attribute_label("gridcell", self.residential_units_lag),
                my_attribute_label(self.land_cover_grid_id_index)] 
    
    def compute(self, dataset_pool):         
        residential_units_delta = dataset_pool.get_dataset('gridcell').get_attribute(self.residential_units) - \
                                  dataset_pool.get_dataset('gridcell').get_attribute(self.residential_units_lag)
        commercial_sqft_delta = dataset_pool.get_dataset('gridcell').get_attribute(self.commercial_sqft) - \
                                dataset_pool.get_dataset('gridcell').get_attribute(self.commercial_sqft_lag)
        industrial_sqft_delta = dataset_pool.get_dataset('gridcell').get_attribute(self.industrial_sqft) - \
                                dataset_pool.get_dataset('gridcell').get_attribute(self.industrial_sqft_lag)
        governmental_sqft_delta = dataset_pool.get_dataset('gridcell').get_attribute(self.governmental_sqft) - \
                                  dataset_pool.get_dataset('gridcell').get_attribute(self.governmental_sqft_lag)
        
        is_developed = array([int(c!=0 or r!=0 or g!=0 or i!=0) for (r,c,g,i) in zip(residential_units_delta, \
                commercial_sqft_delta, governmental_sqft_delta, industrial_sqft_delta)])
        
        new_size = is_developed.size + 1
        is_developed = resize(is_developed, new_size)
        is_developed[-1] = -9999
        
        lct_gridid_mapping_index = self.get_dataset().get_attribute(self.land_cover_grid_id_index)
        
        return take(is_developed, lct_gridid_mapping_index)
    

from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from biocomplexity.tests.expected_data_test import ExpectedDataTest
from opus_core.storage_factory import StorageFactory
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
    variable_name = "biocomplexity.land_cover.de3"

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
                "residential_units_lag3": array([1, 5, 3]),
                "commercial_sqft_lag3": array([1, 2, 3]),
                "industrial_sqft_lag3": array([2, 3, 5]),
                "governmental_sqft_lag3": array([4, 7, 6])}}, 
            dataset = "land_cover")
        should_be = array([1, 1, 0, 0, 1])
        
        self.assert_(ma.allclose(values, should_be, rtol=1E-5), 
                     msg = "Error in " + self.variable_name)


if __name__ == "__main__":
    opus_unittest.main()
