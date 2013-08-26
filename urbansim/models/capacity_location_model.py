# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, zeros, array, arange, ones, resize, clip
from opus_core.misc import sample
from opus_core.sampling_toolbox import probsample_replace
from opus_core.datasets.dataset import DatasetSubset
from opus_core.model import Model
from opus_core.logger import logger

class CapacityLocationModel(Model):
    """This model is used to place agents into locations where locations are sampled proportionally 
    to a capacity attribute. 
    """
    model_name = "Capacity Location Model"
    model_short_name = "CapLM"
    
    def __init__(self, 
                 capacity_attribute = None,
                 number_of_agents_attribute = None,
                 filter = None,
                 agents_filter=None,
                 model_name=None,
                 model_short_name=None,
                 dataset_pool=None):
        """The 'capacity_attribute' gives the total capacity, including taken locations. 
        The 'number_of_agents_attribute' gives the taken locations. 
        The sampling weights are then computed as  capacity_attribute - number_of_agents_attribute.
        """
        self.filter = filter
        self.agents_filter = agents_filter
        self.dataset_pool = self.create_dataset_pool(dataset_pool, ["urbansim", "opus_core"])
        self.capacity_attribute = capacity_attribute
        self.number_of_agents_attribute = number_of_agents_attribute
        if self.capacity_attribute is not None:
            self.consider_capacity = True
        else:
            self.consider_capacity = False   
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name
     
    def run(self, location_set, agent_set, agents_index=None, resources=None, **kwargs):
        """
            'location_set', 'agent_set' are of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which 
            the model runs. If it is None, the whole agent_set is considered.
        """
        if isinstance(agents_index,list):
            agents_index=array(agents_index)
        if agents_index is None:
            agents_index=arange(agent_set.size())

        if self.agents_filter is not None:
            filter_values = agent_set.compute_variables([self.agents_filter], dataset_pool=self.dataset_pool)[agents_index]
            filtered_agents_index = where(filter_values>0)[0] # index relative to agents_index
        else:
            filtered_agents_index = arange(agents_index.size)
        results = -1*ones(agents_index.size)
        logger.log_status("Number of agents: %s" % filtered_agents_index.size)
        choices = self._do_run(location_set, agent_set, agents_index[filtered_agents_index], resources)
        if choices.size > 0:
            results[filtered_agents_index] = choices
        return results
    
    def _do_run(self, location_set, agent_set, agents_index, resources=None):
        location_id_name = location_set.get_id_name()[0]
        asubset = DatasetSubset(agent_set, agents_index)
        if asubset.size() <= 0:
            return array([], dtype='int32')
        #unplace agents
        agent_set.modify_attribute(location_id_name, 
                                resize(array([-1]), asubset.size()), agents_index)
        if self.filter is None:
            location_index = arange(location_set.size())
        else:
            filter_values = location_set.compute_variables([self.filter], dataset_pool=self.dataset_pool)
            location_index = where(filter_values > 0)[0]
        if location_index.size <= 0:
            logger.log_status("No locations available. Nothing to be done.")
            return array([])
        
        location_subset = DatasetSubset(location_set, location_index)
        if self.consider_capacity:
            location_set.compute_variables([self.capacity_attribute], 
                                           dataset_pool=self.dataset_pool)
            weights = location_subset[self.capacity_attribute]
            if self.number_of_agents_attribute is not None:
                location_set.compute_variables([self.number_of_agents_attribute], 
                                           dataset_pool=self.dataset_pool)
                weights = clip(weights - location_subset[self.number_of_agents_attribute],
                                           0, location_subset[self.capacity_attribute])
        else:
            weights = ones(location_subset.size())
        
        if weights.sum() <=0:
            logger.log_status("Locations' capacity sums to zero. Nothing to be done.")
            return array([])        
        distr = weights/float(weights.sum())
        random_sample = probsample_replace(location_subset.get_id_attribute(), size=asubset.size(), 
                                       prob_array=distr)
        agent_set.modify_attribute(location_id_name, random_sample, agents_index)
        return agent_set.get_attribute_by_index(location_id_name, agents_index)
 

from opus_core.tests import opus_unittest
from numpy import array, ma, arange
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool

         
class Test(opus_unittest.OpusTestCase):        
    def test_capacity_jobs_model(self):        
        storage = StorageFactory().get_storage('dict_storage')

        jobs_table_name = 'building_types'        
        storage.write_table(
            table_name=jobs_table_name,
            table_data={
                "job_id": arange(200)+1,
                "grid_id":array(10*[1]+20*[2]+10*[3]+160*[-1])
                }
            )
        jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)
        capacity = array([60, 25, 200])
        gridcells_table_name = 'gridcells'        
        storage.write_table(
            table_name=gridcells_table_name,
            table_data={"grid_id":arange(3)+1,
                        "capacity": capacity}
            )
        gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)
        dataset_pool = DatasetPool(datasets_dict={'job': jobs, 'gridcell':gridcells}, 
                                   package_order=["urbansim", "opus_core"])
        current = gridcells.compute_variables(["urbansim.gridcell.number_of_jobs"], dataset_pool=dataset_pool)
        # run model
        model = CapacityLocationModel(capacity_attribute='gridcell.capacity', 
                                      number_of_agents_attribute="urbansim.gridcell.number_of_jobs",
                                      agents_filter="job.grid_id<0",
                                      dataset_pool=dataset_pool
                                      )
        model.run(gridcells, jobs)
        # get results
        result = gridcells.compute_variables(["urbansim.gridcell.number_of_jobs"], dataset_pool=dataset_pool)
        #logger.log_status((result - current)/float(result.sum()))
        #logger.log_status((capacity - current)/float(capacity.sum()))
        #logger.log_status(result)
        self.assertEqual(result[0] > result[1], True)
        self.assertEqual(result[1] < result[2], True)
        self.assertEqual(result[0] < result[2], True)
        

        

if __name__=="__main__":
    opus_unittest.main()
