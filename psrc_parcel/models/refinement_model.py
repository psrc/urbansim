# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import copy
from opus_core.model import Model
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
import numpy
from numpy import logical_and, ones, zeros, concatenate, unique
from numpy import where, histogram, round_, sort, array, in1d
from opus_core.misc import safe_array_divide, unique
from opus_core.sampling_toolbox import sample_replace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger
from opus_core.variables.attribute_type import AttributeType

class RefinementModel(Model):
    """ Model refines simulation results by shifting agents' location around
    according to specified actions ('subtract', 'add', 'target', 'set_value', 'delete'):
    
    subtract - unplace/removes agents satisfying agent_expression from locations with location_expression being true;
    add - adds agents with attributes matching agent_expression to locations with location_expression being true; 
         If sharing year and transaction_id with a subtract action, it first place agents that are unplaced by subtract 
         action and satisfy agents_expression condition. If not, or if there are less unplaced agents than the specified
         amount, it randomly clones existing agents with matching agent_expression and location_expression;
    target - subtract or add agents with matching agent_expression and location_expression to achieve the specified amount
    
    location_capacity_attribute - if specified, the model will proportionally modify the specified attribute 
         based on number of agents placed/unplaced proportion to existing number of agents at the location
    """
    
    model_name = "Refinement Model"
    model_short_name = "RM"

    def __init__(self, model_name=None, model_short_name=None, *args, **kwargs):
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
        Model.__init__(self, *args, **kwargs)

    def run(self, refinement_dataset=None, current_year=None, base_year=2000,
            action_order=['subtract', 'target', 'add', 'set_value', 'delete'],
            dataset_pool=None):
        
        """'refinement_dataset' is a RefinementDataset object.  see unittest for its columns
        """
        
        if refinement_dataset is None:
            refinement_dataset = dataset_pool.get_dataset('refinement')
        self.id_names = (refinement_dataset.get_id_name()[0], 'transaction_id')
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
        
        # get MPDs
        SimulationState().set_current_time(base_year)
        base_storage = AttributeCache(SimulationState().get_cache_directory())
        self.mpds = Dataset(in_storage=base_storage, dataset_name='development_project_proposal', 
                                in_table_name='development_project_proposals',
                                id_name='proposal_id')
        SimulationState().set_current_time(current_year)
        
        #refinements_this_year = copy.deepcopy(refinement_dataset)
        refinements_this_year = refinement_dataset
        this_year_index = where(refinement_dataset.get_attribute('year')==current_year)[0]
        all_years_index = where(refinement_dataset.get_attribute('year')==-1)[0]
        refinements_this_year.subset_by_index(concatenate( (this_year_index, all_years_index) ), 
                                              flush_attributes_if_not_loaded=False)
        
        transactions = refinements_this_year.get_attribute('transaction_id')
        actions = refinements_this_year.get_attribute('action')
        all_agent_datasets = []
        self.processed_locations = {}
        for this_transaction in sort( unique(transactions) ):
            #transaction_list = [] # list of each action in this transaction
            agents_pool = []  # index to agents to keep track agent within 1 transaction
            logger.start_block("Refinement transaction %i" % this_transaction)
            for action_type in action_order:
                action_function = getattr(self, '_' + action_type)
                for refinement_index in where( logical_and(transactions==this_transaction, actions == action_type))[0]:
                    this_refinement = refinements_this_year.get_data_element(refinement_index)
                    ## get agent_dataset and location_dataset if specified
                    if not hasattr(this_refinement, 'agent_dataset') or len(this_refinement.agent_dataset)==0:
                        agent_dataset_name = VariableName( this_refinement.agent_expression ).get_dataset_name()
                    else:
                        agent_dataset_name = this_refinement.agent_dataset
                    agent_dataset = dataset_pool.get_dataset( agent_dataset_name )
                    location_dataset = None
                    if len(this_refinement.location_expression)>0:
                        location_dataset = dataset_pool.get_dataset( VariableName( this_refinement.location_expression ).get_dataset_name() )
                    
                    if location_dataset.get_id_name()[0] not in agent_dataset.get_known_attribute_names():
                        agent_dataset.compute_variables('urbansim_parcel.%s.%s' % 
                            (agent_dataset.get_dataset_name(), location_dataset.get_id_name()[0]), dataset_pool=dataset_pool)

                    logger.log_status("Action: %s %i agents satisfying %s" % \
                                  (action_type, this_refinement.amount,
                                   ' and '.join( [this_refinement.agent_expression, 
                                                this_refinement.location_expression] ).strip(' and ')
                               ) )
                    if len(agents_pool) == 0: # add unplaced agents into the pool
                        agents_pool += (where(agent_dataset[location_dataset.get_id_name()[0]] < 0)[0]).tolist()
                        
                    action_function( agents_pool, this_refinement.amount,
                                 agent_dataset, location_dataset, 
                                 this_refinement, 
                                 dataset_pool )
                
                    if location_dataset.get_dataset_name() == 'zone' and 'zone_id' not in agent_dataset.get_primary_attribute_names():
                        zones = agent_dataset['zone_id'].copy()
                        agent_dataset.delete_one_attribute('zone_id')
                        agent_dataset.add_attribute(name='zone_id', data=zones, metadata=1)
                    if location_dataset.get_dataset_name() <> 'zone' and 'zone_id' in agent_dataset.get_primary_attribute_names():
                        agent_dataset.delete_one_attribute('zone_id')
                        
                    agent_dataset.flush_dataset()
                    #if 'zone_id' in agent_dataset.get_known_attribute_names():
                    #    agent_dataset.get_attribute('zone_id')
                    dataset_pool._remove_dataset(agent_dataset.get_dataset_name())
                    if location_dataset is not None:
                        location_dataset.flush_dataset()
                        dataset_pool._remove_dataset(location_dataset.get_dataset_name())
                    all_agent_datasets += [agent_dataset]
                
            #for agents in all_agent_datasets:
            #    agents.flush_dataset()
                    
            ## delete agents still in agents_pool at the end of the transaction
            #agent_dataset.remove_elements( array(agents_pool) )
            
            
