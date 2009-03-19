# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class aggregate_SSS_from_building(Variable):
    """aggregate SSS variable from building"""

    _return_type="Int32"
    
    def __init__(self, variable_name):
        self.variable_name = variable_name
        Variable.__init__(self)
    
    def dependencies(self):
        return ["sanfrancisco.building.zone_id",
                "_aggregate_%s=zone.aggregate(sanfrancisco.building.%s)" % (self.variable_name,self.variable_name)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_aggregate_%s" % self.variable_name)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("building").get_attribute(self.variable_name).sum()
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
            'building':
            {"building_id": array([1,2,3,4,5,6]),
             "parcel_id": array([1,1,2,2,3,3]),
             "employment":array([0,1,4,0,2,5]),
            },
            'parcel':
            {
             "parcel_id":array([1,2,3]),
             "zone_id":  array([1,1,2]),
             },
            'zone':
            {
             "zone_id":  array([1,2]),
             },
             
           }
        )
        
        should_be = array([5, 7])

        instance_name = 'sanfrancisco.zone.aggregate_employment_from_building'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
