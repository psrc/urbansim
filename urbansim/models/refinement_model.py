#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

import copy
from opus_core.model import Model
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
import numpy
from numpy import unique, logical_and, ones, zeros, concatenate
from numpy import where, histogram, round_, sort
from opus_core.misc import safe_array_divide
from opus_core.sampling_toolbox import sample_replace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger
from opus_core.variables.attribute_type import AttributeType

class RefinementModel(Model):
    """ Model refines simulation results by shifting agents' location around
    according to specified actions ('subtract', 'add', 'target', 'set_value', 'delete'):
    
    subtract - unplace/removes agents satisfying agent_expression from locations with location_expression being true;
    modify - takes agents that are unplaced by preceeding subtract action, and modify their attribute(s) to 
         match agent_expression and then place them to locations with location_expression being true, must share 
         year and transaction_id with a subtract action;
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

    def run(self, refinement_dataset=None, current_year=None, 
            action_order=['subtract', 'add', 'target', 'set_value', 'delete'],
            dataset_pool=None):
        
        """'refinement_dataset' is a RefinementDataset object.  see unittest for its columns
        """
        
        if refinement_dataset is None:
            refinement_dataset = dataset_pool.get_dataset('refinement')
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
        
        #refinements_this_year = copy.deepcopy(refinement_dataset)
        refinements_this_year = refinement_dataset
        this_year_index = where(refinement_dataset.get_attribute('year')==current_year)[0]
        refinements_this_year.subset_by_index(this_year_index, flush_attributes_if_not_loaded=False)
        
        transactions = refinements_this_year.get_attribute('transaction_id')
        actions = refinements_this_year.get_attribute('action')
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
                    
                    logger.log_status("Action: %s %i agents satisfying %s" % \
                                      (action_type, this_refinement.amount,
                                       ' and '.join( [this_refinement.agent_expression, 
                                                    this_refinement.location_expression] ).strip(' and ')
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
    def _subtract(self, agents_pool, amount, 
                  agent_dataset, location_dataset, 
                  this_refinement,
                  dataset_pool ):
        
        fit_index = self.get_fit_agents_index(agent_dataset, 
                                              this_refinement.agent_expression, 
                                              this_refinement.location_expression,
                                              dataset_pool)
        
        if amount > fit_index.size:
            logger.log_warning("Refinement requests to subtract %i agents,  but there are %i agents in total satisfying %s;" \
                               "subtract %i agents instead" % (amount, fit_index.size, 
                                                               ' and '.join( [this_refinement.agent_expression, 
                                                                            this_refinement.location_expression] ).strip(' and '),
                                                               fit_index.size) )
            amount = fit_index.size
        
        if amount == fit_index.size:
            movers_index = fit_index
        else:
            movers_index = sample_noreplace( fit_index, amount )
            
        agents_pool += movers_index.tolist()
        ## modify location capacity attribute if specified
        if this_refinement.location_capacity_attribute is not None and len(this_refinement.location_capacity_attribute) > 0:
            location_dataset = dataset_pool.get_dataset( VariableName( this_refinement.location_expression ).get_dataset_name() )

            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            # new=False argument to histogram tells it to use deprecated behavior for now (to be removed in numpy 1.3)
            # See numpy release notes -- search for histogram
            # TODO: remove this test and the new=False argument after numpy 1.2.0 or greater is required
            if numpy.__version__ >= '1.2.0':
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()), new=False)[0]
            else:
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()))[0]
            # correct version for numpy 1.2.0 and later:
            # num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size() +1) )[0]
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
            self._add_refinement_info_to_dataset(location_dataset, ("refinement_id", "transaction_id"), this_refinement, index=movers_location_index)
            
        agent_dataset.modify_attribute(location_dataset.get_id_name()[0], 
                                       -1 * ones( movers_index.size, dtype='int32' ),
                                       index = movers_index
                                       )
        self._add_refinement_info_to_dataset(agent_dataset, ("refinement_id", "transaction_id"), this_refinement, index=movers_index)
        
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
            if numpy.__version__ >= '1.2.0':
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()), new=False)[0]
            else:
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()) )[0]
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
            self._add_refinement_info_to_dataset(location_dataset, ("refinement_id", "transaction_id"), this_refinement, index=movers_location_index)
            
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
                logger.log_warning("Refinement requests to add %i agents,  but there are only %i agents subtracted from previous action(s) and no agents satisfying %s to clone from;" \
                                   "add %i agents instead" % (amount, amount_from_agents_pool, 
                                                              ' and '.join( [this_refinement.agent_expression, 
                                                                           this_refinement.location_expression]).strip(' and '), 
                                                              amount_from_agents_pool,) )

                amount = amount_from_agents_pool
                
                is_suitable_location = location_dataset.compute_variables( this_refinement.location_expression,
                                                                           dataset_pool=dataset_pool )
                location_id_for_agents_pool = sample_replace( location_dataset.get_id_attribute()[is_suitable_location],
                                                                 amount_from_agents_pool )
            else:
                
                agents_index_for_location = sample_replace( fit_index, amount_from_agents_pool)
                location_id_for_agents_pool = agent_dataset.get_attribute( location_dataset.get_id_name()[0] 
                                                                         )[agents_index_for_location]
                movers_index = concatenate( (movers_index, agents_index_for_location) )

        elif fit_index.size == 0:
            ## no agents in agents_pool and no agents to clone either, --> fail
            logger.log_error( "Action 'add' failed: there is no agent subtracted from previous action, and no suitable agents satisfying %s to clone from." % \
                              'and'.join( [this_refinement.agent_expression, this_refinement.location_expression] ).strip('and') )
            return
            
        if amount > amount_from_agents_pool:
            agents_index_to_clone = sample_replace( fit_index, amount - amount_from_agents_pool)
            movers_index = concatenate( (movers_index, agents_index_to_clone) )

        if movers_index.size > 0 and this_refinement.location_capacity_attribute is not None and len(this_refinement.location_capacity_attribute) > 0:
            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            # see previous comment about histogram function
            if numpy.__version__ >= '1.2.0':
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()), new=False)[0]
            else:
                num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()))[0]
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
            self._add_refinement_info_to_dataset(location_dataset, ("refinement_id", "transaction_id"), this_refinement, index=movers_location_index)
        if amount_from_agents_pool > 0:
            agent_dataset.modify_attribute( location_dataset.get_id_name()[0],
                                            location_id_for_agents_pool,
                                            agents_index_from_agents_pool
                                            )
            self._add_refinement_info_to_dataset(agent_dataset, ("refinement_id", "transaction_id"), this_refinement, index=agents_index_from_agents_pool)
        if amount > amount_from_agents_pool:
            new_agents_index = agent_dataset.duplicate_rows(agents_index_to_clone)
            self._add_refinement_info_to_dataset(agent_dataset, ("refinement_id", "transaction_id"), this_refinement, index=agents_index_to_clone)
            self._add_refinement_info_to_dataset(agent_dataset, ("refinement_id", "transaction_id"), this_refinement, index=new_agents_index)
        
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
        self._add_refinement_info_to_dataset(agent_dataset, ("refinement_id", "transaction_id"), this_refinement, index=fit_index)
            
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
    
            
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.datasets.dataset import Dataset
from numpy import arange, array, ma, allclose
import tempfile, os, shutil
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from urbansim.building.aliases import aliases


aliases +=[ 'raz_id = building.disaggregate(parcel.raz_id)' ]
class RefinementModelTest(opus_unittest.OpusTestCase):
    def setUp(self):
        building_data = {
            'building_id': array([1, 2, 3, 4, 5, 6, 7, 8]),
            'parcel_id':   array([1, 2, 2, 3, 4, 4, 5, 5]),
            'non_residential_sqft': \
                           array([6, 2, 3, 6, 1, 2, 5, 0]),
            'residential_units': \
                           array([0, 0, 0, 0, 0, 0, 1, 1])
            }
        parcel_data = {
            'parcel_id':                array([1, 2, 3, 4, 5]),
            'generic_land_use_type_id': array([6, 6, 3, 4, 1]),
            'raz_id':                   array([3, 4, 5, 5, 6])
            }
        job_data = {
            'job_id':      array([ 1, 2, 3, 4, 5, 6, 7, 8]),
            'building_id': array([ 1, 1, 2, 3, 6, 1, 6, 4]),
            'sector_id':   array([13,12,13,12,13,13,12,13]),
            'dummy_id':    array([ 1, 2, 3, 4, 5, 6, 7, 8])
        }
        household_data = {
            'household_id': array([1, 2]),
            'building_id':  array([7, 8]),
            'persons':      array([3, 4]),
        }
        person_data = {
            'person_id':    array([ 1,  2,  3,  4,  5,  6,  7]),
            'household_id': array([ 1,  1,  1,  2,  2,  2,  2]),
            'job_id':       array([ 2,  1, -1, -1,  3,  4,  7])
        }
        
        refinement_data = {
            'refinement_id': arange(1, 8),
            'year':          array([2021,2021,2021,2022, 2023, 2024, 2024]),
            'transaction_id':array([1,      1,   1,   2,    3,    1,    1]),
            'action':        array(['subtract', 'subtract', 'add', 'target', 'add', 'add', 'set_value']),
            'amount':        array([2,      1,   4,   7,    1,      1,    -1]),
            'agent_dataset': array(['job',
                                    'job',
                                    'job',
                                    'household',
                                    'household',
                                    'household',
                                    'person'
                                      ]),
            'agent_expression': array(['job.sector_id==13',
                                       'job.sector_id==13',
                                       '',
                                       'household.household_id>0',
                                       'household.persons>5',
                                       'household.persons==3',
                                       'person.job_id'
                                      ]),
            'location_expression': array(['urbansim.building.raz_id==3',
                                          'urbansim.building.raz_id==4',
                                          '(urbansim.building.raz_id==5) * (building.disaggregate(parcel.generic_land_use_type_id)==4)',
                                          'urbansim.building.raz_id==6',
                                          'urbansim.building.raz_id==6',
                                          'urbansim.building.raz_id==6',
                                          'household.refinement_id==6'
                                          ]),
            'location_capacity_attribute':array(['',
                                                 'non_residential_sqft',
                                                 'non_residential_sqft',
                                                 'residential_units',
                                                 'residential_units',
                                                 '',
                                                 ''
                                              ])
        }
        self.tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')

        SimulationState().set_cache_directory(self.tmp_dir)
        attribute_cache = AttributeCache()
        self.dataset_pool = SessionConfiguration(new_instance=True,
                                                 package_order=['urbansim', 'opus_core'],
                                                 in_storage=attribute_cache).get_dataset_pool()        

        #storage = StorageFactory().get_storage('flt_storage', storage_location=self.tmp_dir)
        attribute_cache.write_table(table_name = 'buildings', table_data = building_data)
        attribute_cache.write_table(table_name = 'parcels', table_data = parcel_data)
        attribute_cache.write_table(table_name = 'households', table_data = household_data)
        attribute_cache.write_table(table_name = 'jobs', table_data = job_data)
        attribute_cache.write_table(table_name = 'persons', table_data = person_data)
        attribute_cache.write_table(table_name = 'refinements', table_data = refinement_data)
        
        #self.dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim', 'opus_core'])
        self.refinement = self.dataset_pool.get_dataset('refinement')
        self.jobs = self.dataset_pool.get_dataset('job')
        self.persons = self.dataset_pool.get_dataset('person')
        self.hhs = self.dataset_pool.get_dataset('household')
        self.buildings = self.dataset_pool.get_dataset('building')
        #self.buildings.compute_variables('raz_id=building.disaggregate(parcel.raz_id)', self.dataset_pool)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        
    def test_transaction(self):
        model = RefinementModel()
        model.run(self.refinement, current_year=2021, dataset_pool=self.dataset_pool)
        jobs13_raz3 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(urbansim.building.raz_id==3))', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz4 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(urbansim.building.raz_id)==4)', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz5 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(urbansim.building.raz_id)==5)', 
                                                  dataset_pool=self.dataset_pool)        
        jobs_raz5 = self.jobs.compute_variables('job.disaggregate(urbansim.building.raz_id)==5', 
                                                dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(jobs13_raz3.sum(), 0)
        self.assertEqual(jobs13_raz4.sum(), 0)
        self.assertEqual(jobs13_raz5.sum() >= 5, True)
        self.assertEqual(jobs_raz5.sum(), 7)
        expected_nr_sqft = array([6, 0, 3, 6, 1, 6, 5, 0])
        ## was             array([6, 2, 3, 6, 1, 2, 5, 0]),
        self.assert_(allclose(self.buildings.get_attribute('non_residential_sqft'),  expected_nr_sqft))
        
    def test_target_action(self):
        model = RefinementModel()
        model.run(self.refinement, current_year=2022, dataset_pool=self.dataset_pool)
        hhs_raz6 = self.hhs.compute_variables('household.disaggregate(urbansim.building.raz_id==6)', 
                                              dataset_pool=self.dataset_pool)
        hhs_bldg = self.buildings.compute_variables('building.number_of_agents(household)', 
                                                    dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(hhs_raz6.sum(), 7)
        self.assert_(hhs_bldg.sum(),  7 )
        self.assert_((hhs_bldg!=0).sum(),  2)
        self.assert_(self.buildings.get_attribute('residential_units').sum(),  7)
        
    def test_no_action_if_no_suitable_agents_to_clone_from(self):
        model = RefinementModel()
        ##log a warning and nothing should happen
        import copy
        hhs = copy.copy(self.hhs.size())
        model.run(self.refinement, current_year=2023, dataset_pool=self.dataset_pool)
        hhs_p5 = self.hhs.compute_variables('household.persons>5')
        
        #check results
        self.assert_(self.hhs.size(),  hhs)
        self.assertEqual(hhs_p5.sum(), 0)

    def test_set_value_action(self):
        model = RefinementModel()
        model.run(self.refinement, current_year=2024, dataset_pool=self.dataset_pool)
        hhs_raz6 = self.hhs.compute_variables('household.disaggregate(urbansim.building.raz_id==6)', 
                                              dataset_pool=self.dataset_pool)
        hhs_bldg = self.buildings.compute_variables('building.number_of_agents(household)', 
                                                    dataset_pool=self.dataset_pool)
        
        #check results
        self.assertEqual(hhs_raz6.sum(), 3)
        self.assert_(hhs_bldg.sum(),  3 )
        self.assert_((hhs_bldg!=0).sum(),  2)
        self.assert_(allclose(self.persons.get_attribute('job_id'), array([-1,  -1, -1, -1,  3,  4,  7])))
        
if __name__=="__main__":
    opus_unittest.main()    
