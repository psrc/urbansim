# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


from numpy import ma
from numpy import int8, where, zeros, logical_or
from opus_core.variables.variable import Variable
from biocomplexity.land_cover.variable_functions import my_attribute_label

class lct_recoded(Variable):
    """ transform the original lct by the following:
          LCTx == 1, 2 or 4  to 1, 
          LCTx == 5 or 10 to 5, 
          LCTx == 6 or 7 to 6,
          LCTx == 8 or 9 to 8,
          LCTx == 10, 11, 14 to 10
          LCTx == 13 to 13   """
    land_cover_types = 'lct'
         
    def dependencies(self):
        return [my_attribute_label(self.land_cover_types)]
     
    def compute(self, dataset_pool):
        lct = self.get_dataset().get_attribute(self.land_cover_types)
        result = ma.filled(lct, 0)
        groups = {}
        groups[1] = [1,2,4]
        groups[5] = [5, 10]
        groups[6] = [6, 7]
        groups[8] = [8, 9]
        groups[10] = [10,11,14]
        groups[13] = [13]
        for group in groups.keys():
            tmp = zeros(lct.shape, dtype=int8)
            for i in range(len(groups[group])):
                tmp = logical_or(tmp, lct == groups[group][i])
            result = where(tmp, group, result)
        return result


from opus_core.tests import opus_unittest
from biocomplexity.variable_test_toolbox import VariableTestToolbox
from numpy import array
from biocomplexity.tests.expected_data_test import ExpectedDataTest
#class Tests(opus_unittest.OpusTestCase):
class Tests(ExpectedDataTest):
        
    def test_my_inputs(self):
        variable_name = "biocomplexity.land_cover.lct_recoded"

        values = VariableTestToolbox().compute_variable(variable_name, 
            {"land_cover":{ 
                "lct":array([12, 4, 8, 11])}},
            dataset = "land_cover")
        should_be = array([12, 1, 8, 10])
        
        self.assert_(ma.allequal(values, should_be),
                     msg = "Error in " + variable_name)


if __name__ == "__main__":                         
    opus_unittest.main()