# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable, ln
from variable_functions import my_attribute_label

class county_id(Variable):
    """county id of household"""
       
    def dependencies(self):
        return [my_attribute_label("grid_id"),
                "urbansim.gridcell.county_id"
                ]
    
    def compute(self, dataset_pool):
        gridcells = dataset_pool.get_dataset('gridcell')
        return self.get_dataset().get_join_data(gridcells, "county_id")


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.county_id"

    def test_my_inputs( self ):

        values = VariableTestToolbox().compute_variable( self.variable_name, \
            {"household":{ \
                "grid_id":array([1, 1, 2, 3, 4]),
                },
             "gridcell":{
                 "grid_id":array([1, 2, 3, 4]),
                 "county_id":array([33, 31, 21, 33])
                         }
             }, \
            dataset = "household" )
        should_be = array( [33, 33, 31, 21, 33] )
        
        self.assertEqual( ma.allclose( values, should_be, rtol=1e-7 ), \
                          True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()