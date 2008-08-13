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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class population(Variable):
    """population in a given zone"""

    _return_type="int32"
    
    def dependencies(self):
        return ["_population=sanfrancisco.zone.aggregate_population_from_building"]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_population")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute("population").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
                "zone":{
                    "zone_id":array([1,2,3,4]),
                    },
                 "building":{
                     "building_id":array([1,2,3,4,5,6]),
                     "population":array([0,1,4,0,2,5]),
                     "zone_id":   array([4,1,3,2,1,2])
                 }             
           }
        )
        
        should_be = array([3,5,4,0])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()
