# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class employment_of_sector_DDD(Variable):
    """Number of employment of sector DDD in a given building"""

    _return_type="int32"
    def __init__(self, sector_id):
        self.sector_id = "%s" % sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_employment_of_sector_%s=sanfrancisco.business.is_of_sector_%s * business.employment" % (self.sector_id, self.sector_id),
                "_employment_of_sector_%s = building.aggregate(business._employment_of_sector_%s)" % (self.sector_id, self.sector_id)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_employment_of_sector_%s" % self.sector_id)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").size()
        self.do_check("x >= 0 and x <= " + str(size), values)


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'business':
            {"business_id":array([1,2,3,4,5]),
             "sector_id":array([4,2,4,3,4]),
             "building_id":array([1,1,2,2,2]),
             "employment":array([100,20,40,30,41])
             },
            'building':
            {
             "building_id":array([1,2]),
             },
             
           }
        )
        
        should_be = array([100, 81])
        instance_name = 'sanfrancisco.building.employment_of_sector_4'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()