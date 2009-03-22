# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 


from numpy import where, logical_and
from urbansim.models.scaling_jobs_model import ScalingJobsModel

class DistributeUnplacedJobsModel(ScalingJobsModel):
    """This model is used to place randomly (within sectors) any unplaced jobs.
    """
    model_name = "Distribute Unplaced Jobs Model"
     
    def run(self, location_set, agent_set, agents_filter=None, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset. The model selects all unplaced jobs which pass the given agents_filter (if any), 
            and passes them to ScalingJobsModel.
        """
        agents_index = agent_set.get_attribute(location_set.get_id_name()[0]) <= 0
        if agents_filter is not None:
            dataset_pool = kwargs.get('dataset_pool', None)
            filter_values = agent_set.compute_variables([agents_filter], dataset_pool=dataset_pool)
            agents_index = logical_and(agents_index, filter_values>0)
        return ScalingJobsModel.run(self, location_set, agent_set, where(agents_index)[0], **kwargs)


from opus_core.tests import opus_unittest
from numpy import array, ma, arange, zeros
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
        storage.write_table(table_name=jobs_table_name, table_data=job_data)
        
        jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)
        
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_table(
            table_name=building_types_table_name,
            table_data={
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
        
        # run model with filter
        # unplace first 500 jobs of sector 15
        jobs.modify_attribute(name='grid_id', data=zeros(500), index=arange(500))
        # unplace first 500 jobs of sector 1
        jobs.modify_attribute(name='grid_id', data=zeros(500), index=arange(7000, 7501))
        # place only unplaced jobs of sector 1
        model.run(gridcells, jobs, agents_filter='job.sector_id == 1')
        # 500 jobs of sector 15 should be unplaced
        result3 = where(jobs.get_attribute("grid_id")<=0)[0]
        self.assertEqual(result3.size, 500)
        # jobs of sector 1 are placed
        result4 = jobs.get_attribute_by_index("grid_id", arange(7000, 7501))
        self.assertEqual((result4 <= 0).sum(), 0)
        
if __name__=="__main__":
    opus_unittest.main()