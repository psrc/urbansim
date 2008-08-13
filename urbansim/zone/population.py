#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from urbansim.gridcell.population import population as gc_population
from urbansim.functions import attribute_label

class population(gc_population):
    """The population of the zone. """
    
    def dependencies(self):
        return [attribute_label("household", self.hh_persons), 
                attribute_label("household", "zone_id")]
    
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.population"

    def test_my_inputs(self):
        population = array([21,22,27,42]) 
        zone_ids = array([1,2,1,3]) 

        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
                {"zone":{
                         "zone_id":array([1,2, 3])}, 
                 "household":{ 
                         "persons":population,
                         "zone_id":zone_ids, 
                    }}, 
            dataset = "zone")
        should_be = array([48, 22, 42])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()