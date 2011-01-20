# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.vacancy_rate_for_SSS import vacancy_rate_for_SSS as gc_vacancy_rate_for_SSS
from variable_functions import my_attribute_label

class vacancy_rate_for_SSS(gc_vacancy_rate_for_SSS):
    """ vacant units / number of units (see the corresponding code for gridcell)"""
        
    def dependencies(self):
        return [my_attribute_label(self.vacant_units), 
                my_attribute_label(self.number_of_units)]

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacancy_rate_for_industrial_sqft"

    def test_my_inputs(self):
        sqft_of_industrial_jobs = array([1225, 5000, 7500])
        industrial_sqft = array([1995, 10000, 7500])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "sqft_of_industrial_jobs":sqft_of_industrial_jobs, 
                "buildings_industrial_sqft":industrial_sqft,
        }}, 
            dataset = "zone")
        should_be = array([770/1995.0, 5000/10000.0, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-5), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()