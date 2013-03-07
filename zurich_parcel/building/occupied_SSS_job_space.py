# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import clip, ma, where
from opus_core.variables.variable import Variable
from opus_core.logger import logger

class occupied_SSS_job_space(Variable):
    """Sum of jobs sqft per building. If job sqft is <= 0, it is replaced by zone-building_type average.
        Result is clipped between 0 and building.building_sqft.
    """

    _return_type="int32"

    def __init__(self, sector):
        Variable.__init__(self)
        self.sector = sector
    
    def dependencies(self):
        return ["urbansim_parcel.job.building_id",
                "urbansim_parcel.job.sqft_imputed",
                "urbansim_parcel.building.building_sqft"]

    def compute(self,  dataset_pool):
        sectors = dataset_pool.get_dataset("sector")
        name_equals_sector = sectors.get_attribute("name") == self.sector
        name_equals_sector_indexes = where(name_equals_sector)
        assert(len(name_equals_sector_indexes) == 1)
        name_equals_sector_index = name_equals_sector_indexes[0]
        sector_ids = sectors.get_attribute("sector_id")
        sector_id = sector_ids[name_equals_sector_index][0]
        sqft_per_jobs = sectors.get_attribute("sqft_per_job")
        sqft_per_job = sqft_per_jobs[name_equals_sector_index][0]

        jobs = dataset_pool.get_dataset("job")
        buildings = self.get_dataset()
        job_sqft = ma.masked_where(jobs.get_attribute('sector_id') == sector_id, [sqft_per_job] * jobs.size(), 0)
        job_area = clip(buildings.sum_over_ids(jobs.get_attribute('building_id'), job_sqft), 0,
                        buildings.get_attribute("building_sqft"))
        logger.log_note("job_area%s: %s" % (sector_id, sum(job_area)))
        return job_area

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
        __file__,
        package_order=['urbansim_parcel','urbansim'],
        test_data={
        "building":{"building_id":         array([1,2,3]),
                   "zone_id":              array([1,2,3]),
                   "building_type_id":     array([1,3,1]),
                   "building_sqft":        array([10, 900, 30])
            },
        "building_sqft_per_job":{
                   "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                   "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                   "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
            },  
         "job": {"job_id":      array([1,2,3,4, 5, 6, 7]),
                 "sqft":        array([0,1,4,0, 2, 5, 0]),
                 "building_id": array([2,1,3,2, 1, 2, 3])
                           },
                   }
                                )
        should_be = array([10,900,30])  #was should_be = array([1+2,900,4+20])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
