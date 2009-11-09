# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class de_employment_DDD(Variable):
    """sum of year DDD employment forecast by Dram/Empal in county"""
    _return_type="int32"

    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "de_employment_" + str(int(number))
        Variable.__init__(self)
    
    def dependencies(self):
        return [attribute_label("large_area", "county_id"), 
                "psrc.large_area." + self.variable_name, 
                my_attribute_label("county_id")]

    def compute(self, dataset_pool):
        large_area = dataset_pool.get_dataset('large_area')
        return self.get_dataset().sum_over_ids(large_area.get_attribute("county_id"), 
                                   large_area.get_attribute(self.variable_name))

    def post_check(self, values, dataset_pool):
        size = dataset_pool.get_dataset('large_area').get_attribute(self.variable_name).sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
    
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.county.de_employment_2010"
 
    def test_my_inputs(self):
        de_employment_2010 = array([21,22,27,42]) 
        large_area_county_ids = array([1,2,1,3]) 
        large_area_id = array([1,2,3,4])
            
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"county":{
                "county_id":array([1,2, 3])}, \
            "large_area":{ \
                "de_employment_2010":de_employment_2010,\
                "county_id":large_area_county_ids, \
                "large_area_id":large_area_id}}, \
            dataset = "county")

        should_be = array([48, 22, 42])
            
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
