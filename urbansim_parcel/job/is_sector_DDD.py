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
from urbansim.functions import attribute_label

class is_sector_DDD(Variable):
    """whether the job is of sector id DDD."""
    _return_type="int32"
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)    
    
    def dependencies(self):
        return ["_is_of_sector = job.sector_id == %s" % self.sector_id]
        
    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_is_of_sector")

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
                "job":{
                    "job_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "sector_id":array([1, 2, 2, 2, 3, 3, 4, 5]),
                    },                 
           }
        )
        
        should_be = array([0, 1, 1, 1, 0, 0, 0, 0])
        instance_name = 'urbansim_parcel.job.is_sector_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
