# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.vacant_SSS_job_space_from_buildings import vacant_SSS_job_space_from_buildings as gc_vacant_SSS_job_space_from_buildings
from variable_functions import my_attribute_label

class vacant_SSS_job_space_from_buildings(gc_vacant_SSS_job_space_from_buildings):
    """ The SSS_sqft_from_buildings/SSS_sqft_per_job - number_of_SSS_jobs. (See its gridcell equivalent for the algorithm.)""" 

    def __init__(self, type):
        gc_vacant_SSS_job_space_from_buildings.__init__(self, type)
        self.possible_jobs = "total_number_of_possible_%s_jobs" % type        
        
    def dependencies(self):
        return [my_attribute_label(self.number_of_jobs), 
                my_attribute_label(self.possible_jobs)]                             

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_commercial_job_space_from_buildings"

    def test_my_inputs(self):
        number_of_commercial_jobs = array([12, 39, 0, 10])
        commercial_sqft = array([1200, 16, 3900, 15])
        commercial_sqft_per_job = array([20, 3, 30, 0])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_commercial_jobs":number_of_commercial_jobs,
                "buildings_commercial_sqft":commercial_sqft, 
                "commercial_sqft_per_job":commercial_sqft_per_job}}, 
            dataset = "zone")
        should_be = array([1200/20.0 - 12, 0, 3900/30.0, 0])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()