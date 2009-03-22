# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_nhb_jobs_without_resource_construction_sectors(Variable):
    """Number of jobs for a given gridcell """
    _return_type="int32"

    
    def dependencies(self):
        #resource and construction sectors are hard-coded as sector 1 and 2
        return ["urbansim.gridcell.number_of_non_home_based_jobs",
                "urbansim.gridcell.number_of_non_home_based_jobs_of_sector_1",
                "urbansim.gridcell.number_of_non_home_based_jobs_of_sector_2"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("number_of_non_home_based_jobs") - \
               self.get_dataset().get_attribute("number_of_non_home_based_jobs_of_sector_1") - \
               self.get_dataset().get_attribute("number_of_non_home_based_jobs_of_sector_2")

    def post_check(self, values, dataset_pool):
        maxv = dataset_pool.get_dataset('gridcell').get_attribute("number_of_non_home_based_jobs").max()
        self.do_check("x >= 0 and x <= " + str(maxv), values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.gridcell.number_of_nhb_jobs_without_resource_construction_sectors"

    def test_my_inputs(self):
        gridcell_grid_id = array([1, 2, 3, 4])
        jobs = array([42, 0, 30, 11])
        sector_1_jobs = array([0, 0, 11, 10]) 
        sector_2_jobs = array([0, 0, 10, 1]) 
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            { "gridcell":{
                  "grid_id":gridcell_grid_id ,
                  "number_of_non_home_based_jobs":jobs,
                  "number_of_non_home_based_jobs_of_sector_1":sector_1_jobs,
                  "number_of_non_home_based_jobs_of_sector_2":sector_2_jobs
                  }},
              dataset = "gridcell" )
        should_be = array([42, 0, 9, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()