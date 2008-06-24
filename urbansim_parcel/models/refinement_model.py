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

import copy
from opus_core.model import Model
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.variable_name import VariableName
from numpy import unique, logical_and, ones, concatenate
from numpy import where, histogram, round_, sort
from opus_core.misc import safe_array_divide
from opus_core.sampling_toolbox import sample_replace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger

class RefinementModel(Model):
    """ Model refines simulation results by shifting agents' location around
    according to specified actions ('subtract', 'modify', 'add', 'target'):
    
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
            action_order=['subtract', 'modify', 'add', 'target'],
            dataset_pool=None):
        
        """'refinement_dataset' is a RefineDataset object.  see unittest for its columns
        """
        
        if refinement_dataset is None:
            refinement_dataset = dataset_pool.get_dataset('refinement')
        
        if current_year is None:
            current_year = SimulationState().get_current_time()
        
        refinements_this_year = copy.deepcopy(refinement_dataset)
        refinements_this_year.subset_by_index(where(refinement_dataset.get_attribute('year')==current_year)[0])

        transactions = refinements_this_year.get_attribute('transaction_id')
        actions = refinements_this_year.get_attribute('action')
        for this_transaction in sort( unique(transactions) ):
            agents_pool = []  # index to agents to keep track agent within 1 transaction
            agent_expressions = refinements_this_year.get_attribute_by_index('agent_expression', transactions==this_transaction)
            agent_expressions = [ e for e in unique( agent_expressions ) if len(e) > 0]
            location_expressions = refinements_this_year.get_attribute_by_index('location_expression', transactions==this_transaction)
            location_expressions = [ e for e in unique( location_expressions ) if len(e) > 0]
            agent_dataset = dataset_pool.get_dataset( VariableName( agent_expressions[0] ).get_dataset_name() )
            location_dataset = dataset_pool.get_dataset( VariableName( location_expressions[0] ).get_dataset_name() )
            logger.start_block("Refinement transaction %s:" % this_transaction)
            for action_type in action_order:
                action_function = getattr(self, '_' + action_type)
                for refinement_index in where( logical_and(transactions==this_transaction, actions == action_type))[0]:
                    this_refinement = refinements_this_year.get_data_element(refinement_index)
                    logger.log_status("Action: %s %s agents satisfying %s and %s " % \
                                      (action_type, this_refinement.amount,
                                       this_refinement.agent_expression, 
                                       this_refinement.location_expression
                                   ) )
                    action_function( agents_pool, this_refinement.amount, 
                                     agent_dataset, this_refinement.agent_expression, 
                                     location_dataset, this_refinement.location_expression, 
                                     this_refinement.location_capacity_attribute,
                                     dataset_pool )
                    
            ## delete agents still in agents_pool at the end of the transaction
            agent_dataset.remove_elements( array(agents_pool) )
            logger.end_block()
            
    def _subtract(self, agents_pool, amount,
                  agent_dataset, agent_expression, 
                  location_dataset, location_expression, 
                  location_capacity_attribute,
                  dataset_pool):
        if agent_expression is not None and len(agent_expression) > 0:
            agents_indicator = agent_dataset.compute_variables(agent_expression, 
                                                               dataset_pool=dataset_pool)
        else:
            agents_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        
        if location_expression is not None and len(location_expression) > 0:
            location_indicator = agent_dataset.compute_variables( "%s.disaggregate(%s)"  % 
                                                                 ( agent_dataset.dataset_name, 
                                                                   location_expression ),
                                                                 dataset_pool=dataset_pool)
        else:
            location_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        fit_index = where ( agents_indicator * location_indicator )[0]
        if amount < fit_index.size:
            logger.log_warning("Refinement requests to subtract %s agents,  but there are %s agents in total satisfying %s and %s;" \
                               "subtract %s agents instead" % (fit_index.size, agent_expression, 
                                                               location_expression, amount, 
                                                               fit_index.size) )
            amount = fit_index.size
            
        movers_index = sample_noreplace( fit_index, amount )
        agents_pool += movers_index.tolist()
        ## modify location capacity attribute if specified
        if location_capacity_attribute is not None and len(location_capacity_attribute) > 0:
            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()) )[0]
            num_of_agents_by_location = location_dataset.compute_variables( "%s.number_of_agents(%s)" % \
                                                                            (location_dataset.dataset_name,
                                                                            agent_dataset.dataset_name),
                                                                            dataset_pool=dataset_pool)
            
            shrink_factor = safe_array_divide( (num_of_agents_by_location - num_of_movers_by_location ).astype('float32'),
                                                num_of_agents_by_location, return_value_if_denominator_is_zero = 1.0  )
            location_dataset.modify_attribute( location_capacity_attribute, 
                                               round_( shrink_factor * location_dataset.get_attribute(location_capacity_attribute) )
                                           )
            
        agent_dataset.modify_attribute(location_dataset.get_id_name()[0], 
                                       -1 * ones( movers_index.size, dtype='int32' ),
                                       index = movers_index
                                       )
        
    def _add(self, agents_pool, amount,
             agent_dataset, agent_expression, 
             location_dataset, location_expression, 
             location_capacity_attribute,
             dataset_pool):
        
        if agent_expression is not None and len(agent_expression) > 0:
            agents_indicator = agent_dataset.compute_variables(agent_expression, 
                                                               dataset_pool=dataset_pool)
        else:
            agents_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        if location_expression is not None and len(location_expression) > 0:
            location_indicator = agent_dataset.compute_variables( "%s.disaggregate(%s)"  % 
                                                                 ( agent_dataset.dataset_name, 
                                                                   location_expression ),
                                                                 dataset_pool=dataset_pool
                                                             )
        else:
            location_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        fit_index = where ( agents_indicator * location_indicator )[0]
        movers_index = array([],dtype="int32")
        amount_from_agents_pool = min( amount, len(agents_pool) )
        if amount_from_agents_pool > 0:
            agents_index_from_agents_pool = sample_noreplace( agents_pool, amount_from_agents_pool )
            [ agents_pool.remove(i) for i in agents_index_from_agents_pool ]
            if fit_index.size == 0:
                logger.log_warning("Refinement requests to add %s agents,  but there are only %s agents subtracted from previous action and no agents satisfying %s and %s to clone from;" \
                                   "add %s agents instead" % (amount, amount_from_agents_pool, agent_expression, 
                                                              location_expression, amount_from_agents_pool,) )

                amount = amount_from_agents_pool
                ## cannot find agents to copy their location or clone them
                is_suitable_location = location_dataset.compute_variables( location_expression,
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
            logger.log_error("Action 'add' failed: there is no agent subtracted from previous action, and no suitable agents satisfying %s and %s to clone from." % \
                             (agent_expression, location_expression) )
            return
            
        if amount > amount_from_agents_pool:
            agents_index_to_clone = sample_replace( fit_index, amount - amount_from_agents_pool)
            movers_index = concatenate( (movers_index, agents_index_to_clone) )

        if movers_index.size > 0 and location_capacity_attribute is not None and len(location_capacity_attribute) > 0:
            movers_location_id = agent_dataset.get_attribute( location_dataset.get_id_name()[0] )[movers_index]
            movers_location_index = location_dataset.get_id_index( movers_location_id )
            
            num_of_movers_by_location = histogram( movers_location_index, bins=arange(location_dataset.size()) )[0]
            num_of_agents_by_location = location_dataset.compute_variables( "%s.number_of_agents(%s)" % \
                                                                            ( location_dataset.dataset_name,
                                                                            agent_dataset.dataset_name ),
                                                                            dataset_pool=dataset_pool)
            
            expand_factor = safe_array_divide( (num_of_agents_by_location + num_of_movers_by_location ).astype('float32'),
                                                num_of_agents_by_location, return_value_if_denominator_is_zero = 1.0 )
            location_dataset.modify_attribute( location_capacity_attribute, 
                                               round_( expand_factor * location_dataset.get_attribute(location_capacity_attribute) )
                                           )
        if amount_from_agents_pool > 0:            
            agent_dataset.modify_attribute( location_dataset.get_id_name()[0],
                                            location_id_for_agents_pool,
                                            agents_index_from_agents_pool
                                            )
        if amount > amount_from_agents_pool:
            agent_dataset.duplicate_rows(agents_index_to_clone)
        
    def _modify(self, agents_pool, amount,
                  agent_dataset, agent_expression, 
                  location_dataset, location_expression, 
                  location_capacity_attribute,
                  dataset_pool):
        pass
            
    def _target(self, agents_pool, amount,
                  agent_dataset, agent_expression, 
                  location_dataset, location_expression, 
                  location_capacity_attribute,
                  dataset_pool):
        if agent_expression is not None and len(agent_expression) > 0:
            agents_indicator = agent_dataset.compute_variables(agent_expression, 
                                                               dataset_pool=dataset_pool)
        else:
            agents_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        
        if location_expression is not None and len(location_expression) > 0:
            location_indicator = agent_dataset.compute_variables( "%s.disaggregate(%s)"  % 
                                                                 ( agent_dataset.dataset_name, 
                                                                   location_expression ),
                                                                 dataset_pool=dataset_pool)
        else:
            location_indicator = ones( agent_dataset.size(), dtype='bool' )
        
        fit_index = where ( agents_indicator * location_indicator )[0]
        if fit_index.size > amount:
            self._subtract( agents_pool, fit_index.size - amount,
                            agent_dataset, agent_expression, 
                            location_dataset, location_expression, 
                            location_capacity_attribute,
                            dataset_pool)
        elif fit_index.size < amount:
            self._add( agents_pool, amount - fit_index.size,
                       agent_dataset, agent_expression, 
                       location_dataset, location_expression, 
                       location_capacity_attribute,
                       dataset_pool)

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
        refinement_data = {
            'refinement_id': arange(1, 6),
            'year':          array([2021,2021,2021,2022, 2023]),
            'transaction_id':array([1,      1,   1,   2,    3]),
            'action':        array(['subtract', 'subtract', 'add', 'target', 'add']),
            'amount':        array([2,      1,   4,   7,    1]),
            'agent_expression': array(['job.sector_id==13',
                                       'numpy.logical_and(job.sector_id==13, job.disaggregate(building.raz_id)==4)',
                                       '',
                                       'household.household_id>0',
                                       'household.persons>5'
                                      ]),
            'location_expression': array(['building.raz_id==3',
                                          '',
                                          '(building.raz_id==5) * (building.disaggregate(parcel.generic_land_use_type_id)==4)',
                                          'building.raz_id==6',
                                          'building.raz_id==6'
                                          ]),
            'location_capacity_attribute':array(['',
                                                 'non_residential_sqft',
                                                 'non_residential_sqft',
                                                 'residential_units',
                                                 'residential_units'
                                              ])
        }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'buildings', table_data = building_data)
        storage.write_table(table_name = 'parcels', table_data = parcel_data)
        storage.write_table(table_name = 'households', table_data = household_data)
        storage.write_table(table_name = 'jobs', table_data = job_data)
        storage.write_table(table_name = 'refinements', table_data = refinement_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim', 'opus_core'])
        self.refinement = self.dataset_pool.get_dataset('refinement')
        self.jobs = self.dataset_pool.get_dataset('job')
        self.hhs = self.dataset_pool.get_dataset('household')
        self.buildings = self.dataset_pool.get_dataset('building')
        self.buildings.compute_variables('raz_id=building.disaggregate(parcel.raz_id)', self.dataset_pool)
        
    def test_transaction(self):
        model = RefinementModel()
        model.run(self.refinement, current_year=2021, dataset_pool=self.dataset_pool)
        jobs13_raz3 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(building.raz_id==3))', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz4 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(building.raz_id)==4)', 
                                                  dataset_pool=self.dataset_pool)
        jobs13_raz5 = self.jobs.compute_variables('numpy.logical_and(job.sector_id==13, job.disaggregate(building.raz_id)==5)', 
                                                  dataset_pool=self.dataset_pool)        
        jobs_raz5 = self.jobs.compute_variables('job.disaggregate(building.raz_id)==5', 
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
        hhs_raz6 = self.hhs.compute_variables('household.disaggregate(building.raz_id==6)', 
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
        
if __name__=="__main__":
    opus_unittest.main()    
