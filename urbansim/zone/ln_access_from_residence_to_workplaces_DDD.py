# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.zone.abstract_zone_access_variable import Abstract_Zone_Access_Variable
from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, exp, log
from opus_core.ndimage import sum as ndimage_sum

class ln_access_from_residence_to_workplaces_DDD(Variable):
    """ ln(SUM(Jobs(j) * exp(logsum_DDD(i to j)), for j=zone_1...zone_n))
    This variable measures how easy is it to get from this residence to some workplace,
    for this income category (DDD).
    """
    number_of_jobs = "number_of_jobs"
    
    def __init__(self, number):
        self.tnumber = number
        self.logsum_hbw_am_income = "logsum_hbw_am_income_" + str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.logsum_hbw_am_income), 
                attribute_label("zone", self.number_of_jobs)]
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        logsum_hbw_am_income = travel_data.get_attribute(self.logsum_hbw_am_income)
        from_zone_id = travel_data.get_attribute('from_zone_id')
        to_zone_id = travel_data.get_attribute('to_zone_id')
        td_attr_by_idx = travel_data.get_attribute_by_index
        zone_ids = zone_set.get_attribute('zone_id')
        njobs = zone_set.get_attribute_by_id(self.number_of_jobs, to_zone_id)
        sums_by_from_zone = ndimage_sum(
            njobs * exp(travel_data.get_attribute(self.logsum_hbw_am_income)), 
            labels=from_zone_id, index=zone_ids)
        return log(array(sums_by_from_zone))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array,log
from numpy import ma
from math import exp as mathexp

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_access_from_residence_to_workplaces_1"

    def test_my_inputs(self):
        # the zone table includes two zones (1 and 2)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2]),
                "number_of_jobs": array([44,55])}, 
             "travel_data":{ 
                 "from_zone_id":array([1,1,2,2]), 
                 "to_zone_id":array([1,2,1,2]), 
                 "logsum_hbw_am_income_1":array([-4.8,-2.222,-3.1,-4]), 
                 "logsum_hbw_am_income_2":array([-3,-2,-1,-3.5])}}, 
            dataset = "zone")
        should_be = array([44 * exp(-4.8) + 55 * exp(-2.222), 
                           44 * exp(-3.1) + 55 * exp(-4)])
        should_be = log(should_be)
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-4), 
            "Error in %s" % self.variable_name)


if __name__=='__main__': 
        opus_unittest.main()
