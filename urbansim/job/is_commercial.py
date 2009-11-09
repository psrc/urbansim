# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class is_commercial(Variable):
    """ Is this a commercial job."""
    
    def dependencies(self):
        return [my_attribute_label("is_building_type_commercial")]
        
    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("is_building_type_commercial")

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_commercial"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        job_building_types_table_name = 'job_building_types'        
        storage.write_table(
            table_name=job_building_types_table_name,
            table_data={
                'id':array([0,2]), 
                'name': array(['foo', 'commercial'])
                }
            )

        job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'job':{
                    'building_type':array([2,0,2])
                    },
                'job_building_type': job_building_types
                },
            dataset = 'job'
            )
            
        should_be = array([1,0,1])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()