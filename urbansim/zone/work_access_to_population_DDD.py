# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from abstract_zone_access_variable import Abstract_Zone_Access_Variable

class work_access_to_population_DDD(Abstract_Zone_Access_Variable):
    """The accessibility to jobs in the given zone from population for number of autos DDD.
    For example, if the possibilities for number of cars per household are 0, 1, 2, or 3+ (3 or more),
    then DDD can be 0, 1, 2, or 3.  Note that for this variable, the zone in which the job is located
    is the destination zone in the travel data.  (So the name for this variable is misleading - it should
    be work_access_from_population_DDD instead.)
    
    The value of this variable for zone j is defined as follows:
        work_access_to_population(j) = sum over i (employment(i) * exp (logsum (ij)))
    where i ranges over all zones, population(i) is the population in zone i, 
    and logsum(ij) is the logsum from the travel model for travel from zone i to zone j. """
    
    def __init__(self, ncars):
        Abstract_Zone_Access_Variable.__init__(self, ncars, "population")

    def access_is_from_origin(self):
        """the zone in which the job is located is the destination zone in the travel data for this variable"""
        return False
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import exp

class Tests(opus_unittest.OpusTestCase):
    # check the case num_autos = 2
    variable_name = "urbansim.zone.work_access_to_population_2"
 
    def test_my_inputs(self):
        # the zone table includes two zones (1 and 2)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2]), 
                "population":array([100,125])}, 
             "travel_data":{ 
                 "from_zone_id":array([1,1,2,2]), 
                 "to_zone_id":array([1,2,1,2]), 
                 "logsum0":array([-4.8,-2.222,-3.1,-4]), 
                 "logsum1":array([-3,-2,-1,-3.5]), 
                 "logsum2":array([-1,-2,-3,-4]), 
                 "logsum3":array([-4,-3,-2,-1])}}, 
            dataset = "zone")
        should_be = array([100*exp(-1)+125*exp(-3), 100*exp(-2)+125*exp(-4)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)

# work_access_to_employment (which is exactly the same except that it uses jobs instead of population)
# has a number of additional unit tests

if __name__=='__main__':
    opus_unittest.main()