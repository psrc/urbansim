# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_building_type_SSS(Variable):
    """ Is this a job of a building type SSS."""
    
    _return_type='bool8'
    type = "building_type"

    def __init__(self, building_type_name):
        self.building_type_name = building_type_name
        Variable.__init__(self)

    def dependencies(self):
        return [my_attribute_label(self.type), attribute_label("job_building_type", "name")]

    def compute(self, dataset_pool):
        building_types = dataset_pool.get_dataset('job_building_type')
        code = building_types.get_id_attribute()[building_types.get_attribute("name") == self.building_type_name]
        return self.get_dataset().get_attribute(self.type) == code

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_building_type_commercial"

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