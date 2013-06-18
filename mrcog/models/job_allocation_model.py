# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
import numpy as np
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from urbansim.lottery_choices import lottery_choices
from urbansim.random_choices import random_choices
from opus_core.resources import Resources

#from IPython import embed

class JobAllocationModel(Model):
    """Allocates jobs from employment submarket to building.
    """
    model_name = "Job Allocation Model"

    def run(self, agents_index=None):
        """Allocates jobs from employment submarket to building.
        """
        def building_match(idx_estabs, idx_blds):        
            units = np.array([np.maximum(np.ones(idx_blds.size),(building_set['vacant_units'][idx_blds])),]*idx_estabs.size)
            row_sums = units.sum(axis=1)
            probabilities = (units) / (np.array([(row_sums),]*idx_blds.size).transpose())
            resources = Resources({"capacity":building_set['vacant_units'][idx_blds],"lottery_max_iterations":50})
            choices = lottery_choices().run(probabilities, resources=resources)
            counter = 0
            for choice in choices:
                if choice == -1:
                    job_set['building_id'][idx_estabs[counter]] = -1
                else:
                    job_set['building_id'][idx_estabs[counter]] = building_set['building_id'][idx_blds[choice]] 
                counter += 1        
                
        def random_match(idx_estabs, idx_blds):
            units = np.array([np.maximum(np.ones(idx_blds.size),(building_set['non_residential_sqft'][idx_blds])),]*idx_estabs.size)
            row_sums = units.sum(axis=1)
            probabilities = (units) / (np.array([(row_sums),]*idx_blds.size).transpose())
            choices = random_choices().run(probabilities)
            counter = 0
            for choice in choices:
                job_set['building_id'][idx_estabs[counter]] = building_set['building_id'][idx_blds[choice]] 
                counter += 1
        
        dataset_pool = SessionConfiguration().get_dataset_pool()
        esubmarket_set = dataset_pool.get_dataset('employment_submarket')
        building_set = dataset_pool.get_dataset('building')
        job_set = dataset_pool.get_dataset('job')

        building_set.add_attribute(name='employment_submarket_id', data=building_set.compute_variables('mrcog.building.employment_submarket_id'))
        building_set.add_primary_attribute(name='vacant_units', data=building_set.compute_variables('building.non_residential_sqft/250 - building.number_of_agents(job)'))
        
        agents_esubmarkets = job_set.get_attribute('employment_submarket_id')
        building_esubmarkets = building_set.get_attribute('employment_submarket_id')
        
        estab_building_ids = job_set.get_attribute('building_id')
        
        esubmarkets = np.unique(agents_esubmarkets[agents_index])
        
        cond_array = np.zeros(job_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        
        for employment_submarket_id in esubmarkets:
            index_estab = np.where(np.logical_and(cond_array, agents_esubmarkets == employment_submarket_id))[0]
            if index_estab.size>0:
                logger.log_status('Esubmarket %s: %s agents to place.' % (employment_submarket_id,index_estab.size))
            index_bld = np.where(building_esubmarkets == employment_submarket_id)[0]
            if (index_estab.size > 0) and (index_bld.size > 1):
                building_match(index_estab, index_bld)
            elif (index_estab.size > 0) and (index_bld.size == 1):
                bld_id = building_set['building_id'][index_bld]
                job_set['building_id'][index_estab] = np.array(index_estab.size*[bld_id])
            else:
                logger.log_status('No buildings in esubmarket %s. %s agents unplaced.' % (employment_submarket_id,index_estab.size))
                
        building_set.delete_one_attribute('vacant_units')
        
        agents_index = np.where(job_set['building_id']==-1)[0]
        esubmarkets = np.unique(agents_esubmarkets[agents_index])
        cond_array = np.zeros(job_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        
        for employment_submarket_id in esubmarkets:
            index_estab = np.where(np.logical_and(cond_array, agents_esubmarkets == employment_submarket_id))[0]
            logger.log_status('Esubmarket %s: %s agents to randomly place.' % (employment_submarket_id,index_estab.size)) 
            index_bld = np.where(building_esubmarkets == employment_submarket_id)[0]
            if (index_estab.size > 0) and (index_bld.size > 0):
                random_match(index_estab, index_bld)
        