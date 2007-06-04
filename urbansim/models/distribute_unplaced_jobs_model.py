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


from numpy import where
from urbansim.models.scaling_jobs_model import ScalingJobsModel

class DistributeUnplacedJobsModel(ScalingJobsModel):
    """This model is used to place randomly (within sectors) any unplaced jobs.
    """
    model_name = "Distribute Unplaced Jobs Model"
     
    def run(self, location_set, agent_set, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset. The model selects all unplaced jobs 
            and passes them to ScalingJobsModel.
        """
        agents_index = where(agent_set.get_attribute(location_set.get_id_name()[0]) <= 0)[0]
        return ScalingJobsModel.run(self, location_set, agent_set, agents_index, **kwargs)


from opus_core.tests import opus_unittest
from numpy import array, ma, arange
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset
from opus_core.storage_factory import StorageFactory

         
class Test(opus_unittest.OpusTestCase):        
    def test_distribute_unplaced_jobs_model(self):
        # Places 1750 jobs of sector 15
        # gridcell       has              expected about
        # 1         4000 sector 15 jobs   5000 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs 
        # 2         2000 sector 15 jobs   2500 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs
        # 3         1000 sector 15 jobs   1250 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs
        # unplaced  1750 sector 15 jobs   0
        
        # create jobs
        
        storage = StorageFactory().get_storage('dict_storage')

        job_data = {
            "job_id": arange(11750)+1,
            "sector_id": array(7000*[15]+3000*[1]+1750*[15]),
            "grid_id":array(4000*[1]+2000*[2]+1000*[3]+1000*[1]+1000*[2]+1000*[3]+1750*[-1])
            }
        
        jobs_table_name = 'jobs'        
        storage._write_dataset(jobs_table_name, job_data)
        
        jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)
        
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage._write_dataset(
            out_table_name = building_types_table_name,
            values = {
                "grid_id":arange(3)+1
                }
            )

        gridcells = GridcellDataset(in_storage=storage, in_table_name=building_types_table_name)

        # run model
        model = DistributeUnplacedJobsModel(debuglevel=4)
        model.run(gridcells, jobs)
        # get results

        # no jobs are unplaced
        result1 = where(jobs.get_attribute("grid_id")<0)[0]
        self.assertEqual(result1.size, 0)
        # the first 10000jobs kept their locations
        result2 = jobs.get_attribute_by_index("grid_id", arange(10000))
#            logger.log_status(result2)
        self.assertEqual(ma.allclose(result2, job_data["grid_id"][0:10000], rtol=0), True)
        

if __name__=="__main__":
    opus_unittest.main()