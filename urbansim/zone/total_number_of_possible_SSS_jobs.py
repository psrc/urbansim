# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.total_number_of_possible_SSS_jobs_from_buildings import total_number_of_possible_SSS_jobs_from_buildings as gc_total_number_of_possible_SSS_jobs_from_buildings
from variable_functions import my_attribute_label

class total_number_of_possible_SSS_jobs(gc_total_number_of_possible_SSS_jobs_from_buildings):
    """ Sums number of possible jobs over zones.
    """
        
    def dependencies(self):
        return [my_attribute_label(self.sqft), 
                my_attribute_label(self.sqft_per_job)] 
        
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.total_number_of_possible_commercial_jobs"

    def test_my_inputs( self ):
        #declare an array of four locations, each with the specified sector ID below

        commercial_sqft = array([1000, 500, 5000, 233])
        commercial_sqft_per_job = array([20, 0, 100, 33])

        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"zone":{ 
                "buildings_commercial_sqft":commercial_sqft, 
                "commercial_sqft_per_job":commercial_sqft_per_job}}, 
            dataset = "zone" )

        #notice that the computation code above purposely truncates decimal results,
        #which makes sense because fractions of jobs don't exist
        should_be = array( [50.0, 0.0, 50.0, 7.0] )
        self.assertEqual( ma.allequal( values, should_be), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()
