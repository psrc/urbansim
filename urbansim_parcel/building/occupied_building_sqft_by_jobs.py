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

from numpy import where, concatenate, newaxis, clip
from opus_core.variables.variable import Variable

class occupied_building_sqft_by_jobs(Variable):
    """Sum of jobs sqft per building. If job sqft is <= 0, it is replaced by zone-building_type average.
        Result is clipped between 0 and building.building_sqft.
    """

    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.job.building_id",
                "urbansim_parcel.job.sqft",
                "urbansim_parcel.building.building_sqft"]

    def compute(self,  dataset_pool):
        jobs = dataset_pool.get_dataset("job")
        buildings = self.get_dataset()
        sqft = jobs.get_attribute('sqft')
        where_zero = where(sqft <= 0)[0]
        if where_zero.size == 0:
            return clip(buildings.sum_over_ids(jobs.get_attribute('building_id'), sqft), 0,
                        buildings.get_attribute("building_sqft"))
        self.add_and_solve_dependencies(["urbansim_parcel.job.zone_id",
                "bldgs_building_type_id = job.disaggregate(building.building_type_id)", 
                "building_sqft_per_job.building_sqft_per_job"], dataset_pool=dataset_pool)
        zones = jobs.get_attribute("zone_id")
        type_ids = jobs.get_attribute("bldgs_building_type_id")
        try:
            sqft_per_job = dataset_pool.get_dataset("building_sqft_per_job")
        except:
            return clip(buildings.sum_over_ids(jobs.get_attribute('building_id'), sqft), 0 ,
                        buildings.get_attribute("building_sqft"))
        
        ids = concatenate((zones[:,newaxis],type_ids[:,newaxis]), axis=1)
        index = sqft_per_job.try_get_id_index(ids)
        building_sqft_per_job = sqft_per_job.get_attribute("building_sqft_per_job")[index]
        building_sqft_per_job[where(index==-1)] = 0
        sqft[where_zero] = building_sqft_per_job[where_zero].astype(sqft.dtype)
        return clip(buildings.sum_over_ids(jobs.get_attribute('building_id'), sqft), 0,
                    buildings.get_attribute("building_sqft"))

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from numpy import array
    from numpy import ma
    from opus_core.tests.utils.variable_tester import VariableTester

    class Tests(unittest.TestCase):
        variable_name = "urbansim_parcel.building.occupied_building_sqft_by_jobs"
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
            should_be = array([1+2,900,4+20])
            tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

    unittest.main()