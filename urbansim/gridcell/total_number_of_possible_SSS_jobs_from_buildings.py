# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from .variable_functions import my_attribute_label

class total_number_of_possible_SSS_jobs_from_buildings(Variable):
    """Computed by dividing the total buildings_commercial/industrial sqft. of location by the 
    commercial/industrial square feet per job
    """
    
    _return_type = "int32"
    
    def __init__(self, type):
        self.sqft = "buildings_%s_sqft" % type
        self.sqft_per_job = "%s_sqft_per_job" % type
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.sqft), my_attribute_label(self.sqft_per_job)]                             

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        values_sqft_per_job = ds.get_attribute(self.sqft_per_job)
        values_sqft = ds.get_attribute(self.sqft)
        return safe_array_divide(values_sqft, values_sqft_per_job, type="int32")
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs( self ):
        #declare an array of four locations, each with the specified sector ID below
        commercial_sqft = array([1000, 500, 5000, 233])
        commercial_sqft_per_job = array([20, 0, 100, 33])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3,4]),
                    "buildings_commercial_sqft":commercial_sqft, 
                    "commercial_sqft_per_job":commercial_sqft_per_job
                }
            }
        )

        #notice that the computation code above purposely truncates decimal results,
        #which makes sense because fractions of jobs don't exist
        should_be = array( [50.0, 0.0, 50.0, 7.0] )
        instance_name = "urbansim.gridcell.total_number_of_possible_commercial_jobs_from_buildings"    
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()