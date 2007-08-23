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

from numpy import where, round_
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
        table_with_imputed_values = round_(sqft_per_job.get_building_sqft_as_table(zones[where_zero].max(),
                                                                                   type_ids[where_zero].max()))
        sqft[where_zero] = table_with_imputed_values[zones[where_zero], type_ids[where_zero]].astype(sqft.dtype)
        return sqft

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from numpy import array
    from opus_core.tests.utils.variable_tester import VariableTester

    class Tests(unittest.TestCase):
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
                     "sqft":        array([0,1,4,0, 2, 5, 0, 0]),
                     "building_id": array([2,1,3,1, 1, 2, 3, 4])
                               },
                       }
                                    )
            # mean over "building_sqft_per_job" is 127.5
            should_be = array([500, 1, 4, 100, 2, 5, 20, 128])
            tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

    unittest.main()