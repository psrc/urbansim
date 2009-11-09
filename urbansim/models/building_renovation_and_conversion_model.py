# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import copy
from opus_core.model import Model
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
import numpy
from numpy import unique, logical_and, ones, zeros, concatenate
from numpy import where, histogram, round_, sort, array
from opus_core.misc import safe_array_divide
from opus_core.sampling_toolbox import sample_replace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger
from opus_core.variables.attribute_type import AttributeType
from urbansim.models.refinement_model import RefinementModel

class BuildingRenovationAndConversionModel(RefinementModel):
    """ 
    """
    
    model_name = "Building Renovation and Conversion Model"
    model_short_name = "BRCM"

    def run(self, refinement_dataset=None, current_year=None, 
            action_order=['subtract', 'add', 'multiple', 'set_value', 'convert', 'demolish', 'delete'],
            dataset_pool=None):
        
        """
        """
        
        if refinement_dataset is None:
            refinement_dataset = dataset_pool.get_dataset('refinement')
        self.id_names = (refinement_dataset.get_id_name()[0], 'transaction_id')
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
        
        #refinements_this_year = copy.deepcopy(refinement_dataset)
        refinements_this_year = refinement_dataset
        this_year_index = where(refinement_dataset.get_attribute('year')==current_year)[0]
        all_years_index = where(refinement_dataset.get_attribute('year')==-1)[0]
        refinements_this_year.subset_by_index(concatenate( (this_year_index, all_years_index) ), 
                                              flush_attributes_if_not_loaded=False)
        
        transactions = refinements_this_year.get_attribute('transaction_id')
        actions = refinements_this_year.get_attribute('action')
        for this_transaction in sort( unique(transactions) ):
            #transaction_list = [] # list of each action in this transaction
            agents_pool = []  # index to agents to keep track agent within 1 transaction
            logger.start_block("Transaction %i" % this_transaction)
            for action_type in action_order:
                action_function = getattr(self, '_' + action_type)
                for refinement_index in where( logical_and(transactions==this_transaction, actions == action_type))[0]:
                    this_refinement = refinements_this_year.get_data_element(refinement_index)
                    ## get agent_dataset and location_dataset if specified
                    agent_dataset_name = this_refinement.agent_dataset
                    agent_dataset = dataset_pool.get_dataset( agent_dataset_name )
                    location_dataset = None
                    logger.log_status("Action: %s\nAmount: %s\nAttribute: %s\nFilter: %s" % \
                                      (action_type, this_refinement.amount, this_refinement.agent_attribute, 
                                       this_refinement.agent_filter
                                       ) )
                    action_function( agents_pool, this_refinement.amount,
                                     agent_dataset, location_dataset, 
                                     this_refinement, 
                                     dataset_pool )
                    
                    agent_dataset.flush_dataset()
                    dataset_pool._remove_dataset(agent_dataset.get_dataset_name())
                    if location_dataset is not None:
                        location_dataset.flush_dataset()
                        dataset_pool._remove_dataset(location_dataset.get_dataset_name())
                    
            ## delete agents still in agents_pool at the end of the transaction
            #agent_dataset.remove_elements( array(agents_pool) )
            
            
#            dataset_pool.flush_loaded_datasets()
#            dataset_pool.remove_all_datasets()
                        
            logger.end_block()
                
    ## methods handling "action" in refinement_dataset
        
    def _delete(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        """similar to subtract action, instead of unplacing agents delete remove agents from the agent dataset,
        those agents won't be available for later action
        """
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_filter, 
                                              '',
                                              dataset_pool)
        
        if amount > fit_index.size or amount < 0:
            logger.log_warning("Request to delete %i agents,  but there are %i agents in total satisfying %s;" \
                               "delete %i agents instead" % (amount, fit_index.size, 
                                                               this_refinement.agent_filter,
                                                               fit_index.size) )
            amount = fit_index.size
        
        if amount == fit_index.size:
            movers_index = fit_index
        else:
            movers_index = sample_noreplace( fit_index, amount )
            
        agents_pool = list( set(agents_pool) - set(movers_index) )
            
        agent_dataset.remove_elements( array(movers_index) )

    def _demolish(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        self._delete(agents_pool, amount, agent_dataset, location_dataset, this_refinement, dataset_pool)
                
    def _set_value(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset,
                                              this_refinement.agent_filter, 
                                              '', 
                                              dataset_pool)
        agent_dataset.modify_attribute( this_refinement.agent_attribute,
                                        amount,
                                        fit_index
                                        )
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=fit_index)

    def _convert(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        self._set_value(agents_pool, amount, 
                       agent_dataset, location_dataset, 
                       this_refinement,
                       dataset_pool)

    def _add(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset,
                                              this_refinement.agent_filter, 
                                              '', 
                                              dataset_pool)
        new_values = agent_dataset.get_attribute_by_index(this_refinement.agent_attribute, fit_index) + amount
        agent_dataset.modify_attribute( this_refinement.agent_attribute,
                                        new_values,
                                        fit_index
                                        )
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=fit_index)

    def _subtract(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        self._add(agents_pool, -amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool)

    def _multiple(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset,
                                              this_refinement.agent_filter, 
                                              '', 
                                              dataset_pool)
        new_values = agent_dataset.get_attribute_by_index(this_refinement.agent_attribute, fit_index) * amount
        agent_dataset.modify_attribute( this_refinement.agent_attribute,
                                        new_values,
                                        fit_index
                                        )
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=fit_index)
