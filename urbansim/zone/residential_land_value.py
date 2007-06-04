#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class residential_land_value(abstract_sum_from_gridcells):
    """Sum of residential land values for the zone.
"""
    gc_variable = "residential_land_value"
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.residential_land_value"
 
    def test_my_inputs(self):
        hc = array([120,30,54,24]) 
        some_gridcell_zone_ids = array([3,2,1,1]) #zi[i]=(zone the ith gridcell belongs to)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{
                "zone_id":array([1,2,3])}, 
            "gridcell":{ 
                "residential_land_value":hc,
                "zone_id":some_gridcell_zone_ids}}, 
            dataset = "zone")
        should_be = array([78, 30, 120])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=0), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()