#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class number_of_jobs_per_acre(Variable):
    """Number of jobs in zone / number of acres in zone"""
    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.job.zone_id", 
                "number_of_jobs = zone.number_of_agents(job)",
                "acres = zone.aggregate(parcel.parcel_sqft) / 43560.0 ",
                "_number_of_jobs_per_acre = zone.number_of_jobs / zone.acres",
                ]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute('_number_of_jobs_per_acre')
        
    def post_check(self, values, dataset_pool):
        size = self.get_dataset().get_attribute("number_of_jobs").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)
        

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
                "job":{
                    "job_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "building_id":array([1, 2, 2, 2, 3, 3, 4, 5]),
                    },
                "building":{
                    "building_id":array([1,2,3,4,5]),
                    "parcel_id":  array([1,1,2,3,4])
                    },
                "parcel":{
                     "parcel_id":array([1,2,3,4]),
                     "zone_id":  array([1,3,2,2]),
                     "parcel_sqft":array([0.1, 0.2, 0.4, 0.3]) * 43560.0,                     
                 },
                "zone":{
                     "zone_id":array([1,2,3]),
                 }             
                 
           }
        )
        
        should_be = array([4/0.1, int(2/(0.3+0.4)), 2/0.2])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)
if __name__=='__main__':
    opus_unittest.main()


#from opus_core.tests import opus_unittest
#from urbansim.variable_test_toolbox import VariableTestToolbox
#from numpy import array
#from numpy import ma
#
#class Tests(opus_unittest.OpusTestCase):
#    variable_name = "psrc.zone.number_of_jobs_per_acre"
# 
#    def test_my_inputs(self):
#        number_of_jobs = array([21,22,27,42]) 
#        acres_of_land = array([1.0,2.0,1.0,2.0])
#        some_gridcell_zone_ids = array([1,2,1,3]) 
#        grid_id = array([1,2,3,4])
#            
#        values = VariableTestToolbox().compute_variable(self.variable_name, \
#                {"zone":{
#                "zone_id":array([1,2, 3])}, \
#            "gridcell":{ \
#                "number_of_jobs":number_of_jobs,\
#                "acres_of_land":acres_of_land,\
#                "zone_id":some_gridcell_zone_ids, \
#                "grid_id":grid_id}}, \
#            dataset = "zone")
#        should_be = array([24, 11, 21])
#
#        self.assertEqual(ma.allclose(values, should_be, rtol=1e-2), \
#                         True, msg = "Error in " + self.variable_name)
#
#if __name__=='__main__':
#    opus_unittest.main()