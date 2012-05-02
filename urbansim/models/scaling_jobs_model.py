# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from numpy import where, zeros, array, arange, ones, ma, resize, logical_and
from opus_core.ndimage import sum as ndimage_sum
from opus_core.misc import DebugPrinter, sample, unique
from opus_core.sampling_toolbox import probsample_replace
from opus_core.datasets.dataset import DatasetSubset
from opus_core.model import Model
from opus_core.logger import logger

class ScalingJobsModel(Model):
    """This model is used to place new jobs that are in specific employment sectors, 
    such as military and education, do not tend to create new business locations or move 
    existing business locations. It relocates given jobs according to the distribution of 
    the scalable jobs of different sectors.
    """
    model_name = "Scaling Jobs Model"
    model_short_name = "SJM"
    variable_package = "urbansim"
    
    def __init__(self, group_member=None, 
                 agents_grouping_attribute = 'job.building_type', 
                 filter = None, 
                 model_name=None,
                 model_short_name=None,
                 variable_package=None,
                 dataset_pool=None,
                 debuglevel=0):
        self.group_member = group_member
        if self.group_member:
            self.group_member.set_agents_grouping_attribute(agents_grouping_attribute)
        self.filter = filter
        self.dataset_pool = self.create_dataset_pool(dataset_pool, ["urbansim", "opus_core"])
        self.debug = DebugPrinter(debuglevel)
        
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name
        if variable_package is not None:
            self.variable_package = variable_package
     
    def run(self, location_set, agent_set, agents_index=None, data_objects=None,
            resources=None, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which 
            the model runs. If it is None, the whole agent_set is considered.
            'data_objects' is a dictionary where each key is the name of an data object 
            ('zone', ...) and its value is an object of class  Dataset.
        """
        if isinstance(agents_index,list):
            agents_index=array(agents_index)
        if agents_index is None:
            agents_index=arange(agent_set.size())
        if self.group_member:
            new_agents_index = self.group_member.get_index_of_my_agents(agent_set, agents_index)
        else:
            new_agents_index = arange(agents_index.size)
        self.debug.print_debug("Number of scalable jobs: " + str(agents_index[new_agents_index].size),2)
        choices = self._do_run(location_set, agent_set, agents_index[new_agents_index], data_objects, resources)
        result = resize(array([-1], dtype=choices.dtype), agents_index.size)
        result[new_agents_index] = choices
        return result
    
    def _do_run(self, location_set, agent_set, agents_index, data_objects=None, resources=None):
        location_id_name = location_set.get_id_name()[0]
        jobsubset = DatasetSubset(agent_set, agents_index)
        if jobsubset.size() <= 0:
            return array([], dtype='int32')
        #unplace jobs
        agent_set.set_values_of_one_attribute(location_id_name, 
                                              resize(array([-1.0]), jobsubset.size()), agents_index)
        sector_ids = jobsubset.get_attribute("sector_id")
        sectors = unique(sector_ids)
        counts = ndimage_sum(ones((jobsubset.size(),)), labels=sector_ids.astype('int32'), index=sectors.astype('int32'))
        if sectors.size <=1 :
            counts = array([counts])
        variables = map(lambda x: "number_of_jobs_of_sector_"+str(int(x)), sectors)
        compute_variables = map(lambda var: self.variable_package + "." + 
            location_set.get_dataset_name()+ "." + var, variables)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.dataset_pool.add_datasets_if_not_included({agent_set.get_dataset_name():agent_set})
        location_set.compute_variables(compute_variables, dataset_pool=self.dataset_pool)
        if self.filter is None:
            location_index = arange(location_set.size())
        else:
            filter_values = location_set.compute_variables([self.filter], dataset_pool=self.dataset_pool)
            location_index = where(filter_values > 0)[0]
        if location_index.size <= 0:
            logger.log_status("No locations available. Nothing to be done.")
            return array([])
        location_subset = DatasetSubset(location_set, location_index)
        i=0
        for sector in sectors:
            distr = location_subset.get_attribute(variables[i])
            if ma.allclose(distr.sum(), 0):
                uniform_prob = 1.0/distr.size
                distr = resize(array([uniform_prob], dtype='float64'), distr.size)
                logger.log_warning("Probabilities in scaling model for sector " + str(sector) + " sum to 0.0.  Substituting uniform distribution!")
#                random_sample = sample(location_set.get_attribute("grid_id"), k=int(counts[i]), \
#                                   probabilities = distr)
            distr = distr/float(distr.sum())
            random_sample = probsample_replace(location_subset.get_id_attribute(), size=int(counts[i]), 
                                       prob_array=distr)
            idx = where(sector_ids == sector)[0]
            #modify job locations
            agent_set.set_values_of_one_attribute(location_id_name, random_sample, agents_index[idx])
            i+=1
        return agent_set.get_attribute_by_index(location_id_name, agents_index)
 
    def prepare_for_run(self, agent_set=None, agents_filter=None, agents_index=None):
        if agent_set is None or agents_filter is None:
            return agents_index
        filter = agent_set.compute_variables([agents_filter], dataset_pool=self.dataset_pool)
        if agents_index is not None:
            tmp = zeros(agent_set.size(), dtype='bool8')
            tmp[agents_index]=True
            filtered_index = logical_and(filter, tmp)
        return where(filtered_index)[0]

from opus_core.tests import opus_unittest
from numpy import array, ma, arange
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset
from opus_core.storage_factory import StorageFactory

         
class Test(opus_unittest.OpusTestCase):        
    def test_scaling_jobs_model(self):
        # Places 1750 jobs of sector 15
        # gridcell       has              expected about
        # 1         4000 sector 15 jobs   5000 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs 
        # 2         2000 sector 15 jobs   2500 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs
        # 3         1000 sector 15 jobs   1250 sector 15 jobs
        #           1000 sector 1 jobs    1000 sector 1 jobs
        # unplaced  1750 sector 15 jobs   0
        
        storage = StorageFactory().get_storage('dict_storage')

        jobs_table_name = 'building_types'        
        storage.write_table(
            table_name=jobs_table_name,
            table_data={
                "job_id": arange(11750)+1,
                "sector_id": array(7000*[15]+3000*[1]+1750*[15]),
                "grid_id":array(4000*[1]+2000*[2]+1000*[3]+1000*[1]+1000*[2]+1000*[3]+1750*[-1])
                }
            )
        jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)
        
        gridcells_table_name = 'gridcells'        
        storage.write_table(
            table_name=gridcells_table_name,
            table_data={"grid_id":arange(3)+1}
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)
        
        # run model
        model = ScalingJobsModel(debuglevel=4)
        model.run(gridcells, jobs, agents_index = arange(10001, 11750))
        # get results
        gridcells.compute_variables(["urbansim.gridcell.number_of_jobs_of_sector_15", "urbansim.gridcell.number_of_jobs_of_sector_1"], 
            resources = Resources({"job":jobs}))
        # sector 1 jobs should be exactly the same
        result1 = gridcells.get_attribute("number_of_jobs_of_sector_1")
        self.assertEqual(ma.allclose(result1, array([1000, 1000, 1000]), rtol=0), True)
        # the distribution of sector 15 jobs should be the same with higher means 
        result2 = gridcells.get_attribute("number_of_jobs_of_sector_15")
#            logger.log_status(result2)
        self.assertEqual(ma.allclose(result2, array([5000, 2500, 1250]), rtol=0.05), True)
        

if __name__=="__main__":
    opus_unittest.main()
