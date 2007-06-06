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

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import where

class construction_cost_per_unit(Variable):
    """  aggregate construction_cost_per_unit from unit_cost for each building component
    result = sum over all components (percent_of_building_sqft * construction_cost_per_unit / sqft_per_unit)
    """
    ##TODO: do we want to specify the construction cost of residential buildings by $/unit or $/sqft
    #this variale compute the latter
    def dependencies(self):
        return ["development_template_component.construction_cost_per_unit",
                "development_template_component.building_sqft_per_unit",
                "portion_of_building = development_template_component.percent_building_sqft / 100.0", 
                "construction_cost_per_component = development_template_component.construction_cost_per_unit * development_template_component.portion_of_building / development_template_component.building_sqft_per_unit",
                "_construction_cost_per_unit = development_template.aggregate(development_template_component.construction_cost_per_component)"
                 ]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_construction_cost_per_unit")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['az_smart','urbansim'],
            test_data={            
            'development_template':
            {
                'template_id': array([1,2,3,4]),
            },
            'development_template_component':
            {
                "component_id":array([1,2,3,4,5]),
                'template_id': array([1,2,3,4,4]),
                "percent_building_sqft":array([100, 100, 100, 20, 80]),
                "building_sqft_per_unit":  array([1600,  1,  2000,  1, 1600]),
                "construction_cost_per_unit":array([100000,  200,  300000,  100, 100000])

            },
#            'building_component':
#            {
#                "component_id":array([1,  2,  3,  4]),
#            }
            }
        )
        
        should_be = array([62.5, 200, 150, 70])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    