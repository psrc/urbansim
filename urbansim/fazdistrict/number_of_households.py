# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_households(Variable):
    """How many households are in the fazdistrict.
"""
    _return_type="int32"
    faz_number_of_households = "number_of_households"
    
    def dependencies(self):
        return [attribute_label("faz", self.faz_number_of_households), attribute_label("faz", "fazdistrict_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('faz'), 
                self.faz_number_of_households)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.fazdistrict.number_of_households"
 
    def test_my_inputs(self):
        number_of_households = array([21,22,27,42]) 
        some_faz_fazdistricts = array([1,2,1,3]) #zi[i]=(zone the ith gridcell belongs to)
        faz_id = array([1,2,3,4])
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"fazdistrict":{
                "fazdistrict_id":array([1,2, 3])}, 
            "faz":{ 
                "number_of_households":number_of_households,
                "fazdistrict_id":some_faz_fazdistricts, 
                "faz_id":faz_id}}, 
            dataset = "fazdistrict")
        should_be = array([48, 22, 42])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()