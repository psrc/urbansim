# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import arange, array

class same_sector_jobs_in_faz(Variable):
    """Number of jobs of the same sector in fazes. """

    jobs_sector_id = "sector_id"
    gc_faz_id = "faz_id"

    def dependencies(self):
        return [attribute_label("job", self.jobs_sector_id),
                attribute_label("gridcell", self.gc_faz_id),
                attribute_label("faz", "same_job_sector")]

    def compute(self, dataset_pool):
        fazes = dataset_pool.get_dataset('faz')
        gc_fazes = self.get_dataset().get_2d_dataset_attribute(self.gc_faz_id)
        return fazes.get_value_from_same_job_sector_table(self.get_dataset().get_attribute_of_dataset(
                    self.jobs_sector_id), gc_fazes)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job_x_gridcell.same_sector_jobs_in_faz"

    def test_my_inputs(self):
        faz_id = array([1,2,3])
        sector_id =  array([1, 4, 2, 1, 2, 2])
        job_faz_id = array([1, 1, 3, 2, 2, 2])
        gc_faz_id = array([1,2, 2, 1])

        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"faz":{
                "faz_id":faz_id},
             "job":{
                "sector_id":sector_id,
                "faz_id":job_faz_id},
             "gridcell":{
                "faz_id":gc_faz_id}},
            dataset = "job_x_gridcell")
        should_be = array([[1 ,1, 1, 1], [1, 0, 0, 1], [0 ,2, 2, 0], [1 ,1, 1, 1], [0, 2, 2, 0], [0, 2, 2, 0]])
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()