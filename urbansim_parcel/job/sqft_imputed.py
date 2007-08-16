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

from numpy import where, concatenate, newaxis
from opus_core.variables.variable import Variable

class sqft_imputed(Variable):
    """jobs sqft imputed by zone-building_type average for jobs where sqft is <= 0.
    """

    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.job.sqft"]

    def compute(self,  dataset_pool):
        jobs = self.get_dataset()
        sqft = jobs.get_attribute('sqft').copy()
        where_zero = where(sqft <= 0)[0]
        if where_zero.size == 0:
            return sqft
        self.add_and_solve_dependencies(["urbansim_parcel.job.zone_id",
                "bldgs_building_type_id = job.disaggregate(building.building_type_id)", 
                "urbansim_parcel.job.building_id",
                "building_sqft_per_job.building_sqft_per_job"], dataset_pool=dataset_pool)
        buildings = dataset_pool.get_dataset("building")
        zones = jobs.get_attribute("zone_id")
        type_ids = jobs.get_attribute("bldgs_building_type_id")
        try:
            sqft_per_job = dataset_pool.get_dataset("building_sqft_per_job")
        except:
            return sqft
        ids = concatenate((zones[:,newaxis],type_ids[:,newaxis]), axis=1)
        index = sqft_per_job.try_get_id_index(ids)
        building_sqft_per_job = sqft_per_job.get_attribute("building_sqft_per_job")[index]
        building_sqft_per_job[where(index==-1)] = 0
        sqft[where_zero] = building_sqft_per_job[where_zero].astype(sqft.dtype)
        return sqft

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from numpy import array
    from numpy import ma
    from opus_core.tests.utils.variable_tester import VariableTester

    class Tests(unittest.TestCase):
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
                     "building_id": array([2,1,3,1, 1, 2, 3])
                               },
                       }
                                    )
            should_be = array([500, 1, 4, 100, 2, 5, 20])
            tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

    unittest.main()