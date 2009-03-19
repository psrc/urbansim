# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class number_of_DDD_persons_households(Variable):
    """Number of households in a zone with ginven number of persons"""
    
    _return_type="int32"
    
    def __init__(self, number):
        Variable.__init__(self)
        self.has_persons = "has_%s_persons" % number

    def dependencies(self):
        return [attribute_label("household", self.has_persons), 
                attribute_label("household", "zone_id")]

    def compute(self, dataset_pool):
        households = dataset_pool.get_dataset('household')
        return self.get_dataset().sum_dataset_over_ids(households, self.has_persons)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_3_persons_households"
    def test_full_tree(self):
        zone_id = array([1, 2, 3, 4])
        hh_zone_id = array([1, 2, 3, 4, 2, 2])
        persons = array([2, 1, 0, 4, 2, 3]) 
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "zone_id": zone_id}, 
             "household":{ 
                 "zone_id":hh_zone_id, 
                 "persons":persons} }, 
            dataset = "zone")
        should_be = array([0,1,0,0])
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()