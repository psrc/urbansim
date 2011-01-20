# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs_of_sector_DDD(Variable):
    """Sum the number of jobs for a given faz that are in the employment sector specified by DDD """
    
    _return_type="int32"
    
    def __init__(self, number):
        self.tnumber = number
        self.number_of_jobs_of_sector = "number_of_jobs_of_sector_"+str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("zone", self.number_of_jobs_of_sector), 
                attribute_label("zone", "faz_id")]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        return self.get_dataset().sum_dataset_over_ids(zones, self.number_of_jobs_of_sector)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.faz.number_of_jobs_of_sector_2"

    def test_my_inputs(self):
        #gridcell_grid_id = array([1, 2, 3])
        #specify an array of 4 jobs, 1st job's grid_id = 2 (it's in gridcell 2), etc.
        zone_faz_id = array([2, 1, 3, 1])
        #corresponds to above job array, specifies which jobs in which gridcells "qualify"
        number_of_jobs_of_sector = array([0, 1, 1, 0])
        faz_id = array([1,2,3])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            { "zone":{
                  "faz_id":zone_faz_id,
                  "number_of_jobs_of_sector_2": number_of_jobs_of_sector }, 
              "faz":{ 
                  "faz_id":faz_id} }, 
              dataset = "faz" )
        should_be = array([1, 0, 1])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()