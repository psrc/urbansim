# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from variable_functions import my_attribute_label


class jobs_per_acre(Variable):
    """The jobs of the zone / land acres in the zone. """
    _return_type = "int32"
    jobs = "number_of_jobs"
    acres_of_land = "acres_of_land"
    
    def dependencies(self):
        return [my_attribute_label(self.jobs), 
                my_attribute_label(self.acres_of_land)]
    
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return safe_array_divide(ds.get_attribute(self.jobs), 
                                 ds.get_attribute(self.acres_of_land))

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import int32
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.jobs_per_acre"
 
    def test_my_inputs(self):
        
        values = VariableTestToolbox().compute_variable(self.variable_name, {
            "zone":{ 
                "number_of_jobs":array([4,2,4,5,0]),
                "acres_of_land": array([210, 52.5, 105, 0, 0])}
            }, 
            dataset = "zone")

        should_be = array([4/210.0, 2/52.5, 4/105.0, 0.0, 0.0], dtype=int32)
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), 
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()