# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_development_type_SSS(Variable):
    """is of SSS development type"""

    def __init__(self, type_name):
        self.type_name = type_name
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label("development_type_name")]

    def compute(self, dataset_pool):
        devtype_name = self.get_dataset().get_attribute('development_type_name')
        return devtype_name == self.type_name

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "randstad.gridcell.is_development_type_residential_city_center"
    #"1" in this case is the group number. was originally DDD, but have to specify it since this is a test, and the
    #"parent code" isn't actually invoked
    def test_my_inputs(self):
        """"""
        gridcell_devtype_name = array(['residential', 'residential_city_center', 'industrial'])
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {"gridcell":{ 
                "development_type_name":gridcell_devtype_name}}, 
            dataset = "gridcell")
        should_be = array([0, 1, 0])
        
        self.assertEqual( ma.allequal( values, should_be ), 
                          True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()