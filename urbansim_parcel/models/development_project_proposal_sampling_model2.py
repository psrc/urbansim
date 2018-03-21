# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace, probsample_noreplace, probsample_replace
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.variables.variable_name import VariableName
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from numpy import zeros, arange, where, ones, logical_or, logical_and, logical_not, int32, float32, sometrue
from numpy import compress, take, alltrue, argsort, array, int8, bool8, ceil, sort, minimum, concatenate
from gc import collect
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from opus_core.model import Model
from opus_core import ndimage
from opus_core.misc import unique, ismember, intersect1d
from collections import defaultdict

try:
    ## if installed, use PrettyTable module for status logging
    from prettytable import PrettyTable
    import prettytable
except:
    PrettyTable = None
    
class DevelopmentProjectProposalSamplingModel(Model):
    """ this is refactory of development_project_proposal_sampling_model
    It will replace urbansim_parcel.models.development_project_proposal_sampling_model once it stablizes.
    """
    def __init__(self, proposal_set,
                 weight_string = "exp_roi=exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                 filter_attribute=None,
                 run_config=None, 
                 estimate_config=None,
                 debuglevel=0, 
                 dataset_pool=None):
        """
        This model samples project proposals from proposal set weighted by weight_string
        """
        self.proposal_set = proposal_set
        if self.proposal_set.n <= 0:
            ## to be skipped if proposal_set has no data
            return
        
        self.dataset_pool = self.create_dataset_pool(dataset_pool, pool_packages=['urbansim_parcel', 'urbansim', 'opus_core'])
        self.dataset_pool.add_datasets_if_not_included({proposal_set.get_dataset_name(): proposal_set})

        if not self.dataset_pool.has_dataset("development_project_proposal_component"):
            self.proposal_component_set = create_from_proposals_and_template_components(proposal_set, 
                                                       self.dataset_pool.get_dataset('development_template_component'))
            self.dataset_pool.replace_dataset(self.proposal_component_set.get_dataset_name(), self.proposal_component_set)
        else:
            self.proposal_component_set = self.dataset_pool.get_dataset("development_project_proposal_component")

        if weight_string is not None:
            if VariableName(weight_string).get_alias() not in self.proposal_set.get_known_attribute_names():
                self.proposal_set.compute_variables(weight_string, dataset_pool=self.dataset_pool)
            self.weight = self.proposal_set.get_attribute(weight_string).astype("float64")
        else:
            self.weight = ones(self.proposal_set.size(), dtype="float32")  #equal weight

        ## handling of filter_attribute
        if filter_attribute is not None:
            if VariableName(filter_attribute).get_alias() not in self.proposal_set.get_known_attribute_names():
                self.proposal_set.compute_variables(filter_attribute)

            self.weight = self.weight * self.proposal_set.get_attribute(filter_attribute)


    def run(self, n=500, 
            realestate_dataset_name = 'building',
            current_year=None,
            occupied_spaces_variable="occupied_spaces",
            total_spaces_variable="total_spaces",
            run_config=None,
            debuglevel=0):
        """
        run method of the Development Project Proposal Sampling Model
        
        **Parameters**
        
            **n** : int, sample size for each iteration
                   
                   sample n proposals at a time, which are then evaluated one by one until the 
                   target vacancies are satisfied or proposals are running out
                   
            **realestate_dataset_name** : string, name of real estate dataset
            
            **current_year**: int, simulation year. If None, get value from SimulationState
            
            **occupied_spaces_variable** : string, variable name for calculating how much spaces are currently occupied
                                        
                                          It can either be a variable for real_estate dataset that returns 
                                          the amount spaces being occupied or a target_vacancy attribute 
                                          that contains the name of real_estate variables.   
            
            **total_spaces_variable** : string, variable name for calculating total existing spaces
            
        **Returns**
        
            **proposal_set** : indices to proposal_set that are accepted 
            
            **demolished_buildings** : buildings to be demolished for re-development
        """

        self.accepted_proposals = []
        self.demolished_buildings = []  #id of buildings to be demolished
        if self.proposal_set.n <= 0:
            logger.log_status("The size of proposal_set is 0; no proposals to consider, skipping DPPSM.")
            return (self.proposal_set, self.demolished_buildings)

        target_vacancy = self.dataset_pool.get_dataset('target_vacancy')

        if current_year is None:
            year = SimulationState().get_current_time()
        else:
            year = current_year
        this_year_index = where(target_vacancy['year']==year)[0]
        target_vacancy_for_this_year = DatasetSubset(target_vacancy, this_year_index)
        if target_vacancy_for_this_year.size() == 0:
            raise IOError, 'No target vacancy defined for year %s.' % year
        
        ## current_target_vacancy.target_attribute_name = 'target_vacancy_rate'
        ## each column provides a category for which a target vacancy is specified
        self.column_names = list(set( target_vacancy.get_known_attribute_names() ) - \
                            set( [ target_vacancy.target_attribute_name, 
                                   'year', '_hidden_id_',
                                   occupied_spaces_variable, total_spaces_variable
                                   ] )
                            )
        self.column_names.sort(reverse=True)
        
        ## buildings table provides existing stocks
        self.realestate_dataset = self.dataset_pool.get_dataset(realestate_dataset_name)
        
        occupied_spaces_variables = [occupied_spaces_variable]
        total_spaces_variables = [total_spaces_variable]
        if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
            occupied_spaces_variables += unique(target_vacancy_for_this_year[occupied_spaces_variable]).tolist()
        if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
            total_spaces_variables += unique(target_vacancy_for_this_year[total_spaces_variable]).tolist()
            
        self._compute_variables_for_dataset_if_needed(self.realestate_dataset, self.column_names + occupied_spaces_variables + total_spaces_variables)
        self._compute_variables_for_dataset_if_needed(self.proposal_component_set, self.column_names + total_spaces_variables)
        self.proposal_set.compute_variables("urbansim_parcel.development_project_proposal.number_of_components", 
                                            dataset_pool=self.dataset_pool)
        
        n_column = len(self.column_names)
        target_vacancy_for_this_year.column_values = target_vacancy_for_this_year.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        self.realestate_dataset.column_values = self.realestate_dataset.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        self.proposal_component_set.column_values = self.proposal_component_set.get_multiple_attributes(self.column_names).reshape((-1, n_column))
        #defaults, can be changed later by spaces_variable specified in target_vacancy rates
        self.realestate_dataset.total_spaces = self.realestate_dataset[total_spaces_variable]
        self.proposal_component_set.total_spaces = self.proposal_component_set[total_spaces_variable]
        self.realestate_dataset.occupied_spaces = self.realestate_dataset[occupied_spaces_variable]
        
        self.accounting = {}; self.logging = {}
        #has_needed_components = zeros(self.proposal_set.size(), dtype='bool')
        for index in range(target_vacancy_for_this_year.size()):
            column_value = tuple(target_vacancy_for_this_year.column_values[index,:].tolist())
            accounting = {'target_vacancy': target_vacancy_for_this_year[target_vacancy.target_attribute_name][index]}

            realestate_indexes = self.get_index_by_condition(self.realestate_dataset.column_values, column_value)
            component_indexes = self.get_index_by_condition(self.proposal_component_set.column_values, column_value)
            
            this_total_spaces_variable, this_occupied_spaces_variable = total_spaces_variable, occupied_spaces_variable
            ## total/occupied_spaces_variable can be specified either as a universal name for all realestate
            ## or in targe_vacancy_rate dataset for each vacancy category
            if occupied_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_occupied_spaces_variable = target_vacancy_for_this_year[occupied_spaces_variable][index]
                self.realestate_dataset.occupied_spaces[realestate_indexes] = (self.realestate_dataset[this_occupied_spaces_variable][realestate_indexes]
                                                                               ).astype(self.realestate_dataset.occupied_spaces.dtype)
    
            if total_spaces_variable in target_vacancy_for_this_year.get_known_attribute_names():
                this_total_spaces_variable = target_vacancy_for_this_year[total_spaces_variable][index]    
                self.realestate_dataset.total_spaces[realestate_indexes] = (self.realestate_dataset[this_total_spaces_variable][realestate_indexes]
                                                                            ).astype(self.realestate_dataset.total_spaces.dtype)
                self.proposal_component_set.total_spaces[component_indexes] = (self.proposal_component_set[this_total_spaces_variable][component_indexes]
                                                                               ).astype(self.proposal_component_set.total_spaces.dtype)
                
            accounting["total_spaces_variable"] = this_total_spaces_variable
            accounting["total_spaces"] = self.realestate_dataset.total_spaces[realestate_indexes].sum()
            accounting["occupied_spaces_variable"] = this_occupied_spaces_variable
            accounting["occupied_spaces"] = self.realestate_dataset.occupied_spaces[realestate_indexes].sum()
            accounting["target_spaces"] = int( round( accounting["occupied_spaces"] /\
                                                     (1 - accounting["target_vacancy"])
                                               ) )
            accounting["proposed_spaces"] = 0
            accounting["demolished_spaces"] = 0
            
            self.accounting[column_value] = accounting
            
            if self._is_target_reached(column_value):
                proposal_indexes = self.proposal_set.get_id_index( unique(self.proposal_component_set['proposal_id'][component_indexes]) )
                single_component_indexes = where(self.proposal_set["number_of_components"]==1)[0]
                self.weight[intersect1d(proposal_indexes, single_component_indexes)] = 0.0
                
        ## handle planned proposals: all proposals with status_id == is_planned 
        ## and start_year == year are accepted
        planned_proposal_indexes = where(logical_and(
                                                  self.proposal_set.get_attribute("status_id") == self.proposal_set.id_planned, 
                                                  self.proposal_set.get_attribute("start_year") == year ) 
                                        )[0]
        logger.start_block("Processing %s planned proposals" % planned_proposal_indexes.size)
        self.consider_proposals(planned_proposal_indexes, force_accepting=True)
        logger.end_block()
        # consider proposals (in this order: proposed, tentative)
        for status in [self.proposal_set.id_proposed, self.proposal_set.id_tentative]:
            stat = (self.proposal_set.get_attribute("status_id") == status)
            if stat.sum() == 0:
                continue
            
            logger.log_status("Sampling from %s eligible proposals of status %s." % (stat.sum(), status))
            #iteration = 0
            while (not self._is_target_reached()):
                ## prevent proposals from being sampled for vacancy type whose target is reached
                #for column_value in self.accounting.keys():
                
                if self.weight[stat].sum() == 0.0:
                    logger.log_warning("Running out of proposals of status %s before vacancy targets are reached; there aren't any proposals with non-zero weight" % status)
                    break
                
                available_indexes = where(logical_and(stat, self.weight > 0))[0]
                sample_size = minimum(available_indexes.size, n)
                sampled_proposal_indexes = probsample_noreplace(available_indexes, sample_size, 
                                                                prob_array=self.weight[available_indexes],
                                                                return_index=False)
                self.consider_proposals(sampled_proposal_indexes)
                self.weight[sampled_proposal_indexes] = 0
                #iteration += 1
        
        self._log_status()
        
        # set status of accepted proposals to 'active'
        self.proposal_set.modify_attribute(name="status_id", 
                                           data=self.proposal_set.id_active,
                                           index=array(self.accepted_proposals, dtype='int32'))
        
        # Code added by Jesse Ayers, MAG, 7/20/2009
        # Get the active projects:
        stat_id = self.proposal_set.get_attribute('status_id')
        actv = where(stat_id==1)[0]
        # Where there are active projects, compute the total_land_area_taken
        # and store it on the development_project_proposals dataset
        # so it can be used by the building_construction_model for the proper
        # computation of units_proposed for those projects with velocity curves
        if actv.size > 0:          
            total_land_area_taken_computed = self.proposal_set.get_attribute('urbansim_parcel.development_project_proposal.land_area_taken')
            self.proposal_set.modify_attribute('total_land_area_taken', total_land_area_taken_computed[actv], actv)

        return (self.proposal_set, self.realestate_dataset.get_id_attribute()[self.demolished_buildings])

    def _log_status(self):
        logging_header = ["Target", "Current", "Difference(T-C)", "Proposed", "Demolished", "Action(P-D)"]
        logging_fields = ["target_spaces", "total_spaces", "difference", "proposed_spaces", "demolished_spaces", "action"]
        ## additional available logging fields are: target_vacancy, occupied_spaces, current_vacancy, future_vancancy
        
        if PrettyTable is not None:
            status_log = PrettyTable()
            if prettytable.__version__ >= 0.6: # compatibility issue
                status_log.field_names = self.column_names + logging_header
                for header in logging_header:
                    status_log.align[header] = 'r' 
            else:
                status_log.set_field_names(self.column_names + logging_header)
                [status_log.set_field_align(header, 'r') for header in logging_header]
        else:
            logger.log_status("\t".join(self.column_names + logging_header))