#            dataset_pool.flush_loaded_datasets()
#            dataset_pool.remove_all_datasets()
                        
            logger.end_block()

            
        return self.processed_locations
            
    def get_fit_agents_index(self, agent_dataset, 
                             agent_expression, 
                             location_expression,
                             dataset_pool):
        if agent_expression is not None and len(agent_expression) > 0:
            #agent_exp_vname= VariableName(  )
            agents_indicator = agent_dataset.compute_variables(agent_expression, 
                                                               dataset_pool=dataset_pool)
        else:
            agents_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        
        if location_expression is not None and len(location_expression) > 0:
            #location_exp_vname= VariableName("%s.disaggregate(%s)"  % ( agent_dataset.dataset_name, 
                                                                        #location_expression ))
            location_indicator = agent_dataset.compute_variables( "%s.disaggregate(%s)"  % ( agent_dataset.dataset_name, 
                                                                                             location_expression ),
                                                                 dataset_pool=dataset_pool)
        else:
            location_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        fit_index = where ( agents_indicator * location_indicator )[0]
        
        return fit_index
    
    def get_fit_agents_index_bldgs(self, agent_dataset, 
                             agent_expression, 
                             location_expression,
                             dataset_pool):
        bldgs = dataset_pool.get_dataset('building')
        if agent_expression is not None and len(agent_expression) > 0:
            #agent_exp_vname= VariableName(  )
            agents_indicator = agent_dataset.compute_variables(agent_expression, 
                                                               dataset_pool=dataset_pool)
        else:
            agents_indicator = ones( agent_dataset.size(), dtype='bool' )

        bldgs_indicator = in1d(bldgs.get_id_attribute(), agent_dataset['building_id'][where(agents_indicator)[0]])
        
        
        if location_expression is not None and len(location_expression) > 0:
            #location_exp_vname= VariableName("%s.disaggregate(%s)"  % ( agent_dataset.dataset_name, 
                                                                        #location_expression ))
            location_indicator = bldgs.compute_variables( "%s.disaggregate(%s)"  % ( bldgs.dataset_name, 
                                                                                             location_expression ),
                                                                 dataset_pool=dataset_pool)
        else:
            location_indicator = ones( bldgs.size(), dtype='bool' )

        fit_index = where ( bldgs_indicator * location_indicator * (in1d(bldgs['parcel_id'], self.mpds['parcel_id'])==0) * (bldgs['year_built'] > 2000))[0]
        
        return (fit_index, agents_indicator)
    
    def _add_refinement_info_to_dataset(self, dataset, names, refinement, default_value=-1, index=None):
        for name in names:
            value = getattr(refinement, name)
            if index is None:
                values = value + zeros(dataset.size(), dtype=type(value))
            else:
                values = value + zeros(index.size, dtype=type(value) )
            self._add_or_modify_attribute(dataset, name, values, default_value=default_value, index=index, metadata=AttributeType.PRIMARY)
    
    def _add_or_modify_attribute(self, dataset, attribute_name, values, default_value=-1, index=None, metadata=2):
        """add attribute_name if not presented in dataset attribute names, modify it otherwise
        used to add attributes in refinement dataset to affects agent set /location set
        """
        #if not (isinstance(values, ndarray)):
            #if index is not None:
                #values = values + zeros(index.size(), dtype=type(values) )
            #else:
                #values = values + zeros(dataset.size(), dtype=type(values) )
            
        if attribute_name not in dataset.get_known_attribute_names():
            if index is not None:  ## if values only contain part of elements for the new attribute, fill the rest with default values
                initial_values = default_value + zeros(dataset.size(), dtype=values.dtype )
                initial_values[index] = values
            else:
                initial_values = values
            dataset.add_attribute(initial_values, attribute_name, metadata=metadata)
        else:
            dataset.modify_attribute(attribute_name, values, index=index)
            
    ## methods handling "action" in refinement_dataset
    def _clone(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        """ clone certain amount of agent satisfying condition specified by agent_expression and location_expression
        and add them to agents_pool.  Useful to add certain agents to location where there is no such agent exist previously.
        """
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        if fit_index.size == 0:
            logger.log_error("Refinement requests to clone %i agents,  but there are no agents satisfying %s." \
                                % (amount,  ' and '.join( [this_refinement.agent_expression, 
                                                           this_refinement.location_expression] ).strip(' and '),
                                                         ))
            return
       
        
        clone_index = sample_replace( fit_index, amount )
            
        agents_pool += clone_index.tolist()
           
        agent_dataset.modify_attribute(location_dataset.get_id_name()[0], 
                                       -1 * ones( clone_index.size, dtype='int32' ),
                                       index = clone_index
                                       )
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=clone_index)


    def _subtract(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        bldgs = dataset_pool.get_dataset('building')
        (fit_index, agents_indicator) = self.get_fit_agents_index_bldgs(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        count = bldgs.sum_dataset_over_ids(agent_dataset, constant=agents_indicator)[fit_index]

        if amount > count.sum():
            logger.log_warning("Refinement requests to subtract %i agents,  but there are %i agents in total satisfying %s;" \
                               "subtract %i agents instead" % (amount, count.sum(), 
                                                               ' and '.join( [this_refinement.agent_expression, 
                                                                            this_refinement.location_expression] ).strip(' and '),
                                                               count.sum()) )
            amount = count.sum()
        
        if amount == count.sum():
            bldgs_movers_index = fit_index
        else:
            bldgs_movers_index = sample_noreplace(fit_index, 1, return_index=True)
            mask = ones(fit_index.size, dtype='bool8')
            while count[bldgs_movers_index].sum() < amount:
                mask[bldgs_movers_index] = False             
                bldgs_movers_index = concatenate((bldgs_movers_index, sample_noreplace( where(mask)[0], 1 )))
            bldgs_movers_index = fit_index[bldgs_movers_index]
            
        agents_index = where(agents_indicator)[0]
        movers_index = agents_index[where(in1d(agent_dataset['building_id'][agents_index], bldgs.get_id_attribute()[bldgs_movers_index]))[0]]

        agents_pool += movers_index.tolist()
        bldgs.remove_elements(bldgs_movers_index)
        logger.log_status("%s buildings removed." % bldgs_movers_index.size)
                    
        agent_dataset.modify_attribute(location_dataset.get_id_name()[0], 
                                       -1 * ones( movers_index.size, dtype='int32' ),
                                       index = movers_index
                                       )
        for synch_dataset_name in ['job', 'household']:
            if synch_dataset_name <> agent_dataset.get_dataset_name():
                synch_dataset = dataset_pool.get_dataset(synch_dataset_name)
                idx = where(in1d(synch_dataset['building_id'], bldgs.get_id_attribute()[bldgs_movers_index]))[0]
            else:
                synch_dataset = agent_dataset
                idx = movers_index
            synch_dataset.modify_attribute('building_id', 
                                       -1 * ones( idx.size, dtype='int32' ),
                                       index = idx)
            logger.log_status("%s %ss unplaced." % (idx.size, synch_dataset_name))
            
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=movers_index)
        
    def _delete(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        """similar to subtract action, instead of unplacing agents delete remove agents from the agent dataset,
        those agents won't be available for later action
        """
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        
        if amount > fit_index.size or amount < 0:
            logger.log_warning("Refinement requests to delete %i agents,  but there are %i agents in total satisfying %s;" \
                               "delete %i agents instead" % (amount, fit_index.size, 
                                                               ' and '.join( [this_refinement.agent_expression, 
                                                                            this_refinement.location_expression] ).strip(' and '),
                                                               fit_index.size) )
            amount = fit_index.size
        
        if amount == fit_index.size:
            movers_index = fit_index
        else:
            movers_index = sample_noreplace( fit_index, amount )
            
        agents_pool = list( set(agents_pool) - set(movers_index) )
        ## modify location capacity attribute if specified
        if this_refinement.location_capacity_attribute is not None and len(this_refinement.location_capacity_attribute) > 0:
            location_dataset = dataset_pool.get_dataset( VariableName( this_refinement.location_expression ).get_dataset_name() )

            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            # see previous comment about histogram function
            num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size() +1) )[0]
            num_of_agents_by_location = location_dataset.compute_variables( "number_of_agents=%s.number_of_agents(%s)" % \
                                                                            (location_dataset.dataset_name,
                                                                            agent_dataset.dataset_name),
                                                                            dataset_pool=dataset_pool)
            
            shrink_factor = safe_array_divide( (num_of_agents_by_location - num_of_movers_by_location ).astype('float32'),
                                                num_of_agents_by_location, return_value_if_denominator_is_zero = 1.0  )
            new_values = round_( shrink_factor * location_dataset.get_attribute(this_refinement.location_capacity_attribute) )
            location_dataset.modify_attribute( this_refinement.location_capacity_attribute, 
                                               new_values
                                               )
            self._add_refinement_info_to_dataset(location_dataset, self.id_names, this_refinement, index=movers_location_index)
            
        agent_dataset.remove_elements( array(movers_index) )
                
    def _add(self, agents_pool, amount, 
             agent_dataset, location_dataset, 
             this_refinement,
             dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        movers_index = array([],dtype="int32")
        amount_from_agents_pool = min( amount, len(agents_pool) )
        if amount_from_agents_pool > 0:
            agents_index_from_agents_pool = sample_noreplace( agents_pool, amount_from_agents_pool )
            [ agents_pool.remove(i) for i in agents_index_from_agents_pool ]
            if fit_index.size == 0:
                ##cannot find agents to copy their location or clone them, place agents in agents_pool
                if amount > amount_from_agents_pool:                   
                    logger.log_warning("Refinement requests to add %i agents,  but there are only %i agents subtracted from previous action(s) and no agents satisfying %s to clone from;" \
                                   "add %i agents instead" % (amount, amount_from_agents_pool, 
                                                              ' and '.join( [this_refinement.agent_expression, 
                                                                           this_refinement.location_expression]).strip(' and '), 
                                                              amount_from_agents_pool,) )
                    amount = amount_from_agents_pool
                # sample from all suitable locations
                is_suitable_location = location_dataset.compute_variables( this_refinement.location_expression,
                                                                           dataset_pool=dataset_pool )
                location_id_for_agents_pool = sample_replace( location_dataset.get_id_attribute()[is_suitable_location],
                                                                 amount_from_agents_pool )
            else:
                #sample from locations of suitable agents            
                agents_index_for_location = sample_replace( fit_index, amount_from_agents_pool)
                location_id_for_agents_pool = agent_dataset.get_attribute( location_dataset.get_id_name()[0] 
                                                                         )[agents_index_for_location]
                movers_index = concatenate( (movers_index, agents_index_for_location) )

        elif fit_index.size == 0:
            ## no agents in agents_pool and no agents to clone either, --> fail
            logger.log_error( "Action 'add' failed: there is no agent subtracted from previous action, and no suitable agents satisfying %s to clone from." % \
                              ' and '.join( [this_refinement.agent_expression, this_refinement.location_expression] ).strip('and') )
            return
            
        if amount > amount_from_agents_pool:
            agents_index_to_clone = sample_replace( fit_index, amount - amount_from_agents_pool)
            movers_index = concatenate( (movers_index, agents_index_to_clone) )

        if movers_index.size > 0 and this_refinement.location_capacity_attribute is not None and len(this_refinement.location_capacity_attribute) > 0:
            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            # see previous comment about histogram function
            num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size() +1) )[0]
            num_of_agents_by_location = location_dataset.compute_variables( "number_of_agents=%s.number_of_agents(%s)" % \
                                                                            ( location_dataset.dataset_name,
                                                                            agent_dataset.dataset_name ),
                                                                            dataset_pool=dataset_pool)
            
            expand_factor = safe_array_divide( (num_of_agents_by_location + num_of_movers_by_location ).astype('float32'),
                                                num_of_agents_by_location, return_value_if_denominator_is_zero = 1.0 )
            new_values = round_( expand_factor * location_dataset.get_attribute(this_refinement.location_capacity_attribute) )
            location_dataset.modify_attribute( this_refinement.location_capacity_attribute, 
                                               new_values
                                           )
            self._add_refinement_info_to_dataset(location_dataset, self.id_names, this_refinement, index=movers_location_index)
        if amount_from_agents_pool > 0:
            agent_dataset.modify_attribute( 'building_id',
                                            -1 * ones( agents_index_from_agents_pool.size, dtype='int32' ),
                                            agents_index_from_agents_pool
                                            )
            agent_dataset.modify_attribute( location_dataset.get_id_name()[0],
                                            location_id_for_agents_pool,
                                            agents_index_from_agents_pool
                                            )

            self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=agents_index_from_agents_pool)
            self.processed_locations['add'] = concatenate((self.processed_locations.get('add', array([])), 
                                                unique(location_dataset['zone_id'][location_dataset.get_id_index(location_id_for_agents_pool)])))
            
        if amount > amount_from_agents_pool:
            new_agents_index = agent_dataset.duplicate_rows(agents_index_to_clone)
            self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=agents_index_to_clone)
            self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=new_agents_index)
            if location_dataset.get_dataset_name() <> 'building':
                agent_dataset.modify_attribute( 'building_id',
                                            -1 * ones( new_agents_index.size, dtype='int32' ),
                                            new_agents_index
                                            )
            self.processed_locations['add'] = concatenate((self.processed_locations.get('add', array([])), 
                                                unique(agent_dataset['zone_id'][new_agents_index])))
            
    def _set_value(self, agents_pool, amount, 
                   agent_dataset, location_dataset, 
                   this_refinement,
                   dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              '', 
                                              this_refinement.location_expression,
                                              dataset_pool)
        agent_dataset.modify_attribute( this_refinement.agent_expression,
                                        amount,
                                        fit_index
                                        )
        self._add_refinement_info_to_dataset(agent_dataset, self.id_names, this_refinement, index=fit_index)
            
    def _target(self, agents_pool, amount, 
                agent_dataset, location_dataset, 
                this_refinement,
                dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        if fit_index.size > amount:
            logger.log_status("%i agents satisfying conditions, greater than target and to subtract %i agents" % \
                              (amount, fit_index.size - amount ) )
            self._subtract( agents_pool, fit_index.size - amount,
                            agent_dataset, location_dataset, 
                            this_refinement,
                            dataset_pool)
        elif fit_index.size < amount:
            logger.log_status("%i agents satisfying conditions, less than target and to add %i agents" % \
                              (amount, amount - fit_index.size ) )
            self._add( agents_pool, amount - fit_index.size,
                       agent_dataset, location_dataset, 
                       this_refinement,
                       dataset_pool)
        else:
            logger.log_status("%i agents satisfying conditions, meeting target and to do nothing" %  amount )
            
            
    def _synchronize(self, agents_pool, amount, 
                     agent_dataset, location_dataset, 
                     this_refinement,
                     dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              '', 
                                              this_refinement.location_expression,
                                              dataset_pool)
        
        
        pass

    def prepare_for_run(self, refinement_dataset_name=None, 
                        refinement_storage=None, 
                        refinement_table_name=None):
        from opus_core.datasets.dataset_factory import DatasetFactory
        from opus_core.session_configuration import SessionConfiguration
        df = DatasetFactory()
        if not refinement_dataset_name:
            refinement_dataset_name = df.dataset_name_for_table(refinement_table_name)
        
        refinement = df.search_for_dataset(refinement_dataset_name,
                                           package_order=SessionConfiguration().package_order,
                                           arguments={'in_storage':refinement_storage, 
                                                      'in_table_name':refinement_table_name}
                                       )
        return refinement
    