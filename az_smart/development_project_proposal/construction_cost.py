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

class construction_cost(Variable):
    """construction cost of the developmentt project proposal
       it may compute on the fly using expression, thus this variable is not needed
           """ 

    def dependencies(self):
        return ["az_smart.development_project_proposal.construction_cost_per_unit",
                "az_smart.development_project_proposal.units_proposed", ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        return proposals.get_attribute("construction_cost_per_unit") * proposals.get_attribute("units_proposed")

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
                'construction_cost_per_unit': array([200000, 200, 90, 100000])
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4]),
                "units_proposed": array([0, 10000, 1200, 1, 3000, 0, 2, 4, 5000, 1000000, 3])
            }
            }
        )
        
        should_be = array([0, 2000000,  108000, 100000,  
                               600000, 0, 200000, 
                            800000, 1000000, 90000000, 300000])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    