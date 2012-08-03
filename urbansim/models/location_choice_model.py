# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from opus_core.resources import Resources
from opus_core.chunk_specification import ChunkSpecification
from numpy import zeros, array, arange, ones, float32, concatenate, where, unique
from numpy import int8, take, put, greater, resize, intersect1d
from opus_core import ndimage
from numpy.random import permutation
from numpy import ma, ndarray
from opus_core.sampler_factory import SamplerFactory
from opus_core.models.choice_model import ChoiceModel
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from opus_core.opus_error import OpusError

class LocationChoiceModel(ChoiceModel):
    """
        LCM is associated with a location_set (Dataset) and a upc_sequence. Method 'run' runs a simulation for a given agent_set,
        where agents choose locations among locations. Locations can be sampled for each agent using given sampling procedure.
        Method 'estimate' runs an estimation process.
        
        Method determine_capacity, get_sampling_weights, and apply_filter should be called in the order from the first to last
    """
    model_name = "Location Choice Model"
    model_short_name = "LCM"

    def __init__(self, location_set, 
                 filter=None, 
                 location_id_string = None,
                 dataset_pool=None, 
                 *args,
                 **kwargs):
        """
        Arguments:
            location_set - Dataset of locations to be chosen from.
            sampler - name of sampling module to be used for sampling locations. If it is None, no sampling is performed
                        and all locations are considered for choice.
            utilities - name of utilities module
            probabilities - name of probabilities module
            choices - name of module for computing agent choices
            filter - filter is applied on location weights for sampling (by multiplication). It is either a string specifying
                        an attribute name of the filter, or a 1D/2D array giving the filter directly,
                        or a dictionary specifying filter for each submodel. If it is None, no filter is applied.
            submodel_string - character string specifying what agent attribute determines submodels.
            location_id_string - character string giving the fully qualified name of the agent attribute
                that specifies the location. Only needed when the attribute is a variable.
                Use it without the "as" clausel, since the code adds an alias which is the id name of the location set.
            run_config - collection of additional arguments that control a simulation run. It is of class Resources.
            estimate_config - collection of additional arguments that control an estimation run. It is of class Resources.
            debuglevel - debuglevel for the constructor. The level is overwritten by the argument in the run and estimate method.

        An instance of upc_sequence class with components utilities, probabilities and choices is created. Also an instance
        of Sampler class for given sampler procedure is created.
        """

        self.dataset_pool = self.create_dataset_pool(dataset_pool, ["urbansim", "opus_core"])
        self.location_id_string = location_id_string
        if self.location_id_string is not None:
            self.location_id_string = VariableName(self.location_id_string)
            #self.location_id_string.set_alias(location_set.get_id_name()[0])

        ChoiceModel.__init__(self, choice_set=location_set, 
                             dataset_pool=self.dataset_pool, 
                             choice_attribute_name=location_id_string,
                             *args, **kwargs)
        
        self.filter = filter

    def run(self, specification, coefficients, agent_set,
            agents_index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        """ Run a simulation and return a numpy array of length agents_index, giving agent choices (ids of locations).
            'specification' is of type EquationSpecification,
            'coefficients' is of type Coefficients,
            'agent_set' is of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which
                        the model runs. If it is None, the whole agent_set is considered.
            'chunk_specification' determines number of chunks in which the simulation is processed.
                        Default is to use 300 rows per chunk.
            'data_objects' is a dictionary where each key is the name of an data object
                    ('zone', ...) and its value is an object of class  Dataset.
            'run_config' is of type Resources, it gives additional arguments for the run.
            'debuglevel' overwrites the constructor 'debuglevel'.
        """
        if run_config == None:
            run_config = Resources()
        self.run_config = run_config.merge_with_defaults(self.run_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        
        ## what is the use of compute location_id string in run? it gets new values anyway
        #if self.location_id_string is not None:
        #    location_id = agent_set.compute_variables(self.location_id_string, dataset_pool=self.dataset_pool)

        ## done in choice_model
        #location_id_name = self.choice_set.get_id_name()[0]
        #if (location_id_name not in agent_set.get_known_attribute_names()):
        #    agent_set.add_attribute(name=location_id_name, data=resize(array([-1]), agent_set.size()))
                    
        if self.run_config.get("agent_units_string", None): # used when agents take different amount of capacity from the total capacity
            agent_set.compute_variables([self.run_config["agent_units_string"]], dataset_pool=self.dataset_pool)

        self.compute_capacity_flag = self.run_config.get("compute_capacity_flag",  False)
        capacity_string = None
        self.capacity = None
        if self.compute_capacity_flag:
            capacity_string = self.run_config.get("capacity_string", None)
            if capacity_string is None:
                raise KeyError, \
                    "Entry 'capacity_string' has to be specified in 'run_config' if 'compute_capacity_flag' is True"
            
        ## if weights is None, use capacity for weights
        if self.run_config.get("weights_for_simulation_string", None) is None and capacity_string is not None:
            self.run_config.merge({"weights_for_simulation_string" : capacity_string})
            
        return ChoiceModel.run(self,specification, coefficients, agent_set,
                agents_index=agents_index, chunk_specification=chunk_specification, run_config=self.run_config,
                debuglevel=debuglevel)

    def run_chunk(self, agents_index, agent_set, specification, coefficients):

        # unplaced agents in agents_index
        location_id_name = self.choice_set.get_id_name()[0]
        agent_set.set_values_of_one_attribute(location_id_name, resize(array([-1]), agents_index.size), 
                                              agents_index)
            
        ## capacity may need to be re-computed for every chunk
        if self.compute_capacity_flag:
            self.capacity = ma.filled(self.determine_capacity(capacity_string=self.run_config.get("capacity_string", None), 
                                                              agent_set=agent_set, 
                                                              agents_index=agents_index), 
                                      0.0)
            if self.capacity is not None:
                logger.log_status("Available capacity: %s units." % self.capacity.sum())
                if self.capacity.sum() <= 0 and self.run_config.get("accept_unavailability_of_choices", False):
                    return array(agents_index.size*[-1], dtype="int32")
                
        self.run_config.merge({"capacity":self.capacity})
        if self.run_config.get("agent_units_string", None):
            self.run_config["agent_units_all"] = agent_set.get_attribute_by_index(self.run_config["agent_units_string"], agents_index)

        choices = ChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)

        ## this is done in choice_model
        #modify locations
        #agent_set.set_values_of_one_attribute(location_id_name, choices, agents_index)
        
        if self.run_config.has_key("capacity"):
            del self.run_config["capacity"]
            
        return choices

    def simulate_chunk(self, *args, **kwargs):
        if self.run_config.get("agent_units_all", None) is not None:
            self.run_config["agent_units"] = self.run_config["agent_units_all"][self.observations_mapping['mapped_index']]
        return ChoiceModel.simulate_chunk(self, *args, **kwargs)

    def compute_demand(self, probabilities):
        """sums probabilities for each alternative and adds it to the demand attribute of the choice set.
        """
        demand = ndimage.sum(probabilities.ravel().astype("float32"), 
                             labels=self.run_config["index"].ravel()+1,
                             index=arange(self.choice_set.size())+1)        
        demand_attr = self.run_config.get("demand_string")
        self.choice_set.modify_attribute(name=demand_attr,
                                         data = self.choice_set.get_attribute(demand_attr) + demand)

    def estimate(self, specification, agent_set, agents_index=None, procedure=None, data_objects=None,
                  estimate_config=None, debuglevel=0):
        """ Computes capacity if required and calls the estimate method of ChoiceModel.
        See ChoiceModel.estimate for details on arguments.
        """
        if agents_index==None:
            agents_index=arange(agent_set.size())
        if agents_index.size <= 0:
            logger.log_status("Nothing to be done.")
            return (None, None)

        logger.log_note('Using dataset pool: %s' % 
                        self.dataset_pool.get_package_order() if self.dataset_pool is not None else self.dataset_pool)

        if estimate_config == None:
            estimate_config = Resources()
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.location_id_string is not None:
            agent_set.compute_variables(self.location_id_string, dataset_pool=self.dataset_pool)
        
        self.capacity = None
        if self.estimate_config.get("compute_capacity_flag", False):
            capacity_string_for_estimation = self.estimate_config.get("capacity_string", None)
            self.capacity = self.determine_capacity(capacity_string=capacity_string_for_estimation, 
                                                              agent_set=agent_set, 
                                                              agents_index=agents_index)

        self.estimate_config.merge({"capacity":self.capacity})
        return ChoiceModel.estimate(self,specification, agent_set,
                                    agents_index, procedure, estimate_config=self.estimate_config, 
                                    debuglevel=debuglevel)

    def determine_capacity(self, capacity_string=None, **kwargs):
        """Return capacity for each location.
        Is there any case where capacity depends on agent_set?
        """
        if capacity_string is None:
            return None
        
        capacity = self.choice_set.compute_variables(capacity_string, dataset_pool=self.dataset_pool)
        return capacity

    def create_interaction_datasets(self, agent_set, agents_index, config, submodels=[], **kwargs):
        """Create interaction dataset with or without sampling of alternatives
        
        arguments to sampler_class is passed through config 
        (run_config or estimation_config in configuration file), such as:
        'include_chosen_choice', 'with_replacement', 'stratum', 
        'sample_size_from_each_stratum', 'sample_size_from_chosen_stratum' 
        (for stratified sampler)
        
        """
        
        nchoices = self.get_choice_set_size()
        ## apply (alternative) filter when alternative size equals to the size of choice set, or sampler class is None
        if (self.sampler_class is None) or (nchoices==self.choice_set.size()):
            if self.filter is None:
                return ChoiceModel.create_interaction_datasets(self, agent_set, agents_index, config)
            else:  # apply filter without doing sampling
                filter_index = self.apply_filter(self.filter, agent_set, agents_index)
                self.model_interaction.create_interaction_datasets(agents_index, filter_index)
                self.update_choice_set_size(filter_index.size)
                return
        
        sampling_weights = self.get_sampling_weights(config, agent_set=agent_set, agents_index=agents_index)
        interaction_dataset = None
        #if filter is specified by submodel in a dict, call sampler submodel by submodel
        sampling_by_groups = False
        if isinstance(self.filter, dict) or config.get("sample_alternatives_by_submodel", False)  or config.get("sample_alternatives_by_group", False):
            groups_equal_submodels=True
            groups = submodels
            sampling_by_groups = True
            if config.get("sample_alternatives_by_group", False):
                group_var = config.get("group_definition_for_sampling_alternatives", None)
                if group_var is None:
                    logger.log_warning('No group variable defined for sampling alternatives. Set "group_definition_for_sampling_alternatives" in run_config/estimate_config.')
                    if isinstance(self.filter, dict):
                        logger.log_warning('Alternatives are sampled by submodel.')
                    else:
                        groups = []
                        sampling_by_groups = False
                else:
                    group_values = agent_set.compute_variables([group_var], dataset_pool=self.dataset_pool)[agents_index]
                    groups = unique(group_values)
                    groups_equal_submodels=False

            index2 = -1 + zeros((agents_index.size, nchoices), dtype="int32")
            attributes = {}
            ###TODO: it may be possible to merge this loop with sample_alternatives_by_chunk or put it in a common function
            for group in groups:
                if groups_equal_submodels:
                    where_group = self.observations_mapping[group]         
                else:
                    where_group = where(group_values == group)[0]
                if where_group.size==0:
                    continue
                agents_index_in_group = agents_index[where_group]

                choice_index = self.apply_filter(self.filter, agent_set=agent_set, 
                                                 agents_index=agents_index_in_group,  
                                                 submodel=group, 
                                                 replace_string='SUBMODEL' if groups_equal_submodels else 'GROUP')
                if choice_index is not None and choice_index.size == 0:
                    logger.log_error("There is no alternative that passes filter %s for %s=%s; %s agents with id %s will remain unplaced." % \
                                     (self.filter, 'SUBMODEL' if groups_equal_submodels else 'GROUP',
                                      group, agents_index_in_group.size, agent_set.get_id_attribute()[agents_index_in_group]))
                    continue
                
                group_sampling_weights = sampling_weights
                if isinstance(sampling_weights, str):
                    group_sampling_weights = re.sub('SUBMODEL' if groups_equal_submodels else 'GROUP', 
                                                       str(int(group)), sampling_weights)
                                      
                chunk_specification = config.get("chunk_specification_for_sampling", {"nchunks":1})
                if type(chunk_specification) == str:
                    chunk_specification = eval(chunk_specification)
                chunk_specification = ChunkSpecification(chunk_specification)
                nchunks = chunk_specification.nchunks(agents_index_in_group)
                chunksize = chunk_specification.chunk_size(agents_index_in_group)
                
                interaction_dataset = self.sample_alternatives_by_chunk(agent_set, agents_index_in_group, 
                                                  choice_index, nchoices,
                                                  weights=group_sampling_weights,
                                                  config=config,
                                                  nchunks=nchunks, chunksize=chunksize)
                if not config.get("accept_unavailability_of_choices", False) and interaction_dataset.get_reduced_m() == 0:
                    raise StandardError, "There are no locations available for the given sampling weights for group %s." % group
                if len(groups)>1 or (agents_index.size > agents_index_in_group.size):
                    if interaction_dataset.get_reduced_m() > 0:
                        index2[where_group,:] = interaction_dataset.index2
                        for name in interaction_dataset.get_known_attribute_names():
                            attr_val = interaction_dataset.get_attribute(name)
                            if not attributes.has_key(name):
                                attributes[name] = zeros(index2.shape, dtype=attr_val.dtype)
                            attributes[name][where_group,:] = attr_val

            if interaction_dataset is None:
                logger.log_warning("There is no agent for groups %s. " % (groups) + \
                                  "This may be due to mismatch between agent_filter and submodels included in specification.")
                self.model_interaction.interaction_dataset = None
                return
            if len(groups)>1 or (agents_index.size > agents_index_in_group.size):  ## if there are more than 1 group, merge the data by submodel and recreate interaction_dataset
                interaction_dataset = self.sampler_class.create_interaction_dataset(interaction_dataset.dataset1, 
                                                                                    interaction_dataset.dataset2, 
                                                                                    index1=agents_index, 
                                                                                    index2=index2)
                for name in attributes.keys():
                    interaction_dataset.add_primary_attribute(attributes[name], name)
                
            self.update_choice_set_size(interaction_dataset.get_reduced_m())
        if not sampling_by_groups: # no sampling by submodels/groups
            choice_index = self.apply_filter(self.filter, agent_set=agent_set, 
                                             agents_index=agents_index)
            if choice_index is not None and choice_index.size == 0:
                logger.log_error("There is no alternative that passes filter %s; %s agents with id %s will remain unplaced." % \
                                 (self.filter, agents_index.size, agent_set.get_id_attribute()[agents_index]))
                return #OR raise?
            
            chunk_specification = config.get("chunk_specification_for_sampling", {"nchunks":1})
            if type(chunk_specification) == str:
                chunk_specification = eval(chunk_specification)
            chunk_specification = ChunkSpecification(chunk_specification)            
            nchunks = chunk_specification.nchunks(agents_index)
            chunksize = chunk_specification.chunk_size(agents_index)
            interaction_dataset = self.sample_alternatives_by_chunk(agent_set, agents_index, 
                                                                    choice_index, nchoices,
                                                                    weights=sampling_weights,
                                                                    config=config,
                                                                    nchunks=nchunks, chunksize=chunksize)
            if not config.get("accept_unavailability_of_choices", False) and interaction_dataset.get_reduced_m() == 0:
                raise StandardError, "There are no locations available for the given sampling weights."
            self.update_choice_set_size(interaction_dataset.get_reduced_m())
            

        self.model_interaction.interaction_dataset = interaction_dataset

    def get_sampling_weights(self, config, **kwargs):
        ## there are cases where filter and weights are mutual dependent (e.g. DPLCM)
        ## pass the filter through self.filter_index to apply_filter, 
        ## which is either boolean array of the same size as self.choice_set or 
        ## index of self.choice_set  
        self.filter_index = None
        return ChoiceModel.get_sampling_weights(self, config, **kwargs)
        
    def apply_filter(self, filter, agent_set=None, agents_index=None, submodel=-2, replace_string='SUBMODEL', **kwargs):
        """Return index to self.choice_set whose value for self.filter variable is true
        
        If filter is a dictionary, it chooses the one for the given submodel.
        
        """
        
        if filter is None:
            filter_index = arange(self.choice_set.size())
            
        if isinstance(filter, dict) and filter.has_key(submodel):
            filter = filter[submodel]

        if isinstance(filter, str):
            submodel_filter = re.sub(replace_string, str(submodel), filter)
            filter_index = where(self.choice_set.compute_variables([submodel_filter], 
                                                                   dataset_pool=self.dataset_pool))[0]
        elif isinstance(filter, ndarray):
            filter_index = where(filter)[0]
        
        if hasattr(self, 'filter_index') and self.filter_index is not None:
            filter_index = intersect1d(self.filter_index, filter_index)
            ##the above WAS
            #choice_indicator = zeros(self.choice_set.size(), dtype='int32')
            #choice_indicator[self.filter_index] += 1
            #choice_indicator[filter_index] += 1
            #filter_index = where(choice_indicator == 2)[0]
                        
        return filter_index

    def plot_choice_histograms(self, capacity=None, main =""):
        if capacity is None:
            capacity = self.run_config.get("capacity_string")
        if isinstance(capacity, str):
            capacity_values = self.choice_set.get_attribute(capacity)
        else:
            capacity_values = capacity
        self.upc_sequence.plot_choice_histograms(capacity=capacity_values, main=main)
        self.upc_sequence.show_plots()

import os
import tempfile
from shutil import rmtree
from opus_core.tests import opus_unittest
from numpy import ma, alltrue
from opus_core.ndimage import sum as ndimage_sum
from opus_core.tests.stochastic_test_case import StochasticTestCase
from opus_core.simulation_state import SimulationState
from opus_core.misc import load_table_from_text_file, unique

## TODO: add unittest for capacity check
class TestChoiceModel(StochasticTestCase):
    def tearDown(self):
        SimulationState().remove_base_cache_directory()

