# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class average_percent_open_space_within_walking_distance(Variable):
    """Number of people in region"""

    def dependencies(self):
        return [attribute_label("gridcell", "region_id"), 
                attribute_label("gridcell", "percent_open_space_within_walking_distance"), 
                my_attribute_label("region_id")]

    def compute(self, dataset_pool):
        gridcell = dataset_pool.get_dataset('gridcell')
        return self.get_dataset().aggregate_over_ids(gridcell.get_attribute("region_id"), 
                                   gridcell.get_attribute("percent_open_space_within_walking_distance"), 'mean')

    def post_check(self, values, dataset_pool):
        size = (dataset_pool.get_dataset('gridcell')
             .get_attribute("percent_open_space_within_walking_distance").max())
        self.do_check("x >= 0 and x <= " + str(size), values)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.region_dataset import RegionDataset
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.region.average_percent_open_space_within_walking_distance"
 
    def test_my_inputs(self):
        percent = array([10,0,70,40]) 
        grid_id = array([1,2,3,4])
            
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"region":RegionDataset(), 
            "gridcell":{ 
                "percent_open_space_within_walking_distance":percent,
                "grid_id":grid_id}}, 
            dataset = "region")

        should_be = array([30])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()