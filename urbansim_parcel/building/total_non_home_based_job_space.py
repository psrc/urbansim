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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma, float32, newaxis, concatenate, where
from opus_core.misc import unique_values

class total_non_home_based_job_space(Variable):
    """ total number of jobs a given can accommodate"""
    
    def dependencies(self):
        return ["building_sqft_per_job.building_sqft_per_job",
                "urbansim_parcel.building.non_residential_sqft",
                "urbansim_parcel.building.zone_id",
                "building.building_type_id",
                ]

    def compute(self,  dataset_pool):
        sqft_per_job = dataset_pool.get_dataset("building_sqft_per_job")
#        building_types = unique_vlaues(sqft_per_job.get_attribute("building_type_id"))
        buildings = self.get_dataset()
        zones = buildings.get_attribute("zone_id")
        type_ids = buildings.get_attribute("building_type_id")
        non_residential_sqft = buildings.get_attribute("non_residential_sqft")
        
        ids = concatenate((zones[:,newaxis],type_ids[:,newaxis]), axis=1)
        index = sqft_per_job.try_get_id_index(ids)
        building_sqft_per_job = sqft_per_job.get_attribute("building_sqft_per_job")[index]
        building_sqft_per_job[where(index==-1)] = 0
        return ma.filled(ma.masked_where(building_sqft_per_job==0, non_residential_sqft / building_sqft_per_job), 0)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
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
                },
            "building_sqft_per_job":{
                       "zone_id":              array([1,  1, 1,  2, 2, 2,  3, 3]),
                       "building_type_id":     array([1,  2, 3,  1, 2, 3,  1, 3]),
                       "building_sqft_per_job":array([100,50,200,80,60,500,20,10]),
                },                
        }
        )
        
        should_be = array([1000/100, 2000/200, 2000/80, 1000/60, 7000/50, 0/200, 0,
                           5000/10, 4000/60, 0])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()