# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, round_
from opus_core.variables.variable import Variable

class sqft_imputed(Variable):
    """jobs sqft imputed by zone-building_type average for jobs where sqft is <= 0.
    """

    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.job.zone_id",
                "bldgs_building_type_id = job.disaggregate(building.building_type_id)", 
                "urbansim_parcel.job.building_id",
                "building_sqft_per_job.building_sqft_per_job"]

    def compute(self,  dataset_pool):
        jobs = self.get_dataset()
        buildings = dataset_pool.get_dataset("building")
        zones = jobs.get_attribute("zone_id")
        type_ids = jobs.get_attribute("bldgs_building_type_id")
        sqft_per_job = dataset_pool.get_dataset("building_sqft_per_job")
        table_with_imputed_values = round_(sqft_per_job.get_building_sqft_as_table(zones.max(),
                                                                                   type_ids.max()))
        sqft = table_with_imputed_values[zones, type_ids].astype(self._return_type)
        return sqft

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test(self):
        tester = VariableTester(
        __file__,
        package_order=['urbansim_parcel','urbansim'],
        test_data={
        "building":{"building_id":         array([1,2,3,4]),
                   "zone_id":              array([1,2,3,3]),
                   "building_type_id":     array([1,3,1,2]),
            },
        "building_sqft_per_job":{
                   "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                   "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                   "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
            },  
         "job": {"job_id":      array([1,2,3,4, 5, 6, 7, 8]),
#                     "sqft":        array([0,1,4,0, 2, 5, 0, 0]),
                 "building_id": array([2,1,3,1, 1, 2, 3, 4])
                           },
                   }
                                )
        # mean over "building_sqft_per_job" is 127.5
#            should_be = array([500, 1, 4, 100, 2, 5, 20, 128])
        should_be = array([500, 100, 20, 100, 100, 500, 20, 128])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()