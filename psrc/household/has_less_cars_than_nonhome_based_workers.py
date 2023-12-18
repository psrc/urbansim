# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class has_less_cars_than_nonhome_based_workers(Variable):
    """Does this household not have children."""
    
    cars = "cars"
    workers = "number_of_nonhome_based_workers"
    
    def dependencies(self):
        return [my_attribute_label(self.cars),
                my_attribute_label(self.workers)]
    
    def compute(self, dataset_pool):    
        return self.get_dataset().get_attribute(self.cars) < self.get_dataset().get_attribute(self.workers)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.has_less_cars_than_nonhome_based_workers"

    def test_my_inputs( self ):
        cars = array([0, 1, 2, 1])
        workers = array([1, 0, 2, 2])

        values = VariableTestToolbox().compute_variable( self.variable_name, \
            {"household":{ \
                "cars":cars,
                "number_of_nonhome_based_workers":workers}}, \
            dataset = "household" )
        should_be = array( [1,0,0,1] )
        
        self.assertEqual(ma.allclose( values, should_be, rtol=1e-7 ), \
                          True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()