# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import ma

class ln_work_access_to_population(Variable):
    """ln of
       ln_home_access_to_population_income_1 + ln_home_access_to_population_income_2 +
       ln_home_access_to_population_income_3 + ln_home_access_to_population_income_4
       (by employment)
    """
    ln_home_access_to_population_income_1 = "ln_home_access_to_population_income_1"
    ln_home_access_to_population_income_2 = "ln_home_access_to_population_income_2"
    ln_home_access_to_population_income_3 = "ln_home_access_to_population_income_3"
    ln_home_access_to_population_income_4 = "ln_home_access_to_population_income_4"

    def dependencies(self):
        return [attribute_label("zone", self.ln_home_access_to_population_income_1),
                attribute_label("zone", self.ln_home_access_to_population_income_2),
                attribute_label("zone", self.ln_home_access_to_population_income_3),
                attribute_label("zone", self.ln_home_access_to_population_income_4)]

    def compute(self, dataset_pool):
        return ma.log(self.get_dataset().get_attribute('ln_home_access_to_population_income_1') +
                     self.get_dataset().get_attribute('ln_home_access_to_population_income_2') +
                     self.get_dataset().get_attribute('ln_home_access_to_population_income_3') +
                     self.get_dataset().get_attribute('ln_home_access_to_population_income_4'))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
import math

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_work_access_to_population"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"zone":{
                'ln_home_access_to_population_income_1':array([4.5, 2.3]),
                'ln_home_access_to_population_income_2':array([1.1, 8.5]),
                'ln_home_access_to_population_income_3':array([4.4, 8.8]),
                'ln_home_access_to_population_income_4':array([2.5, 6.7])}},
            dataset = "zone")
        should_be = array([math.log(12.5), math.log(26.3)])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()