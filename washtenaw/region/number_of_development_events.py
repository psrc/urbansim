# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_development_events(Variable):
    """Number of development_events in developed cell in region"""

    def dependencies(self):
        return ["urbansim.gridcell.region_id", 
                "urbansim.gridcell.number_of_development_events", 
                my_attribute_label("region_id")]

    def compute(self, dataset_pool):
        gridcell = dataset_pool.get_dataset('gridcell')
        num_of_dev_events = gridcell.get_attribute('number_of_development_events')
        return self.get_dataset().sum_over_ids(gridcell.get_attribute("region_id"), 
                                   num_of_dev_events)

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('gridcell').get_attribute("number_of_development_events").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from urbansim.datasets.region_dataset import RegionDataset
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "washtenaw.region.number_of_development_events"

    def test_my_inputs(self):
        num_of_dev_events = array([21,22,27,42]) 
        grid_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(
            self.variable_name, 
            {
                "region":RegionDataset(), 
                "gridcell":{ 
                    "number_of_development_events":num_of_dev_events,
                    "grid_id":grid_id
                    }
                }, 
            dataset = "region")

        should_be = array([112])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), 
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()