#        error_log = ''
        
        keys = self.accounting.keys(); keys.sort()
        for key in keys:
            value = self.accounting[key]
            value["current_vacancy"] = (value.get("total_spaces",0) - value.get("occupied_spaces",0))/float(value.get("total_spaces",0))           
            value["difference"] = value.get("target_spaces",0)-value.get("total_spaces",0)            
            value["action"] = (value.get("proposed_spaces",0)-value.get("demolished_spaces",0))
            value["future_vacancy"] = (value.get("total_spaces",0) + value["action"] - value.get("occupied_spaces",0)) /\
                 float(value.get("total_spaces",0)+value["action"])
            if value["action"]>0: value["action"] = "+" + str(value["action"])
            
            logging_values = [value.get(field,'') for field in logging_fields]
            row = [str(item) for item in list(key) + logging_values]
            if PrettyTable is not None:
                status_log.add_row(row)
            else:
                logger.log_status("\t".join(row))
                
        #logging for keys not appearing in target_vacancies
        keys = self.logging.keys(); keys.sort()
        for key in keys: 
            value = self.logging[key]
            value["difference"] = ( value.get("target_spaces",0)-value.get("total_spaces",0) ) or ''
            value["action"] = (value.get("proposed_spaces",0)-value.get("demolished_spaces",0))
            if value["action"]>0: value["action"] = "+" + str(value["action"])
            
            logging_values = [value.get(field,'') for field in logging_fields]
            if not any(logging_values): continue

            #action_num = (value.get("proposed_spaces",0)-value.get("demolished_spaces",0)) or ''
            #else: action = str(action_num)
            row = [str(item) for item in list(key) + logging_values]
            if PrettyTable is not None:
                status_log.add_row(row)
            else:
                logger.log_status("\t".join(row))
        
        if PrettyTable is not None:
            logger.log_status("\n" + status_log.get_string())

    def _compute_variables_for_dataset_if_needed(self, dataset, variable_names):
        known_attributes = dataset.get_known_attribute_names()
        dataset_pool = SessionConfiguration().get_dataset_pool()
        for variable in variable_names:
            alias = VariableName(variable).get_alias()
            if variable not in known_attributes and alias not in known_attributes:
                dataset.compute_one_variable_with_unknown_package(variable, dataset_pool=dataset_pool)

    def get_index_by_condition(self, array, condition):
        from numpy import alltrue
        #assert array.ndim == 2
        #assert array.shape[1] == len(condition)
        result = array == condition
        if result.ndim > 1:
            result = alltrue(result, axis=-1)
        return result
    
    def consider_proposals(self, proposal_indexes, force_accepting=False):
        is_proposal_rejected = zeros(proposal_indexes.size, dtype="bool")
        sites = self.proposal_set["parcel_id"][proposal_indexes]
        for i, proposal_index in enumerate(proposal_indexes):
            if not is_proposal_rejected[i] and ((self.weight[proposal_index] > 0) or force_accepting):
                accepted = self.consider_proposal(proposal_index, force_accepting=force_accepting)
                if accepted:
                    is_proposal_rejected[ sites == sites[i]] = True
        
    def consider_proposal(self, proposal_index, force_accepting=False):
        this_site = self.proposal_set["parcel_id"][proposal_index]            
        building_indexes = array([], dtype='i')
        demolished_spaces = defaultdict(int)
        if self.proposal_set["is_redevelopment"][proposal_index] or force_accepting:  #redevelopment proposal
            building_indexes = where(self.realestate_dataset['parcel_id']==this_site)[0]
            for building_index in building_indexes:
                column_value = tuple(self.realestate_dataset.column_values[building_index,:].tolist())
                demolished_spaces[column_value] += self.realestate_dataset.total_spaces[building_index]

        component_indexes = where(self.proposal_component_set['proposal_id']==self.proposal_set['proposal_id'][proposal_index])[0]
        proposed_spaces = defaultdict(int) 
        #[(self.proposal_component_set.column_values[component_index,:], self.proposal_component_set.total_spaces[component_indexes])]            
        for component_index in component_indexes:
            column_value = tuple(self.proposal_component_set.column_values[component_index,:].tolist())
            proposed_spaces[column_value] += self.proposal_component_set.total_spaces[component_index]
        
        ## skip this proposal if the proposal has no components that are needed to reach vacancy target
        if not force_accepting and all([ self._is_target_reached(key) 
                 or (proposed_spaces.get(key,0) - demolished_spaces.get(key,0) <= 0)  ## 
                 for key in proposed_spaces.keys() ]):
            return False
        
        # accept this proposal
        for key, value in demolished_spaces.items():
            if key not in self.accounting:
                if key not in self.logging:
                    self.logging[key] = defaultdict(int)
                self.logging[key]["demolished_spaces"] += value
            else:
                self.accounting[key]["demolished_spaces"] += value 
                ##TODO we may want to re-activate sampling of proposals if new total spaces is below target spaces 
                ##because of demolished buildings 
        
        for key, value in proposed_spaces.items():
            if key not in self.accounting:
                if key not in self.logging:
                    self.logging[key] = defaultdict(int)
                self.logging[key]["proposed_spaces"] += value
            else:
                self.accounting[key]["proposed_spaces"] += value
                self.eliminate_proposals_if_target_reached(key)
                                     
        if building_indexes.size > 0: self.demolished_buildings.extend(building_indexes.tolist())
        self.accepted_proposals.append(proposal_index)
        
        # don't consider proposals for this site in future sampling
        self.weight[proposal_index] = 0.0
        self.weight[self.proposal_set["parcel_id"] == this_site] = 0.0
        return True
    
    def eliminate_proposals_if_target_reached(self, key):
        if self._is_target_reached(key):  ## disable proposals from sampling
            component_indexes = self.get_index_by_condition(self.proposal_component_set.column_values, key)
            proposal_indexes = self.proposal_set.get_id_index( unique(self.proposal_component_set['proposal_id'][component_indexes]) )
            self.weight[proposal_indexes] = 0.0
        return
        
    def _is_target_reached(self, column_value=()):
        if column_value:
            if self.accounting.has_key(column_value):
                accounting = self.accounting[column_value]
                result = accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                                accounting.get("demolished_spaces",0) )
                return result
            else:
                return True
        results = [  accounting.get("target_spaces",0) <= ( accounting.get("total_spaces",0) + accounting.get("proposed_spaces",0) - 
                                                            accounting.get("demolished_spaces",0) ) 
                   for column_value, accounting in self.accounting.items() ]
        return all(results)

