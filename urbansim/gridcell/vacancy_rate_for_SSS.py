# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import safe_array_divide

class vacancy_rate_for_SSS(Variable):
    """ vacant units / number of units"""
    _return_type="float32"

    def __init__(self, units):
        self.vacant_units = "vacant_%s_from_buildings" % units
        self.number_of_units = "buildings_%s" % units
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.vacant_units), \
                my_attribute_label(self.number_of_units)]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return safe_array_divide(ds.get_attribute(self.vacant_units), 
                                 ds.get_attribute(self.number_of_units))
   
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 1", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        sqft_of_industrial_jobs = array([1225, 5000, 7500])
        industrial_sqft = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{
                    "grid_id":array([1,2,3]),
                    "sqft_of_industrial_jobs":sqft_of_industrial_jobs, 
                    "buildings_industrial_sqft":industrial_sqft,
                }
            }
        )
        
        should_be = array([770/1995.0, 5000/10000.0, 0])
        instance_name = "urbansim.gridcell.vacancy_rate_for_industrial_sqft"
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()