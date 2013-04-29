# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import clip
from opus_core.logger import logger, log_block

class vacant_SSS_job_space(Variable):
    """ number of job spaces that is vacant/unoccupied"""
    
    _return_type = "int32"
    
    def __init__(self, sector):
        Variable.__init__(self)
        self.sector = sector
    
    def dependencies(self):
        return []

    @log_block(name='vacant_SSS_job_space.compute')
    def compute(self,  dataset_pool):
        building = self.get_dataset()
        total = building.compute_one_variable_with_unknown_package("total_%s_job_space" % self.sector, dataset_pool=dataset_pool)
        logger.log_note("total: %s" % (repr(total)))
        occupied = building.compute_one_variable_with_unknown_package("occupied_%s_job_space" % self.sector, dataset_pool=dataset_pool)
        logger.log_note("occupied: %s" % (repr(occupied)))
        vacant = total - occupied
        logger.log_note("vacant: %s" % (repr(vacant)))

        # HACK
        vacant = clip(vacant, a_min=0, a_max=1e100)
        
        logger.log_note("vacant: %s" % (sum(vacant)))
        assert((vacant >= 0).all())
        assert(sum(vacant) > 0)
        return vacant

    def post_check(self,  values, dataset_pool=None):
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
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            "building":{"building_id":         array([1,2,3,4,5,6,7,8,9,10]),
                       "zone_id":              array([1,1,2,2,1,3,3,3,2,2]),
                       "building_type_id":     array([1,3,1,2,2,1,2,3,2,4]),
                       "non_residential_sqft": array([1,2,2,1,7,0,3,5,4,6])*1000,
             "occupied_building_sqft_by_jobs": array([500, 2100, 0, 0, 6000, 100, 3000, 1000, 0, 5999])
                                       #vacant sqft:  500, 0,  2000, 1000, 1000, 0, 0, 4000, 4000, 1  
                },
            "building_sqft_per_job":{
                       "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                       "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                       "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
                },                          
        }
        )
        
        should_be = array([5, 0, 2000/80, 1000/60, 1000/50, 0, 0, 4000/10, 4000/60, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()