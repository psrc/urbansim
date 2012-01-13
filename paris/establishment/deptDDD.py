# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class deptDDD(Variable):
    """is the establishment in dept DDD"""

    _return_type="int32"
    def __init__(self, dept_id):
        self.dept_id = dept_id
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "urbansim_parcel.establishment.dept_id", 
                "_dept%s=urbansim_parcel.establishment.dept_id==%s" % (self.dept_id, self.dept_id)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset()['_dept%s' % self.dept_id]

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == 0 or x == 1")

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
            'establishment':
            {"establishment_id":array([1,2,3,4,5]),
             "dept_id":array([4,2,4,3,4]),
             },
           }
        )
        
        should_be = array([1, 0, 1, 0, 1])
        instance_name = 'paris.establishment.dept4'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        instance_name = 'paris.establishment.dept3'
        should_be = array([0, 0, 0, 1, 0])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
