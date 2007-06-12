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
from urbansim.functions import attribute_label
    
class is_sector_DDD(Variable):
    """is business of sector SSS (cie, med, mips, pdr, retail_ent, visitor)."""

    def __init__(self, sector):
        self.sector = sector
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label("building_use_id"), 
                my_attribute_label("business_id")]
        
    def compute(self,  dataset_pool):
        sector = self.get_dataset().get_attribute("building_use_id")
        return  sector == self.sector
    
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources        
    from urbansim_parcel.datasets.businesses import BusinessDataset
        
    class Tests(unittest.TestCase):
        variable_name = "urbansim_parcel.business.is_sector_14"
        
        def test_my_inputs(self):
            building_id = array([1,1,2,3,7])

            resources = Resources({'data':
                                   {"business_id":array([1,2,3,4,5]),
                                    "sector":  array(["CIE", "mips", "cie", "pdr", "cie"]),
                                    "building_use_id": array([14, 1, 14, 2, 14])
                                    },
                                  })
            businesses = BusinessDataset(resources=resources, in_storage_type="RAM")
            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"business":businesses, 
                  }, 
                dataset = "business")
            should_be = array([1, 0, 1, 0, 1])

            self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                             True, msg = "Error in " + self.variable_name)

    unittest.main()