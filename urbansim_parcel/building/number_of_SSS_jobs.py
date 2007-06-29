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
from numpy import where

class number_of_SSS_jobs(Variable):
    """Number of SSS (home_based, non_home_based) jobs in a given building"""

    _return_type="int32"
    def __init__(self, status):
        self.status = status
        Variable.__init__(self)
        
    def dependencies(self):
        return ["job_building_type.name",
                "job.building_type",
                "job.building_id"
                ]

    def compute(self,  dataset_pool):
        job_building_type = dataset_pool.get_dataset("job_building_type")
        jobs = dataset_pool.get_dataset("job")
        job_building_type_id = job_building_type.get_id_attribute()[where(job_building_type.get_attribute("name")==self.status)[0]]
        is_of_status = jobs.get_attribute("building_type") == job_building_type_id
    
        return self.get_dataset().sum_dataset_over_ids(jobs, constant=is_of_status)

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").size()
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
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'job':
            {"job_id":array([1,2,3,4,5]),
             "building_type":array([1,2,1,1,2]),
             "building_id":array([1,1,3,2,2]),
             },
            'building':
            {
             "building_id":array([1,2,3]),
             },
            'job_building_type':
            {
             "id":array([1,2]),
             "name":array(["home_based", "non_home_based"])
             },
             
           }
        )
        
        should_be = array([1, 1, 0])
        instance_name = 'urbansim_parcel.building.number_of_non_home_based_jobs'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()