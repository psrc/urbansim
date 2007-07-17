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

class land_area_taken(Variable):
    """land area taken up by the proposal
    
    """
    _return_type = "int32"
    mol = 0.1  #more or less, in this range use all vacant_land_area

    def dependencies(self):
        return ["vacant_land_area = development_project_proposal.disaggregate(urbansim_parcel.parcel.vacant_land_area)",
                "land_sqft_min = development_project_proposal.disaggregate(development_template.land_sqft_min)",
                "land_sqft_max = development_project_proposal.disaggregate(development_template.land_sqft_max)", 
                 ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        vacant_land_area = proposals.get_attribute("vacant_land_area")
        land_sqft_min = proposals.get_attribute("land_sqft_min")
        land_sqft_max = proposals.get_attribute("land_sqft_max")
        
        results = vacant_land_area.astype(self._return_type)
        w_min = where(results<land_sqft_min)
        results[w_min] = 0 #min_units[w_min], there should not be any such cases; filter takes care of them
        w_max = where(results >= land_sqft_max * (1+self.mol) )
        results[w_max] = land_sqft_max[w_max].astype(self._return_type)
        
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'building_type_id': array([1, 1, 2, 3]),
                'density':array([0.6, 2, 10, 5]),
                'land_sqft_min': array([0, 10, 4, 30]), 
                'land_sqft_max': array([2, 20, 8, 100])
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "vacant_land_area": array([1, 22,  110]),
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            },
            }
        )
        
        should_be = array([1, 0,  0, 0,  
                              20, 8, 0, 
                           2, 20, 8, 110])   
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    