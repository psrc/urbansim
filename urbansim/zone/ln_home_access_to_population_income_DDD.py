# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, exp, where

# ln_home_access_to_population_income_DDD
# todo: same for employment
class ln_home_access_to_population_income_DDD(Variable):
    """ SUM(Population(i) * exp(logsum_DDD(this_zone to i)), for i=zone_1...zone_n)
    """
    population = "population"
    
    def __init__(self, number):
        self.tnumber = number
        self.logsum_hbw_am_income = "logsum_hbw_am_income_" + str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("travel_data", self.logsum_hbw_am_income), 
                attribute_label("zone", self.population)]
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        logsum_hbw_am_income = travel_data.get_attribute(self.logsum_hbw_am_income)
        from_zone_id = travel_data.get_attribute('from_zone_id')
        
        td_attr_by_idx = travel_data.get_attribute_by_index
        zone_ids = zone_set.get_attribute('zone_id')
        
        # todo: make this better with numpy features, also don't 
        #       assume travel_data is in order
        return [(zone_set.get_attribute(self.population) * 
                                    exp(td_attr_by_idx(self.logsum_hbw_am_income, where(from_zone_id == zone)))).sum() for zone in zone_ids]


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from math import exp as mathexp

class Tests(opus_unittest.OpusTestCase):
    # check the case num_autos = 2
    variable_name = "urbansim.zone.ln_home_access_to_population_income_1"

    def test_my_inputs(self):
        # the zone table includes two zones (1 and 2)
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2]),
                "population": array([44,55])}, 
             "travel_data":{ 
                 "from_zone_id":array([1,1,2,2]), 
                 "to_zone_id":array([1,2,1,2]), 
                 "logsum_hbw_am_income_1":array([-4.8,-2.222,-3.1,-4]), 
                 "logsum_hbw_am_income_2":array([-3,-2,-1,-3.5])}}, 
            dataset = "zone")
        should_be = array([44 * exp(-4.8) + 55 * exp(-2.222), 
                           44 * exp(-3.1) + 55 * exp(-4)])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
        opus_unittest.main()