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
from variable_functions import my_attribute_label

class is_industrial(Variable):
    """ Is this a industrial job."""

    def dependencies(self):
        return [my_attribute_label("is_building_type_industrial")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("is_building_type_industrial")
            
    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
        

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_industrial"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        job_building_types_table_name = 'job_building_types'        
        storage.write_table(
            table_name=job_building_types_table_name,
            table_data={
                'id':array([3,2,4]), 
                'name': array(['governmental', 'commercial', 'industrial'])
                }
            )

        job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'job':{
                    'building_type':array([4,4,0])
                    },
                'job_building_type': job_building_types
                },
            dataset = 'job'
            )
            
        should_be = array([1,1,0])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = 'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()