## TODO: enable unittests     
#from opus_core.tests import opus_unittest
#from opus_core.storage_factory import StorageFactory
#from opus_core.datasets.dataset_pool import DatasetPool
#from numpy import arange, array, all, exp
#from opus_core.datasets.dataset import Dataset
#
#class DevelopmentProjectProposalSamplingModelTest(opus_unittest.OpusTestCase):
#    def Mtest_vacancy_rates_calculation(self):
#
#        proposal_data = {
#            'proposal_id': array([1]),
#            }
#        proposal_component_data = {
#            'component_id':array([1]),
#            }
#        storage = StorageFactory().get_storage('dict_storage')
#        storage.write_table(table_name = 'development_project_proposals', table_data = proposal_data)
#        storage.write_table(table_name = 'development_project_proposal_components', table_data = proposal_component_data)
#        dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim'])
#                       
#        proposal_dataset = dataset_pool.get_dataset('development_project_proposal')
#        proposal_component_dataset = dataset_pool.get_dataset('development_project_proposal_component')
# 
#        DPPSM = DevelopmentProjectProposalSamplingModel(proposal_dataset, dataset_pool=dataset_pool, weight_string=None)
#        DPPSM.existing_units =   {1:200, 2:200, 3:200, 4:200, 5:200, 6:200}
#        DPPSM.demolished_units = {1:100, 2:100, 3:100, 4:50,  5:0,   6:20}
#        DPPSM.proposed_units =   {1:50,  2:150, 3:80,  4:100, 5:160, 6:0}
#        DPPSM.occupied_units =   {1:180, 2:180, 3:180, 4:180, 5:180, 6:180}
#        
#        expected = {1:0.0, 2:0.28, 3:0.0, 4:0.28, 5:0.5, 6:0.0}
#        actual = {}
#        for type in DPPSM.existing_units.keys():
#            actual[type] = DPPSM._get_vacancy_rates(type)
#
#        self.assertDictsEqual(actual, expected)
#    def test_my_inputs(self):
#
#        test_data={
#        'target_vacancy':
#        {
#            "year":                 array([2000, 2000, 2000,  2000,  2000,  2000, 2001, 2001, 2001]),
#            "geography_id":         array([1,       2,   3,     1,     2,     3,    3,    3,   -1]),
#            "is_residential":       array([0,       0,    0,     1,     1,     1,    0,    1,   -1]),
#            "target_vacancy_rate":  array([0.5,  0.75, 0.25,   0.4,   0.6,   0.2,  0.3,  0.33, 0.13])
#        },
#        'development_template_component':
#        {
#            'component_id': array([1, 2, 3, 4, 5, 6]),
#            'template_id':  array([1, 2, 2, 3, 3, 4]),
#            'percent_building_sqft':      array([100,  80,   20,   50, 50, 100]),
#            'building_sqft_per_unit':     array([4000, 400,  1,    1,  1,  1000]),
#            ## construction_cost_per_unit is actually construction_cost_per_sqft
#            #'construction_cost_per_unit': array([50,   20,  20,  80, 100, 100]),
#            'building_type_id':            array([19,   4,    3,    13, 3,   19]),
#            #'is_residential':             array([1,    1,    0,    0,  0,   1]),
#        },
#        'building_type':
#        {  
#            'building_type_id':              array([19,   4,    3,    13]),
#            'is_residential':                array([1,    1,    0,    0 ]),
#         },
#        'building':
#        {  
#            "building_id":       array([1, 2,  3,  4,  5,  6,  7,  8,  9,  10]),
#            "parcel_id":         array([1, 1,  2,  2,  3,  3,  4,  6,  6,  6]),
#
#            "geography_id":      array([1, 1,  1,  1,  2,  2,  2,  3,  3,  3]),
#            "building_type_id":  array([3, 4,  19, 13, 3,  19, 4,  4,  13, 3]),
#          #"is_residential":     array([0, 1,  1,  0,  0,  1,  1,  1,  0,  0]),
#            "units_existing":    array([7, 2,  3,  4,  1,  1,  5,  8,  6,  9]),
#            "units_occupied":    array([7, 1,  3,  4,  0,  1,  4,  2,  6,  6]),
#        },
#
#        'development_project_proposal':
#        {  
#            "proposal_id":array([1,  2,  3,  4, 5,  6, 7, 8, 9, 10, 11]),
#            "start_year": array([1,  1,  1,  1, 1,  1, 1, 1, 1, 1, 1]) * 2000,
#            "status_id":  array([4,  4,  4,  4, 4,  4, 4, 4, 4, 4, 4]),  #tentative
#            "parcel_id":  array([1,  1,  2,  2, 3,  3, 4, 5, 5, 6, 6]),
#         "geography_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3]),
#            "template_id":array([1,  2,  3,  4, 2,  3, 4, 1, 2, 3, 4]),
#            #"unit_price_expected":array([560000/2000.0, 400000/1500.0, 400000/2000.0, 200000/3000.0, 330000/1000.0, 420000/4000.0,
#                                            #480000/5000.0, 1400000/3050.0, 4600000/8000.0, 200000000/1000000.0, 1000000/3500.0]),
#            #"units_proposed":array([1, 1500, 2000, 8, 1000, 4000, 3, 2, 8000, 1000000, 4]),
#            #"building_sqft": array([2000, 1500, 2000, 3000, 1000, 4000, 5000, 3050, 8000, 1000000, 3500]),
#            "is_redevelopment":array([0,  0,  1,  1, 0,  1, 1, 0, 1, 1,  1]),
#            #"land_area_taken": array([10000, 20000, 10000, 20000,
#                                      #22680, 45360, 15120,
#                                      #45000, 45000, 90000, 9000,
#                                      #]),
#            "exp_roi": exp(array([-0.2       , -0.61165049, -0.43262411, -0.89041096,  0.69230769,
#                              -0.53203343, -0.20551724,  2.33333333, -0.69816273,  0.90294957,
#                              -0.93533368])),
#        },
#        'development_project_proposal_component':
#        {
#            "proposal_component_id":array([1,  2, 3,  4, 5,  6,  7,  8,  9,10,11,12, 13,14,15, 16,  17]),
#            "proposal_id":          array([1,  2, 2,  3, 3,  4,  5,  5,  6, 6, 7, 8,  9, 9, 10, 10, 11]),
#            "component_id":         array([1,  2, 3,  4, 5,  6,  2,  3,  4, 5, 6, 1,  2, 3, 4,  5,  6]),
#        ##  "is_residential":       array([1,  1, 0,  0, 0,  1,  1,  0,  0, 0, 1, 1,  1, 0, 0,  0,  1]),
#            "geography_id":         array([1,  1, 1,  1, 1,  1,  2,  2,  2, 2, 2, 3,  3, 3, 3,  3,  3]),
#            "template_id":          array([1,  2, 2,  3, 3,  4,  2,  2,  3, 3, 4, 1,  2, 2, 3,  3,  4]),
#"number_of_nhb_job_spaces_proposed":array([0,  0,16, 18, 15, 0,  0,  2,  3, 3, 0, 0,  0, 2, 3,  3,  0]),
#"residential_units_proposed":       array([5,  3, 0,  0, 0,  1,  6,  0,  0, 0, 8, 1,  2, 0, 0,  0,  4]),             
#        }
#
#        }
#
#        storage = StorageFactory().get_storage('dict_storage')
#        for key, value in test_data.iteritems():
#            storage.write_table(table_name = '%ss' % key, table_data = value)
#        storage.write_table(table_name = 'target_vacancies', table_data = test_data['target_vacancy'])
#
#        dataset_pool = SessionConfiguration(in_storage=storage, package_order = ['urbansim_parcel', 'urbansim']).get_dataset_pool()
#
#        proposal_dataset = dataset_pool.get_dataset('development_project_proposal')
#        proposal_component_dataset = dataset_pool.get_dataset('development_project_proposal_component')
#
#        DPPSM = DevelopmentProjectProposalSamplingModel(proposal_dataset, dataset_pool=dataset_pool, weight_string='exp_roi')
#        DPPSM.run(current_year=2000)
#
#        self.assert_(all(DPPSM.target_vacancy_rate<=DPPSM._get_vacancy_rates()))
#        
#if __name__=="__main__":
#    opus_unittest.main()
