# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.functions import attribute_label
from urbansim.gridcell.number_of_jobs_of_sector_DDD import number_of_jobs_of_sector_DDD as gc_number_of_jobs_of_sector_DDD

class number_of_jobs_of_sector_DDD(gc_number_of_jobs_of_sector_DDD):
    """Sum the number of jobs for a given zone that are in the employment sector specified by DDD """
    
    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector),
                attribute_label("job", "zone_id")]
                
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_jobs_of_sector_2"

    def test_my_inputs(self):
        job_zone_id = array([2, 1, 3, 1, 1])
        is_job_of_sector = array([0, 1, 1, 0, 1])
        zone_id = array([1,2,3])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            { "job":{
                  "zone_id":job_zone_id,
                  "is_in_employment_sector_2": is_job_of_sector }, 
              "zone":{ 
                  "zone_id":zone_id} }, 
              dataset = "zone" )
        should_be = array([2, 0, 1])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()