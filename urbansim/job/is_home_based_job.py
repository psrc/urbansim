# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros
from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_home_based_job(Variable):
    """Determine if jobs are home-based (from building_type) according to job_building_types table. """

    _return_type = "bool8"
    def dependencies(self):
        return [my_attribute_label("building_type"),
                attribute_label("job_building_type", "home_based")]

    def compute(self, dataset_pool):
        jobs_bt = dataset_pool.get_dataset('job_building_type')
        jobs = self.get_dataset()
        result = zeros(jobs.size())
        codes = jobs_bt.get_id_attribute()[jobs_bt.get_attribute("home_based") == 1]
        result = zeros(jobs.size(), dtype=self._return_type)
        for code in codes:
            result += (jobs.get_attribute("building_type") == code).astype(self._return_type)
        return result


from opus_core.tests import opus_unittest
from numpy import array, arange
from numpy import ma
from opus_core.resources import Resources
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from urbansim.datasets.job_dataset import JobDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_home_based_job"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        job_building_types_table_name = 'job_building_types'
        storage.write_table(
            table_name=job_building_types_table_name,
            table_data={
                'id':array([1,2,3,4]),
                'home_based': array([0, 1, 0, 1])
                }
            )

        jobs_table_name = 'jobs'
        storage.write_table(
            table_name=jobs_table_name,
            table_data={
                'job_id':arange(10)+1,
                'building_type': array([3,3,2,2,4,2,1,3,4,1])
                }
            )

        job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)
        jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)

        jobs.compute_variables(self.variable_name, resources=Resources({'job_building_type': job_building_types}))

        values = jobs.get_attribute(self.variable_name)

        should_be = array([0,0,1,1,1,1,0,0,1,0], dtype="bool8")

        self.assertTrue(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()