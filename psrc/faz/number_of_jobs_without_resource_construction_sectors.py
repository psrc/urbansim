# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_jobs_without_resource_construction_sectors(Variable):
    """How many jobs are in the faz.
"""
    _return_type="int32"
    
    
    def dependencies(self):
        return ["psrc.zone.number_of_jobs_without_resource_construction_sectors", 
                attribute_label("zone", "faz_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('zone'), 
                "number_of_jobs_without_resource_construction_sectors")


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.faz.number_of_jobs_without_resource_construction_sectors"
 
    def test_my_inputs(self):
        number_of_jobs = array([21,22,27,42]) 
        some_zone_faz_ids = array([1,2,1,3]) #zi[i]=(zone the ith gridcell belongs to)
        zone_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"faz":{
                "faz_id":array([1,2, 3])}, \
            "zone":{ \
                "number_of_jobs_without_resource_construction_sectors":number_of_jobs,\
                "faz_id":some_zone_faz_ids, \
                "zone_id":zone_id}}, \
            dataset = "faz")
        should_be = array([48, 22, 42])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()