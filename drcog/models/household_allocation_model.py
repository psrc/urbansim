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

class HouseholdAllocationModel(Model):
    """Allocates households from submarket to building.
    """
    model_name = "Household Allocation Model"

    def run(self, agents_index=None):
        """Allocates households from submarket to building.
        """
        def building_match(idx_hhs, idx_blds):        
            resunits = np.array([np.maximum(np.ones(idx_blds.size),(building_set['vacant_units'][idx_blds])),]*idx_hhs.size)
            row_sums = resunits.sum(axis=1)
            probabilities = (resunits) / (np.array([(row_sums),]*idx_blds.size).transpose())
            resources = Resources({"capacity":building_set['vacant_units'][idx_blds],"lottery_max_iterations":50})
            choices = lottery_choices().run(probabilities, resources=resources)
            counter = 0
            for choice in choices:
                if choice == -1:
                    household_set['building_id'][idx_hhs[counter]] = -1
                else:
                    household_set['building_id'][idx_hhs[counter]] = building_set['building_id'][idx_blds[choice]] 
                counter += 1        
                
        def random_match(idx_hhs, idx_blds):
            resunits = np.array([np.maximum(np.ones(idx_blds.size),(building_set['residential_units'][idx_blds])),]*idx_hhs.size)
            row_sums = resunits.sum(axis=1)
            probabilities = (resunits) / (np.array([(row_sums),]*idx_blds.size).transpose())
            choices = random_choices().run(probabilities)
            counter = 0
            for choice in choices:
                household_set['building_id'][idx_hhs[counter]] = building_set['building_id'][idx_blds[choice]] 
                counter += 1
        
        dataset_pool = SessionConfiguration().get_dataset_pool()
        submarket_set = dataset_pool.get_dataset('submarket')
        building_set = dataset_pool.get_dataset('building')
        household_set = dataset_pool.get_dataset('household')

        building_set.add_attribute(name='submarket_id', data=building_set.compute_variables('drcog.building.submarket_id'))
        building_set.add_primary_attribute(name='vacant_units', data=building_set.compute_variables('building.residential_units - building.number_of_agents(household)'))
        
        agents_submarkets = household_set.get_attribute('submarket_id')
        building_submarkets = building_set.get_attribute('submarket_id')
        
        hh_building_ids = household_set.get_attribute('building_id')
        
        submarkets = np.unique(agents_submarkets[agents_index])
        
        cond_array = np.zeros(household_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        
        for submarket_id in submarkets:
            index_hh = np.where(np.logical_and(cond_array, agents_submarkets == submarket_id))[0]
            if index_hh.size>0:
                logger.log_status('Submarket %s: %s agents to place.' % (submarket_id,index_hh.size))
            index_bld = np.where(building_submarkets == submarket_id)[0]
            if (index_hh.size > 0) and (index_bld.size > 1):
                building_match(index_hh, index_bld)
            elif (index_hh.size > 0) and (index_bld.size == 1):
                bld_id = building_set['building_id'][index_bld]
                household_set['building_id'][index_hh] = np.array(index_hh.size*[bld_id])
            else:
                logger.log_status('No buildings in submarket %s. %s agents unplaced.' % (submarket_id,index_hh.size))
                
        building_set.delete_one_attribute('vacant_units')
        
        agents_index = np.where(household_set['building_id']==-1)
        submarkets = np.unique(agents_submarkets[agents_index])
        cond_array = np.zeros(household_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        
        for submarket_id in submarkets:
            index_hh = np.where(np.logical_and(cond_array, agents_submarkets == submarket_id))[0]
            logger.log_status('Submarket %s: %s agents to randomly place.' % (submarket_id,index_hh.size)) 
            index_bld = np.where(building_submarkets == submarket_id)[0]
            if (index_hh.size > 0) and (index_bld.size > 0):
                random_match(index_hh, index_bld)
        