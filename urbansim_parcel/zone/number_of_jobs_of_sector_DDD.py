# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class number_of_jobs_of_sector_DDD(Variable):
    """number of jobs of sector DDD in a given zone"""

    _return_type="int32"
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "urbansim_parcel.job.is_sector_%s" % self.sector_id, 
                "urbansim_parcel.job.zone_id", 
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('job'), "is_sector_%s" % self.sector_id)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("parcel").get_attribute("employment_of_sector_" + self.sector).sum()
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
            package_order=['urbansim'],
            test_data={
            'job':
            {"job_id":array([1,2,3,4,5]),
             "sector_id":array([4,2,4,3,4]),
             "zone_id":array([1,1,2,2,2]),
             },
            'zone':
            {
             "zone_id":array([1,2]),
             },
             
           }
        )
        
        should_be = array([1, 2])
        instance_name = 'urbansim_parcel.zone.number_of_jobs_of_sector_4'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        instance_name = 'urbansim_parcel.zone.number_of_jobs_of_sector_3'
        should_be = array([0, 1])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()