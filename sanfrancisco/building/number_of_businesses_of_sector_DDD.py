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

class number_of_businesses_of_sector_DDD(Variable):
    """Number of businesses of sector DDD in a given building"""

    _return_type="int32"
    def __init__(self, sector):
        self.sector = sector
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "is_of_sector_%s = sanfrancisco.business.is_of_sector_%s" % (self.sector, self.sector),
                "_number_of_businesses_of_sector_%s = building.aggregate(business.is_of_sector_%s)" % (self.sector, self.sector)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_number_of_businesses_of_sector_%s" % self.sector)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'business':
            {"business_id":array([1,2,3,4,5]),
             "building_id":array([1,1,2,2,2]),
             "sector_id":array([4,2,4,3,4])
             },
            'building':
            {
             "building_id":array([1,2]),
             },
             
           }
        )
        
        should_be = array([1,2])
        instance_name = 'sanfrancisco.building.number_of_businesses_of_sector_4'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()