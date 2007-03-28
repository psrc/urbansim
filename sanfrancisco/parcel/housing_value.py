#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy.ma import masked_where, filled
from numpy import Float32

class housing_value(Variable):
    """ (land_value + improvement_value) / residential_units."""
    
    land_value = "land_val"
    improvement_value = "struc_val"
    residential_units = "residunits"
    
    def dependencies(self):
        return [my_attribute_label(self.land_value), \
                my_attribute_label(self.improvement_value), \
                my_attribute_label(self.residential_units)]
        
    def compute(self,  dataset_pool):
        parcels = self.get_dataset()
        residential_units = parcels.get_attribute(self.residential_units)
        return filled((parcels.get_attribute(self.land_value) + \
                       parcels.get_attribute(self.improvement_value)) /\
                      masked_where(residential_units==0, residential_units.astype(Float32)), 0.0)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
        
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy.ma import allclose
    from opus_core.resources import Resources    
    from sanfrancisco.datasets.parcels import ParcelSet

    class Tests(unittest.TestCase):
        variable_name = "sanfrancisco.parcel.housing_value"

        def test_my_inputs(self):
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4,5]),
                                    "residential_units":array([2,0,1,4,7]),
                                    "land_value":array([100,11,20,0,90]),
                                    "improvement_value":array([20,10,17,40,17]),
                                    
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels}, 
                dataset = "parcel")
            should_be = array([60, 0, 37, 10, 15.28571415])
            
            self.assertEqual(allclose(values, should_be), \
                             True, msg = "Error in " + self.variable_name)
            
    unittest.main()