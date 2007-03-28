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
from numpy import ma
from numpy import Float32

class development_template_id(Variable):
    """Identify which template a "compound" building was developed from"""
    ##TODO: to be finished when the development template is defined
    ##TODO: what to do where a parcel was developed from multiple template (additive)    
    def dependencies(self):
        return [my_attribute_label("land_area_sqft"), 
                "unit_name = development_template_component.disaggregate(building_component.unit_name)",
                "sqft_per_unit = development_template_component.disaggregate(building_component.sqft_per_unit)",
                "development_template.far"]
        
    def compute(self,  dataset_pool):
        template = dataset_pool.get_dataset("development_template")
        template_components = dataset_pool.get_dataset("development_template_component")
        unit_names = template_components.get_attribute("unit_name")
        sqft_per_unit = template_components.get_attribute("sqft_per_unit")
        buildings = self.get_dataset()
        total_sqft = zeros(buildings.size())
        template_id = zeros(buildings.size())
        for i in arange(unit_name.size()):
            unit_name = unit_names[i]
            if sqft_per_unit[i] > 0:
                sqft = buildings.get_attribute(unit_name) * sqft_per_unit[i]
            else:
                sqft = buildings.get_attribute(unit_name)
            total_sqft += sqft
            template_indexes.append(i)
        template_indexes = array(template_indexes)
        template_ids = template_components.get_attribute("template_id")[template_indexes]
        
        parcels = self.get_dataset()
        residential_units = parcels.get_attribute(self.residential_units)
        return ma.filled(parcels.get_attribute(self.lot_sf) / \
                      ma.masked_where(residential_units==0, residential_units.astype(Float32)), 0.0)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
        
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from opus_core.resources import Resources    
    from psrc_parcel.datasets.parcels import ParcelSet

    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.parcel.lot_sf_per_unit"

        def test_my_inputs(self):
            resources = Resources({'data':
                                   {"parcel_id":array([1,2,3,4,5]),
                                    "residential_units":array([2,0,1,4,7]),
                                    "lot_sf":array([1000,0,2000,1000,7000]),
                                    
                                    },
                                  })
            parcels = ParcelSet(resources=resources, in_storage_type="RAM")

            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels}, 
                dataset = "parcel")
            should_be = array([500, 0, 2000, 250, 1000])
            
            self.assertEqual(ma.allclose(values, should_be), \
                             True, msg = "Error in " + self.variable_name)
            
    unittest.main()