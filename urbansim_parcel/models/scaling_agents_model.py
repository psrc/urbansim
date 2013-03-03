# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import re
from opus_core.resources import Resources
from numpy import where, zeros, array, arange, ones, ma, resize, logical_and
from opus_core.ndimage import sum as ndimage_sum
from opus_core.misc import DebugPrinter, sample, unique
from opus_core.sampling_toolbox import probsample_replace
from opus_core.model import Model
from opus_core.logger import logger

class ScalingAgentsModel(Model):
    """Scale agents in their place by given amount. It is a generalization of the ScalingJobsModel.
    """
    model_name = "Scaling Agents Model"
    model_short_name = "SAM"
    
    def __init__(self,  submodel_string=None,
                 filter = None, 
                 dataset_pool=None,
                 package_order=["urbansim_parcel", "urbansim", "opus_core"],
                 debuglevel=0):
        self.filter = filter
        self.submodel_string = submodel_string
        self.dataset_pool = self.create_dataset_pool(dataset_pool, package_order)
        self.debug = DebugPrinter(debuglevel)
        
     
    def run(self, location_set, agent_set, agents_index=None):
        """
            'location_set', 'agent_set' are of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which 
            the model runs. If it is None, the whole agent_set is considered.
        """
        if agents_index is None:
            agents_index=arange(agent_set.size())
        
        if agents_index.size == 0:
            logger.log_status('Nothing to be done.')
            return array([], dtype='int32')
        if self.submodel_string is not None:
            submodels = unique(agent_set[self.submodel_string][agents_index])
        else:
            submodels = [-2]    
        self.map_agents_to_submodels(submodels, self.submodel_string, agent_set, agents_index,
                                      dataset_pool=self.dataset_pool, 
                                      resources = Resources({"debug": self.debug}))
        result = array(agents_index.size*[-1], dtype="int32")
        if self.observations_mapping['mapped_index'].size == 0:
            logger.log_status("No agents mapped to submodels.")
            return result
        
        for submodel in submodels:
            result[self.observations_mapping[submodel]] = self._simulate_submodel(submodel, 
                                location_set, agent_set, agents_index)
        return result
    
    def _simulate_submodel(self, submodel, location_set, agent_set, agents_index):
        location_id_name = location_set.get_id_name()[0]
        subm_agents_index = agents_index[self.observations_mapping[submodel]]
        if self.submodel_string is not None:
            all_agents_in_subm = where(agent_set[self.submodel_string]==submodel)[0]
        else:
            all_agents_in_subm = arange(agent_set.size())
        if subm_agents_index.size <= 0:
            return array([], dtype='int32')
        #unplace agents
        agent_set.set_values_of_one_attribute(location_id_name, 
                                resize(array([-1]), subm_agents_index.size), subm_agents_index)
        
        agent_distr_in_loc = array(ndimage_sum(ones(all_agents_in_subm.size), 
                                         labels=agent_set[location_id_name][all_agents_in_subm], 
                                  index=location_set.get_id_attribute()))
 
        if self.filter is None:
            location_index = arange(location_set.size())
        else:
            submodel_filter = re.sub('SUBMODEL', str(submodel), self.filter)
            filter_values = location_set.compute_variables([submodel_filter], dataset_pool=self.dataset_pool)
            location_index = where(filter_values > 0)[0]
        if location_index.size <= 0:
            logger.log_status("No locations available. Nothing to be done.")
            return array(subm_agents_index.size*[-1], dtype="int32")
        logger.log_status("Submodel %s: %s %s(s) are scaled into %s %s(s)." % (submodel, 
                                                    subm_agents_index.size, agent_set.get_dataset_name(), 
                                                    location_index.size, location_set.get_dataset_name()))
        distr = agent_distr_in_loc[location_index]
        if ma.allclose(distr.sum(), 0):
            uniform_prob = 1.0/distr.size
            distr = resize(array([uniform_prob], dtype='float64'), distr.size)
            logger.log_warning("Probabilities in scaling model for submodel " + str(submodel) + " sum to 0.0.  Substituting uniform distribution!")
        distr = distr/float(distr.sum())
        random_sample = probsample_replace(location_set.get_id_attribute()[location_index], size=subm_agents_index.size, 
                                       prob_array=distr)
        #modify agents locations
        agent_set.set_values_of_one_attribute(location_id_name, random_sample, subm_agents_index)
        return random_sample
 
    def prepare_for_run(self, agent_set=None, agents_filter=None, agents_index=None):
        if agent_set is None or agents_filter is None:
            return agents_index
        filter = agent_set.compute_variables([agents_filter], dataset_pool=self.dataset_pool)
        if agents_index is not None:
            tmp = zeros(agent_set.size(), dtype='bool8')
            tmp[agents_index]=True
            filter = logical_and(filter, tmp)
        return where(filter)[0]

from opus_core.tests import opus_unittest
from numpy import array, ma, arange
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.building_dataset import BuildingDataset
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

        jobs_table_name = 'jobs'        
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
        model = ScalingAgentsModel(submodel_string='sector_id', debuglevel=4)
        model.run(gridcells, jobs, agents_index = arange(10000, 11750))
        # get results
        gridcells.compute_variables(["urbansim.gridcell.number_of_jobs_of_sector_15", "urbansim.gridcell.number_of_jobs_of_sector_1"], 
            resources = Resources({"job":jobs}))
        self.assertEqual((jobs['grid_id']>0).all(), True)
        # sector 1 jobs should be exactly the same
        result1 = gridcells.get_attribute("number_of_jobs_of_sector_1")
        self.assertEqual(ma.allclose(result1, array([1000, 1000, 1000]), rtol=0), True)
        # the distribution of sector 15 jobs should be the same with higher means 
        result2 = gridcells.get_attribute("number_of_jobs_of_sector_15")
#            logger.log_status(result2)
        self.assertEqual(ma.allclose(result2, array([5000, 2500, 1250]), rtol=0.05), True)
        
    def test_scaling_households_model(self):       
        storage = StorageFactory().get_storage('dict_storage')

        hhs_table_name = 'households'        
        storage.write_table(
            table_name=hhs_table_name,
            table_data={
                "household_id": arange(100)+1,
                "building_id":array(10*[1]+60*[2]+30*[-1])
                }
            )
        households = HouseholdDataset(in_storage=storage, in_table_name=hhs_table_name)
        
        buildings_table_name = 'buildings'        
        storage.write_table(
            table_name=buildings_table_name,
            table_data={"building_id":arange(2)+1}
            )
        buildings = BuildingDataset(in_storage=storage, in_table_name=buildings_table_name)
        
        # run model
        model = ScalingAgentsModel(debuglevel=4)
        model.run(buildings, households, agents_index = arange(70, 100))
        # all households are placed
        self.assertEqual((households['building_id']>0).all(), True)
        # get results
        buildings.compute_variables(["urbansim_parcel.building.number_of_households"], 
                                        resources = Resources({"household":households}))
        result = buildings["number_of_households"]
        self.assertEqual(result.sum(), 100)
        res_incr = result - array([10, 60]) # building increments
        # second building should get many more HHs than the first building (at least twice as much)
        self.assertEqual(res_incr[1] > 2*res_incr[0], True)
 


if __name__=="__main__":
    opus_unittest.main()
