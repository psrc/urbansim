# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.zone.abstract_zone_access_variable import Abstract_Zone_Access_Variable
from urbansim.functions import attribute_label
from opus_core.variables.variable import Variable
from numpy import array, log

class ln_access_to_workplace_from_residences(Variable):
    """ Average, over all income categories, of the accessibility to this workpace 
    from some residence.
    """
    access_to_workplace_from_residences_1 = "access_to_workplace_from_residences_1"
    access_to_workplace_from_residences_2 = "access_to_workplace_from_residences_2"
    access_to_workplace_from_residences_3 = "access_to_workplace_from_residences_3"
    access_to_workplace_from_residences_4 = "access_to_workplace_from_residences_4"

    def dependencies(self):
        return [attribute_label("zone", self.access_to_workplace_from_residences_1), 
                attribute_label("zone", self.access_to_workplace_from_residences_2), 
                attribute_label("zone", self.access_to_workplace_from_residences_3), 
                attribute_label("zone", self.access_to_workplace_from_residences_4)]
    
    def compute(self, dataset_pool):
        zone_set = self.get_dataset()

        return log((zone_set.get_attribute(self.access_to_workplace_from_residences_1)
                    + zone_set.get_attribute(self.access_to_workplace_from_residences_2)
                    + zone_set.get_attribute(self.access_to_workplace_from_residences_3)
                    + zone_set.get_attribute(self.access_to_workplace_from_residences_4)) / 4.0)
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    # check the case num_autos = 2
    variable_name = "urbansim.zone.ln_access_to_workplace_from_residences"

    def test_my_inputs(self):            
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"zone":{
                "access_to_workplace_from_residences_1":array([1.0, 0.5, 0.25, 0.1]),
                "access_to_workplace_from_residences_2":2.0*array([1.0, 0.5, 0.25, 0.1]),
                "access_to_workplace_from_residences_3":array([1.0, 0.5, 0.25, 0.1]),
                "access_to_workplace_from_residences_4":array([1.0, 0.5, 0.25, 0.1])}},
            dataset = "zone")
        should_be = log(array([5, 2.5, 1.25, .5]) / 4.0)
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-4), 
                         True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()