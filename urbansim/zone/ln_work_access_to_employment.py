# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import ma

class ln_work_access_to_employment(Variable):
    """ln of
       ln_access_from_residence_to_workplaces_1 + ln_access_from_residence_to_workplaces_2 +
       ln_access_from_residence_to_workplaces_3 + ln_access_from_residence_to_workplaces_4
       (by employment)
    """
    ln_access_from_residence_to_workplaces_1 = "ln_access_from_residence_to_workplaces_1"
    ln_access_from_residence_to_workplaces_2 = "ln_access_from_residence_to_workplaces_2"
    ln_access_from_residence_to_workplaces_3 = "ln_access_from_residence_to_workplaces_3"
    ln_access_from_residence_to_workplaces_4 = "ln_access_from_residence_to_workplaces_4"

    def dependencies(self):
        return [attribute_label("zone", self.ln_access_from_residence_to_workplaces_1),
                attribute_label("zone", self.ln_access_from_residence_to_workplaces_2),
                attribute_label("zone", self.ln_access_from_residence_to_workplaces_3),
                attribute_label("zone", self.ln_access_from_residence_to_workplaces_4)]

    def compute(self, dataset_pool):
        return ma.log(self.get_dataset().get_attribute('ln_access_from_residence_to_workplaces_1') +
                     self.get_dataset().get_attribute('ln_access_from_residence_to_workplaces_2') +
                     self.get_dataset().get_attribute('ln_access_from_residence_to_workplaces_3') +
                     self.get_dataset().get_attribute('ln_access_from_residence_to_workplaces_4'))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
import math

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.ln_work_access_to_employment"

    def test_my_inputs(self):

        values = VariableTestToolbox().compute_variable(self.variable_name,
                {"zone":{
                'ln_access_from_residence_to_workplaces_1':array([4.5, 2.3]),
                'ln_access_from_residence_to_workplaces_2':array([1.1, 8.5]),
                'ln_access_from_residence_to_workplaces_3':array([4.4, 8.8]),
                'ln_access_from_residence_to_workplaces_4':array([2.5, 6.7])}},
            dataset = "zone")
        should_be = array([math.log(12.5), math.log(26.3)])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()