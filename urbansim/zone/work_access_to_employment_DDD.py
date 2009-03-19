# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from abstract_zone_access_variable import Abstract_Zone_Access_Variable

class work_access_to_employment_DDD(Abstract_Zone_Access_Variable):
    """The accessibility to jobs in the given zone from employment (other jobs) for number of autos DDD.
    For example, if the possibilities for number of cars per household are 0, 1, 2, or 3+ (3 or more),
    then DDD can be 0, 1, 2, or 3.  Note that for this variable, the zone in which the job is located
    is the destination zone in the travel data.  (So the name for this variable is misleading - it should
    be work_access_from_employment_DDD instead.)
    
    The value of this variable for zone j is defined as follows:
        work_access_to_employment(j) = sum over i (employment(i) * exp (logsum (ij)))
    where i ranges over all zones, employment(i) is the number of jobs in zone i, 
    and logsum(ij) is the logsum from the travel model for travel from zone i to zone j. """
    
    def __init__(self, ncars):
        Abstract_Zone_Access_Variable.__init__(self, ncars, "number_of_jobs")

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
    variable_name = "urbansim.zone.work_access_to_employment_2"

    def test_my_inputs(self):
        # the zone table includes two zones (1 and 2)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2]), 
                "number_of_jobs":array([100,125])}, 
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

    def test_weird_inputs(self):
        # The zone ids don't need to start with 0 or 1.  Also, they don't need to be
        # contiguous, and the zone id's in the travel data might not be in the same order.
        # The zone table is for two zones (listed here in reverse order [14,11]).
        # Also, in the travel data below, note that the to_zone_ids are listed in a weird order ...
        # this should still work
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([14,11]), 
                "number_of_jobs":array([125,100])}, 
             "travel_data":{ 
                 "from_zone_id":array([11,11,14,14]), 
                 "to_zone_id":array([11,14,14,11]), 
                 "logsum0":array([-4.8,-2.222,-4,-3.1]), 
                 "logsum1":array([-3,-2,-3.5,-1]), 
                 "logsum2":array([-1,-2,-4,-3]), 
                 "logsum3":array([-4,-3,-1,-2])}}, 
            dataset = "zone")
        should_be = array([100*exp(-2)+125*exp(-4), 100*exp(-1)+125*exp(-3)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)

    def test_3weird_inputs(self):
        # similar to the weird_inputs test, but with 3 zones in the zone table (listed in a random order)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([14,11,99]), 
                "number_of_jobs":array([125,100,333])}, 
             "travel_data":{ 
                 "from_zone_id":array([11,11,99,14,99,11,99,14,14]), 
                 "to_zone_id":  array([99,14,99,99,14,11,11,14,11]), 
                 "logsum0":array([-4.8,-2.222,-4,-3.1,-1.11,-1.5,-2.8,-1.99,-2.99]), 
                 "logsum1":array([-3,-2,-3.5,-1,-1,-1,-1,-1,-1]), 
                 "logsum2":array([-1,-2,-3,-4,-5,-6,-7,-8,-9]), 
                 "logsum3":array([-4,-3,-2,-1,-1,-2,-3,-4,-5])}}, 
            dataset = "zone")
        should_be = array([125*exp(-8)+100*exp(-2)+333*exp(-5), 125*exp(-9)+100*exp(-6)+333*exp(-7), 125*exp(-4)+100*exp(-1)+333*exp(-3)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)

    def test_extra_zones(self):
        # Similar to test_my_inputs, but also with some additional 
        # travel data that is not used.  (It is ok for there to be additional zones 
        # in the travel data that aren't in the zone table.  In this case
        # zone 888 in the travel data is extra.)
        #
        # The zone table itself just includes two zones (1 and 2).
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2]), 
                "number_of_jobs":array([100,125])}, 
             "travel_data":{ 
                 "from_zone_id":array([1,1,2,2,888,888,1,2]), 
                 "to_zone_id":array  ([1,2,1,2,1,2,888,888]), 
                 "logsum0":array([-4.8,-2.222,-3.1,-4,-100,-200,-300,-400]), 
                 "logsum1":array([-3,-2,-1,-3.5,-100,-200,-300,-400]), 
                 "logsum2":array([-1,-2,-3,-4,-100,-200,-300,-400]), 
                 "logsum3":array([-4,-3,-2,-1,-100,-200,-300,-400])}}, 
            dataset = "zone")
        should_be = array([100*exp(-1)+125*exp(-3), 100*exp(-2)+125*exp(-4)])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()