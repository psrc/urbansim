# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import gc
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.coefficients import create_coefficient_from_specification, Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from opus_core.upc_factory import UPCFactory
from opus_core.sampler_factory import SamplerFactory
from opus_core.model_component_creator import ModelComponentCreator
from opus_core.misc import DebugPrinter, unique
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.models.chunk_model import ChunkModel
from opus_core.chunk_specification import ChunkSpecification
from opus_core.class_factory import ClassFactory
from opus_core.model import get_specification_for_estimation, prepare_specification_and_coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from numpy import where, zeros, array, arange, ones, take, ndarray, resize, concatenate, alltrue
from numpy import int32, compress, float64, isnan, isinf, newaxis, row_stack
from numpy.random import permutation
from opus_core.variables.attribute_type import AttributeType

class ChoiceModel(ChunkModel):
    """
        Implements a discrete choice model, where agents choose from given choices.
        Method 'run' runs a simulation for a given agent_set.
        Method 'estimate' runs an estimation process. The specific algorithm is implemented in the given upc_sequence.
    """

    model_name = "Choice Model"
    model_short_name ="ChoiceM"

    def __init__(self, choice_set, utilities="opus_core.linear_utilities",
                        probabilities="opus_core.mnl_probabilities",
                        choices="opus_core.random_choices",
                        sampler=None, sampler_size=None,
                        submodel_string=None,
                        choice_attribute_name="choice_id",
                        interaction_pkg="opus_core",
                        run_config=None, estimate_config=None, debuglevel=0,
                        dataset_pool=None):
        """
        Arguments:
            choice_set - Dataset or array/list of choices.
            utilities - name of utilities module
            probabilities - name of probabilities module
            choices - name of module for computing agent choices
            sampler - name of sampling module to be used for sampling alternatives. If it is None, no sampling is performed
                        and all alternatives are considered for choice.
            submodel_string - character string specifying what agent attribute determines submodels.
            choice_attribute_name - name of the attribute that identifies the choices. This argument is
                only relevant if choice_set is not an instance of Dataset.
                Otherwise the choices are identified by the unique identifier of choice_set.
            interaction_pkg - only relevant if there is an implementation of an interaction dataset
                that corresponds to interaction between agents and choices.
            run_config - collection of additional arguments that control a simulation run. It is of class Resources.
            estimate_config - collection of additional arguments that control an estimation run. It is of class Resources.
            debuglevel - debuglevel for the constructor. The level is overwritten by the argument in the run and estimate method.

        An instance of upc_sequence class with components utilities, probabilities and choices is created. Also an instance
        of Sampler class for given sampler procedure is created.
        """
        self.debug = DebugPrinter(debuglevel)

        self.compute_choice_attribute = False
        self.choice_attribute_name = choice_attribute_name
        if (self.choice_attribute_name is not None):
            self.choice_attribute_name = VariableName(self.choice_attribute_name)
            if self.choice_attribute_name.get_dataset_name() is not None:
                self.compute_choice_attribute = True
                
        if not isinstance(choice_set, Dataset):
            storage = StorageFactory().get_storage('dict_storage')
            storage_table_name = 'choice_set'
            table_data = {self.choice_attribute_name.get_alias():array(choice_set)}
            storage.write_table(
                table_name=storage_table_name,
                table_data=table_data
                )
                                
            choice_set = Dataset(
                in_storage = storage,
                in_table_name = storage_table_name,
                id_name = self.choice_attribute_name.get_alias(),
                dataset_name = 'choice',
                )

        self.choice_set = choice_set
        self.upc_sequence = UPCFactory().get_model(
            utilities=utilities, probabilities=probabilities, choices=choices, debuglevel=debuglevel)
            
        self.sampler_class = SamplerFactory().get_sampler(sampler)
        if (sampler <> None) and (self.sampler_class == None):
            logger.log_warning("Error in loading sampler class. No sampling will be performed.")
        self.sampler_size=sampler_size
        
        self.submodel_string = submodel_string # which attribute determines submodels
        self.run_config = run_config
        if self.run_config == None:
            self.run_config = Resources()
        self.estimate_config = estimate_config
        if self.estimate_config == None:
            self.estimate_config = Resources()
        self.result_choices = None
        self.dataset_pool = self.create_dataset_pool(dataset_pool)
        self.dataset_pool.replace_dataset(self.choice_set.get_dataset_name(), self.choice_set)
        self.coefficient_names = {}
        self.model_interaction = ModelInteraction(self, interaction_pkg, self.choice_set)
        ChunkModel.__init__(self)
        self.get_status_for_gui().initialize_pieces(3, pieces_description = array(['initialization', 'computing variables', 'submodel: 1']))

    def run(self, specification, coefficients, agent_set,
            agents_index=None, chunk_specification=None, data_objects=None, run_config=None, debuglevel=0):
        """ Run a simulation and return a numpy array of length agents_index, giving agent choices (ids of locations).
            'specification' is of type EquationSpecification,
            'coefficients' is of type Coefficients,
            'agent_set' is of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which
                        the model runs. If it is None, the whole agent_set is considered.
            'chunk_specification' - specifies how to determine the number of chunks to use
                        when computing.
            'data_objects' is a dictionary where each key is the name of an data object
                    ('zone', ...) and its value is an object of class  Dataset.
            'run_config' is of type Resources, it gives additional arguments for the run.
            'debuglevel' overwrites the constructor 'debuglevel'.
        """
        self.debug.flag = debuglevel
        if run_config == None:
            run_config = Resources()
        ## plug in default switches: 
        ## whether to include_chosen_choice for sampler, 
        ## whether it is called in estimate method 
        run_config.merge_with_defaults({"include_chosen_choice":False, "estimate":False})
        self.run_config = run_config.merge_with_defaults(self.run_config)

        self.dataset_pool.replace_dataset(agent_set.get_dataset_name(), agent_set)
        if agents_index==None:
            agents_index=arange(agent_set.size())

        ## compute_variables is not meaningful given it's going to be overwritten by run()
        ## (HS) but we need it in cases when doesn't exist and is added as primary attribute,
        ## e.g. cars_category in auto-ownership model. 
        if self.compute_choice_attribute:
            agent_set.compute_variables([self.choice_attribute_name], dataset_pool=self.dataset_pool)
        
        ## add a primary attribute for choice_id_name or convert it to primary attribute
        choice_id_name = self.choice_set.get_id_name()[0]
        if (choice_id_name not in agent_set.get_known_attribute_names()):
            agent_set.add_primary_attribute(name=choice_id_name, 
                                    data=resize(array([-1]), agent_set.size()))
        else:
            if choice_id_name in agent_set.get_nonloaded_attribute_names():
                agent_set.get_attribute(choice_id_name)
            if agent_set._get_attribute_type(choice_id_name) == AttributeType.COMPUTED:
                agent_set.attribute_boxes[choice_id_name].set_type(AttributeType.PRIMARY)
                agent_set._add_to_primary_attribute_names(choice_id_name)
            
        if self.run_config.get("demand_string", None):
            self.choice_set.add_primary_attribute(name=self.run_config.get("demand_string"),
                                          data=zeros(self.choice_set.size(), dtype="float32"))
            self.compute_demand_flag = True
        else:
            self.compute_demand_flag = False

        ## calculate cumulative supply that is compatible with demand calculation
        if self.run_config.get("supply_string", None):
            current_choice = agent_set.get_attribute(choice_id_name)
            agent_set.modify_attribute(choice_id_name, zeros(agents_index.size)-1, index=agents_index)
            supply_varaible_name = VariableName(self.run_config.get("supply_string"))
            supply_alias = supply_varaible_name.get_alias()
            if supply_alias in self.choice_set.get_primary_attribute_names():
                self.choice_set.delete_one_attribute(supply_alias)
            supply = self.choice_set.compute_variables(supply_varaible_name, dataset_pool=self.dataset_pool)
            self.choice_set.add_primary_attribute(name=supply_alias, data=supply)
            agent_set.modify_attribute(choice_id_name, current_choice)

        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.model_interaction.set_agent_set(agent_set)
        
        self.result_choices = ChunkModel.run(self, chunk_specification, agent_set, agents_index, int32,
                                 specification=specification, coefficients=coefficients)
        return self.result_choices

    def run_chunk(self, agents_index, agent_set, specification, coefficients):

        if agents_index.size <= 0:
            return array([], dtype='int32')

        self.set_choice_set_size()
        nchoices = self.get_choice_set_size()
        
        ## initial specified_coefficients with dummy values as we may need to get submodel information from it
        ## recreated specified_coefficients when the sampling is done and choice_ids is known
        #self.model_interaction.create_specified_coefficients(coefficients, specification, choice_ids=arange(nchoices)+1)
        submodels = specification.get_distinct_submodels()
        self.map_agents_to_submodels(submodels, self.submodel_string, agent_set, agents_index,
                                      dataset_pool=self.dataset_pool, resources = Resources({"debug": self.debug}))
        
        self.create_interaction_datasets(agent_set, agents_index, self.run_config, submodels=submodels)
        ## move Choice set size log after compute_variables so it is not buried in compute_variable msg
        #logger.log_status("Choice set size: %i" % self.get_choice_set_size())
        index = self.model_interaction.get_choice_index()
        if index.size <=0:
            logger.log_warning("No choices available.")
            return array(agents_index.size*[-1], dtype="int32")
        self.debug.print_debug("Create specified coefficients ...",4)
        self.model_interaction.create_specified_coefficients(coefficients, specification, self.choice_set.get_id_attribute()[index])
        self.run_config.merge({"index":index})

        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        
        # simulate
        choice_indices = self.simulate_chunk()
        choice_set_ids = self.choice_set.get_id_attribute()
        choices = where(choice_indices < 0, -1, choice_set_ids[choice_indices])

        #modify choices
        agent_set.set_values_of_one_attribute(self.choice_set.get_id_name()[0], choices, agents_index)

        del self.run_config["index"]
        return choices

    def simulate_chunk(self):
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        self.model_interaction.compute_variables()
        
        logger.log_status("Choice set size: %i" % self.get_choice_set_size())
        
        coef = {}
        result = resize(array([-1], dtype="int32"), self.observations_mapping["index"].size)
        index = self.run_config["index"]
        self.debug.print_debug("Simulate ...",4)
        for submodel in self.model_interaction.get_submodels():
            self.model_interaction.prepare_data_for_simulation(submodel)
            coef[submodel] = self.model_interaction.get_submodel_coefficients(submodel)
            self.coefficient_names[submodel] = self.model_interaction.get_variable_names_for_simulation(submodel)
            self.debug.print_debug("   submodel: %s   nobs: %s" % (submodel, self.observations_mapping[submodel].size), 5)
            self.increment_current_status_piece()
            if self.model_interaction.is_there_data(submodel): # observations for this submodel available
                if index is not None:
                    self.run_config["index"] = take (index, indices=self.observations_mapping[submodel], axis=0)
                self.run_config.merge({"specified_coefficients": coef[submodel]})
                coefficients = coef[submodel].get_coefficient_values()
                data = self.get_all_data(submodel)
                nan_index = where(isnan(data))[2]
                inf_index = where(isinf(data))[2]
                if nan_index.size > 0:
                    nan_var_index = unique(nan_index)
                    raise ValueError, "NaN(Not a Number) is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % coef[submodel].get_variable_names()[nan_var_index]
                if inf_index.size > 0:
                    inf_var_index = unique(inf_index)
                    raise ValueError, "Inf is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % coef[submodel].get_variable_names()[inf_var_index]

                res = self.simulate_submodel(data, coefficients, submodel)
                restmp = res.astype(int32)
                res_positive_idx = where(res>=0)[0]
                if index is not None:
                    if index.shape[1] <> coef[submodel].nequations():
                        restmp[res_positive_idx] = array(map(lambda x:
                            index[x,coef[submodel].get_equations_index()[res[x]]], res_positive_idx)).astype(int32)
                else:
                    restmp[res_positive_idx] = coef[submodel].get_equations_index()[res[res_positive_idx]].astype(int32)
                result[self.observations_mapping[submodel]] = restmp
        return result

    def simulate_submodel(self, data, coefficients, submodel=0):
        result = self.upc_sequence.run(data, coefficients, resources=self.run_config)
        if self.compute_demand_flag:
            self.compute_demand(submodel)
        if self.run_config.get("export_simulation_data", False):
            self.export_probabilities(submodel, 
                                        self.run_config.get("simulation_data_file_name", './choice_model_data.txt'))
        return result

    def compute_demand(self, submodel=0):
        """sums probabilities for each alternative and adds it to the demand attribute of the choice set.
        """
        demand = self.get_demand_for_submodel(submodel)
        demand_attr = self.run_config.get("demand_string")
        self.choice_set.modify_attribute(name=demand_attr,
                                         data = self.choice_set.get_attribute(demand_attr) + demand)

    def get_demand_for_submodel(self, submodel=0):
        probs = self.upc_sequence.get_probabilities()
        return probs.sum(axis=0) # sums probabilities for each alternative


    def estimate(self, specification, agent_set, agents_index=None, procedure=None, data_objects=None,
                  estimate_config=None, debuglevel=0):
        """ Run an estimation process and return a tuple where the first element is an object of class Coefficients
            containing the estimated coefficients, and the second element is a dictionary with an entry for each submodel
            giving the return values of the specified estimation procedure.
            'specification' is of type EquationSpecification,
            'agent_set' is of type Dataset,
            'agent_index' are indices of individuals in the agent_set for which
                        the model is estimated. If it is None, the whole agent_set is considered.
            'procedure' is a string giving the name of the estimation procedure. If it is None,
                there should be an entry "estimation" in 'estimate_config' that determines the procedure. The class
                must have a method 'run' that takes as arguments 'data', 'upc_sequence' and 'resources'. It returns a dictionary
                with entries 'estimators', 'standard_errors' and 't_values' (all 1D numpy arrays).
            'data_objects' is a dictionary where each key is the name of an data object
                    ('zone', ...) and its value is an object of class  Dataset.
            'estimate_config' is of type Resources, it gives additional arguments for the estimation procedure.
            'debuglevel' overwrites the class 'debuglevel'.
        """
        self.debug.flag = debuglevel
        if estimate_config == None:
            estimate_config = Resources()
            
        ## plug in default switches: 
        ## whether to include_chosen_choice for sampler, 
        ## whether it is called in estimate method 
        estimate_config.merge_with_defaults({"include_chosen_choice":True, "estimate":True})
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)

        self.procedure=procedure
        if self.procedure == None:
            self.procedure = estimate_config.get("estimation", None)
        self.procedure = ModelComponentCreator().get_model_component(self.procedure)
        if self.procedure == None:
            raise StandardError, "No estimation procedure given, or error when loading the corresponding module."
        
        if agent_set.size()<=0:
            agent_set.get_id_attribute()

        if agents_index==None:
            agents_index=arange(agent_set.size())

        if not isinstance(agents_index,ndarray):
            agents_index=array(agents_index)

        if self.compute_choice_attribute:
            agent_set.compute_variables([self.choice_attribute_name], dataset_pool=self.dataset_pool)
            
        self.model_interaction.set_agent_set(agent_set)

        self.set_choice_set_size()
        nchoices = self.get_choice_set_size()

        estimation_size_agents = estimate_config.get("estimation_size_agents", None) # should be a proportion of the agent_set
        if estimation_size_agents == None:
            estimation_size_agents = 1.0
        else:
            estimation_size_agents = max(min(estimation_size_agents,1.0),0.0) # between 0 and 1

        if estimation_size_agents < 1.0:
            self.debug.print_debug("Sampling agents for estimation ...",3)
            agents_index_for_estimation = sample_noreplace(agents_index,
                                                         int(agents_index.size*estimation_size_agents))
        else:
            agents_index_for_estimation = agents_index

        self.debug.print_debug("Number of agents for estimation: " + str(agents_index_for_estimation.size),2)
        if agents_index_for_estimation.size <= 0:
            self.debug.print_debug("Nothing to be done.",4)
            return None

        submodels = specification.get_distinct_submodels()
        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        self.map_agents_to_submodels(submodels, self.submodel_string, agent_set,
                                      agents_index_for_estimation,
                                      dataset_pool = self.dataset_pool,
                                      resources = Resources({"debug": self.debug}),
                                      submodel_size_max=self.estimate_config.get('submodel_size_max', None))
        
        self.create_interaction_datasets(agent_set, agents_index_for_estimation, estimate_config, submodels=submodels)
        ## move Choice set size log after compute_variables so it is not buried in compute_variable msg
        #logger.log_status("Choice set size: %i" % self.get_choice_set_size())
        #self.model_interaction.set_chosen_choice(agents_index_for_estimation)
        self.model_interaction.set_chosen_choice_if_necessary(agents_index=agents_index_for_estimation)
        index = self.model_interaction.get_choice_index()
        self.coefficients = create_coefficient_from_specification(specification)
        self.model_interaction.create_specified_coefficients(self.coefficients, specification, self.choice_set.get_id_attribute()[index])
        #run estimation
        result = self.estimate_step()
        return (self.coefficients, result)

    def create_interaction_datasets(self, agent_set, agents_index, config, **kwargs):
        """create interaction dataset agent_x_choice without sampling of alternatives
        config can be used to pass extra parameters to the sampler
        """
 
        if self.sampler_class is None:
            self.model_interaction.create_interaction_datasets(agents_index, arange(self.choice_set_size))
        else:
            nchoices = self.get_number_of_elemental_alternatives()
            if nchoices == self.choice_set.size():  
                #sampler class specified, but the sample size equals the size of choice set
                self.model_interaction.create_interaction_datasets(agents_index, arange(self.choice_set_size))
            else:
                sampling_weights = self.get_sampling_weights(config, agent_set=agent_set, agents_index=agents_index)
                choice_index = None
                chunk_specification = config.get("chunk_specification_for_sampling", ChunkSpecification({"nchunks":1}))
                nchunks = chunk_specification.nchunks(agents_index)
                chunksize = chunk_specification.chunk_size(agents_index)
                interaction_dataset = self.sample_alternatives_by_chunk(agent_set, agents_index, 
                                                                        choice_index, nchoices,
                                                                        weights=sampling_weights,
                                                                        config=config,
                                                                        nchunks=nchunks, chunksize=chunksize)
                self.update_choice_set_size(interaction_dataset.get_reduced_m())
                self.model_interaction.interaction_dataset = interaction_dataset
             
    def estimate_step(self):
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        self.model_interaction.compute_variables()
        
        logger.log_status("Choice set size: %i" % self.get_choice_set_size())
        
        coef = {}
        result = {}
        #index = self.estimate_config["index"]
        self.debug.print_debug("Estimate ...",4)
        for submodel in self.model_interaction.get_submodels():
            logger.log_status("submodel: %s" % submodel)
            self.increment_current_status_piece()
            self.model_interaction.prepare_data_for_estimation(submodel)
            coef[submodel] = self.model_interaction.get_submodel_coefficients(submodel)            
            self.coefficient_names[submodel] = self.model_interaction.get_coefficient_names(submodel)
            if self.model_interaction.is_there_data(submodel):   # observations for this submodel available
                self.estimate_config['index'] = self.model_interaction.get_choice_index_for_submodel(submodel)
                #if index <> None:
                    #    self.estimate_config["index"] = take (index, indices=self.observations_mapping[submodel], axis=0)
                # remove not used choices
                is_submodel_chosen_choice = self.model_interaction.set_chosen_choice_for_submodel_and_update_data(submodel)
                self.estimate_config["chosen_choice"] = is_submodel_chosen_choice
                self.estimate_config.merge({"coefficient_names":self.coefficient_names[submodel]})
                self.estimate_config.merge({"specified_coefficients": coef[submodel]})
                self.estimate_config.merge({"variable_names": self.model_interaction.get_variable_names(submodel)})
                self.estimate_config.merge({"fixed_values": self.model_interaction.get_coefficient_fixed_values(submodel)})
                self.estimate_config.merge({"submodel": submodel})
                self.estimate_config.merge({"_model_":self})
                result[submodel] = self.estimate_submodel(self.get_all_data(submodel), submodel)
                if "estimators" in result[submodel].keys():
                    coef[submodel].set_beta_alt(result[submodel]["estimators"])
                if "standard_errors" in result[submodel].keys():
                    coef[submodel].set_beta_se_alt(result[submodel]["standard_errors"])
                if "other_measures" in result[submodel].keys():
                    for measure in result[submodel]["other_measures"].keys():
                        coef[submodel].set_measure_from_alt(measure,
                              result[submodel]["other_measures"][measure])
                if "other_info" in result[submodel].keys():
                    for info in result[submodel]["other_info"]:
                        coef[submodel].set_other_info(info, result[submodel]["other_info"][info])
                coef[submodel].fill_beta_from_beta_alt()

                if self.estimate_config.get("export_estimation_data", False):
                    self.export_estimation_data(submodel, is_submodel_chosen_choice, self.get_all_data(submodel),
                                                coef[submodel].get_coefficient_names_from_alt(),
                                                self.estimate_config.get("estimation_data_file_name", './estimation_data.txt'),
                                                self.estimate_config.get("use_biogeme_data_format",False))

            self.coefficients.fill_coefficients(coef)
            self.estimate_config["coefficient_names"]=None
            self.estimate_config["variable_names"]=None
        return result

    def estimate_submodel(self, data, submodel=0):
        if self.model_interaction.is_there_data(submodel):
            return self.procedure.run(data, upc_sequence=self.upc_sequence, resources=self.estimate_config)
        return {}

    def get_sampling_weights(self, config, agent_set=None, agents_index=None, **kwargs):
        """Return weights_string in the config
        which is the value for key
        'weights_for_estimation_string' or 'weights_for_simulation_string'.
        Can be overwritten in child class and return an 1d or 2d array

        If it is the equal sign (i.e. '='), all choices have equal weights.
        
        """
        weights_string = None
        
        if config is not None:
            if config.get('estimate', False): #if we are in estimate()
                weights_string = config.get("weights_for_estimation_string", None)
            else:  # otherwise
                weights_string = config.get("weights_for_simulation_string", None)
                
            if weights_string == '=':
                return ones(self.choice_set.size(), dtype="int32")
          
        return weights_string
    
    def sample_alternatives_by_chunk(self, agent_set, agents_index, 
                                     choice_index, sample_size,
                                     weights=None, 
                                     with_replacement=False, 
                                     include_chosen_choice=None,
                                     config=None, 
                                     nchunks=1, chunksize=None):
        """Return interaction data with sampled alternatives (agents_index * sample_size)
        
        Do it in 'nchunks' iterations, and stack the results from each chunk
        
        """
        if not chunksize:
            chunksize=agents_index.size
        index2 = -1 + zeros((agents_index.size, sample_size), dtype="int32") 
        attributes = {}
        for ichunk in range(nchunks):
            index_for_ichunk = self.get_index_for_chunk(agents_index.size, ichunk, chunksize)
            agents_index_in_ichunk = agents_index[index_for_ichunk]
            interaction_dataset = self.sampler_class.run(agent_set, self.choice_set, 
                                                         index1=agents_index_in_ichunk,
                                                         index2=choice_index,
                                                         sample_size=sample_size,
                                                         weight=weights, 
                                                         with_replacement=with_replacement,
                                                         include_chosen_choice=include_chosen_choice,
                                                         resources=config,
                                                         dataset_pool=self.dataset_pool
                                                         )
            if nchunks>1:
                index2[index_for_ichunk,:] = interaction_dataset.index2
                for name in interaction_dataset.get_known_attribute_names():
                    attr_val = interaction_dataset.get_attribute(name)
                    if not attributes.has_key(name):
                        attributes[name] = zeros(index2.shape, dtype=attr_val.dtype)
                    attributes[name][index_for_ichunk,:] = attr_val
                    
        if nchunks>1:
            interaction_dataset = self.sampler_class.create_interaction_dataset(interaction_dataset.dataset1, 
                                                                                interaction_dataset.dataset2, 
                                                                                index1=agents_index, 
                                                                                index2=index2)
            for name in attributes.keys():
                interaction_dataset.add_attribute(attributes[name], name)

        return interaction_dataset

    def get_agents_for_chunk(self, agents_index, ichunk, chunksize):
        """Return ichunk with size chunksize in agents_index,
        return agents_index if chunksize >= agents_index.size
        """
        max_index = agents_index.size
        return agents_index[self.get_index_for_chunk(max_index, ichunk, chunksize)]

    def get_index_for_chunk(self, max_index, ichunk, chunksize):
        """
        """
        return arange(ichunk*chunksize, min((ichunk+1)*chunksize, max_index))

    def get_export_simulation_file_names(self, submodel, file_name):
        import os
        file_name_root, file_name_ext = os.path.splitext(file_name)
        if submodel < 0:
            submodel = ''
        else:
            submodel='_submodel%s' % submodel
        out_file_probs = "%s_probabilities%s%s" % (file_name_root, submodel, file_name_ext)
        out_file_choices = "%s_choices%s%s" % (file_name_root, submodel, file_name_ext)
        return (out_file_probs, out_file_choices)
                
    def get_probabilities_and_choices(self, submodel):
        """Return a tuple of probabilities (2d array, first column are the agent ids, remaining columns
        are probabilities for each choice) and choices (2d array of [possibly sampled] choice ids, 
                                                        where the first column are the agent ids)."""
        from numpy import argsort
        agent_ids = self.model_interaction.get_agent_ids_for_submodel(submodel)
        probs = concatenate((agent_ids[...,newaxis], self.upc_sequence.get_probabilities()), axis=1)
        choice_ids = concatenate((agent_ids[...,newaxis], self.model_interaction.get_choice_ids_for_submodel(submodel)), axis=1)
        # sort results
        order_idx = argsort(agent_ids)
        probs = probs[order_idx,:]
        choice_ids = choice_ids[order_idx,:]
        return (probs, choice_ids)
        
    def export_probabilities(self, submodel, file_name):
        """Export the current probabilities into a file.
        """
        from opus_core.misc import write_table_to_text_file
        
        if self.index_of_current_chunk == 0:
            mode = 'w'
        else:
            mode = 'a'
        export_file_probs, export_file_choices = self.get_export_simulation_file_names(submodel, file_name)
        probs, choice_ids = self.get_probabilities_and_choices(submodel)
        logger.start_block('Exporting probabilities (%s x %s) into %s' % (probs.shape[0], probs.shape[1], export_file_probs))
        write_table_to_text_file(export_file_probs, probs, mode=mode, delimiter='\t')
        logger.end_block()
        logger.start_block('Exporting choices into %s' % export_file_choices)
        write_table_to_text_file(export_file_choices, choice_ids, mode=mode, delimiter='\t')
        logger.end_block()
        
    def export_estimation_data(self, submodel, is_chosen_choice, data, coef_names, file_name, use_biogeme_data_format=False):
        from numpy import reshape, repeat
        import os
        delimiter = '\t'
        if use_biogeme_data_format:
            nobs, alts, nvars = data.shape

            avs = ones(shape=(nobs,alts,1))  # if the choice is available, set to all ones
            data = concatenate((data, avs),axis=2)
            coef_names = coef_names.tolist() + ['av']
            nvars += 1

            try:
                from numpy import argsort
                stratum_id = self.sampler_class._stratum_id[...,newaxis]
                data = concatenate((data, stratum_id, self.sampler_class._sampling_probability[...,newaxis], ),axis=2)
                iid = argsort(stratum_id, axis=1)
                for i in range(data.shape[0]):  # re-arrange data based on stratum id
                    data[i,...] = data[i,...][iid[i,:,0]]
                    is_chosen_choice[i,:] = is_chosen_choice[i,:][iid[i,:,0]]

                coef_names = coef_names + ['stratum', 'sampling_prob']
                nvars += 2
                logger.log_status("added variables specific to stratified sampler")
            except:
                pass

            chosen_choice = where(is_chosen_choice)[1] + 1
            index_of_non_constants = []
            for i in range(nvars):
                if not (coef_names[i] == "constant"):
                    index_of_non_constants.append(i)

            index_of_non_constants = array(index_of_non_constants)
            nvars_without_const = index_of_non_constants.size
            #additional 2 columns for ID and choice
            data_for_biogeme = zeros((nobs, alts*nvars_without_const + 1), dtype=float64)

            biogeme_var_names = []
            for ivar in range(nvars_without_const):
                for ialt in range(alts):
                    biogeme_var_names.append(coef_names[index_of_non_constants[ivar]] + "_" + str(ialt+1))
                    data_for_biogeme[:,1+ivar*alts+ialt] = data[:,ialt, index_of_non_constants[ivar]]

            data_for_biogeme[:, 0] = chosen_choice
            ids = reshape(arange(nobs)+1, (nobs,1))
            data_for_biogeme = concatenate((ids, data_for_biogeme),axis=1)
            data = data_for_biogeme

            header = ['ID', 'choice'] + biogeme_var_names
            nrows, ncols = data.shape
        else:
            nobs, alts, nvars = data.shape
            ids = reshape(repeat(arange(nobs, dtype='int32')+1, alts), (nobs,alts,1))
            data = concatenate((ids, is_chosen_choice[...,newaxis].astype("int16"), data),axis=2)
            nvars += 2
            nrows = nobs * alts
            header = ['ID', 'choice'] + coef_names.tolist()
            data = reshape(data,(-1,nvars))


        file_name_root, file_name_ext = os.path.splitext(file_name)
        out_file = "%s_submodel_%s.txt" % (file_name_root, submodel)
        fh = open(out_file,'w')
        fh.write(delimiter.join(header) + '\n')   #file header
        for row in range(nrows):
            line = [str(x) for x in data[row,]]
            fh.write(delimiter.join(line) + '\n')

        fh.flush()
        fh.close
        print 'Data written into %s' % out_file

    def get_agents_order(self, agents):
        return permutation(agents.size())
    
    def set_choice_set_size(self):
        """If "sample_size" is specified in resources, it is considered as the choice set size. Otherwise
        the value of resources entry "sample_proportion_locations" is considered as determining the size of 
        the choice set.
        """
        if self.sampler_class is not None:
            pchoices =  self.run_config.get("sample_proportion_locations", None)
            nchoices =  self.run_config.get("sample_size_locations", None)
            if nchoices == None:
                if pchoices == None:
                    logger.log_warning("Neither 'sample_proportion_locations' nor 'sample_size_locations' " +
                                       "given. Choice set will not be sampled.")
                    nchoices = self.choice_set.size()
                else:
                    nchoices = int(pchoices*self.choice_set.size())
        else:
            nchoices = self.choice_set.size()
        self.choice_set_size =  min(nchoices, self.choice_set.size())

    def update_choice_set_size(self, nchoices):
        """
        update self.choice_set_size if necessary
        when the sampler class is stratified_sampler that won't be able to know 
        the accurate number of choice beforehand, this method update the choice
        set size after the sampler_class is run.
        """
        self.choice_set_size = nchoices

    #def set_choice_set_size(self):
        #self.choice_set_size = self.choice_set.size()
        
    def get_choice_set_size(self):
        return self.choice_set_size

    def get_number_of_elemental_alternatives(self):
        return self.get_choice_set_size()

    def plot_histogram(self, main="", file=None):
        """Plots histogram of choices and probabilities for the last chunk."""
        self.upc_sequence.plot_histogram(main=main)
        self.upc_sequence.show_plots(file)

    def plot_histogram_of_choices(self, index=None, main="", bins=None):
        """Plots a histogram of choices for the whole dataset.
        """
        from opus_core.plot_functions import plot_histogram
        if self.result_choices is None:
            raise StandardError, "Model does not have any results. Try to run it first."
        if index is None:
            values = self.result_choices
        else:
            values = self.result_choices[index]
        plot_histogram(values, main, xlabel="choices", bins=bins)

    def prepare_for_run(self, agent_set=None, agent_filter=None, filter_threshold=0, **kwargs):
        spec, coef = prepare_specification_and_coefficients(**kwargs)
        if (agent_set is not None) and (agent_filter is not None):
            filter_values = agent_set.compute_variables([agent_filter], dataset_pool=self.dataset_pool)
            index = where(filter_values > filter_threshold)[0]
        else:
            index = None
        return (spec, coef, index)
    
    def prepare_for_estimate(self, agent_set=None, agent_filter=None, filter_threshold=0, **kwargs):
        spec = get_specification_for_estimation(**kwargs)
        if (agent_set is not None) and (agent_filter is not None):
            filter_values = agent_set.compute_variables([agent_filter], dataset_pool=self.dataset_pool)
            index = where(filter_values > filter_threshold)[0]
        else:
            index = None
        return (spec, index)
    
    def get_data(self, coefficient, submodel=-2):
        return ChunkModel.get_data(self, coefficient, submodel, is3d=True)

    def get_dataset_pool(self):
        return self.dataset_pool
    
    def get_data_as_dataset(self, submodel=-2):
        """Like get_all_data, but the returning value is an InteractionDataset containing attributes that
        correspond to the data columns. Their names are coefficient names."""
        all_data = self.get_all_data(submodel)
        if all_data is None:
            return None
        names = self.get_coefficient_names(submodel)
        if names is None:
            return None
        dataset_data = {}
        for i in range(names.size):
            dataset_data[names[i]] = all_data[:, :, i].reshape((all_data.shape[0], all_data.shape[1]))
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name = 'dataset', 
                            table_data = dataset_data)
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name=[])
        return ds

    def get_all_data(self, submodel):
        return self.model_interaction.get_data(submodel)
        
    def get_specified_coefficients(self):
        return self.model_interaction.get_specified_coefficients()
        
    def _get_status_total_pieces(self):
        return ChunkModel._get_status_total_pieces(self) * self.get_status_for_gui().get_total_number_of_pieces()
    
    def _get_status_current_piece(self):
        return ChunkModel._get_status_current_piece(self)*self.get_status_for_gui().get_total_number_of_pieces() + self.get_status_for_gui().get_current_piece()
        
    def _get_status_piece_description(self):
        return "%s %s" % (ChunkModel._get_status_piece_description(self), self.get_status_for_gui().get_current_piece_description())

       
class ModelInteraction:
    """ This class handles all the work that involves the interaction dataset of the Choice model."""
    def __init__(self, model, package=None, choice_set=None):
        self.interaction_package = package
        self.choice_set = choice_set
        if (choice_set is not None):
            if isinstance(choice_set, str): # can be a dataset name
                self.choice_set = model.dataset_pool.get_dataset(choice_set)
        self.interaction_module = None
        self.interaction_class_name = None
        self.interaction_dataset = None
        self.model = model
        self.interaction_resources = None
        self.data = {}
        self.specified_coefficients = None
        self.chosen_choice = None
        self.chosen_choice_per_submodel = {}
        self.submodel_coefficients = {}
        
    def set_agent_set(self, agent_set):
        self.agent_set = agent_set
        factory = DatasetFactory()
        self.interaction_module, self.interaction_class_name = \
            factory.compose_interaction_dataset_name(self.agent_set.get_dataset_name(),
                                                         self.choice_set.get_dataset_name())

    def create_interaction_datasets(self, agents_index, choice_set_index):
        # free memory of existing interaction set
        if isinstance(self.interaction_dataset, InteractionDataset):
            self.interaction_dataset.unload_all_attributes()
            gc.collect()
                
        self.interaction_resources = Resources({"debug":self.model.debug})
        try:
            self.interaction_dataset = ClassFactory().get_class(
                            self.interaction_package+"."+self.interaction_module,
                            class_name=self.interaction_class_name,
                                arguments={"dataset1":self.agent_set, "dataset2":self.choice_set,
                                           "index1":agents_index, "index2":choice_set_index})
        except ImportError:
            self.interaction_dataset = InteractionDataset(dataset1=self.agent_set, dataset2=self.choice_set,
                                              index1=agents_index, index2=choice_set_index, debug=self.model.debug)

    def get_choice_index(self):
            return self.interaction_dataset.get_2d_index()

    def get_choice_index_for_submodel(self, submodel):
        index = self.get_choice_index()
        if index is not None:
            return take(index, self.model.observations_mapping[submodel], axis=0)

    def get_choice_ids_for_submodel(self, submodel):
        index = self.get_choice_index_for_submodel(submodel)
        if index is not None:
            return self.interaction_dataset.get_dataset(2).get_id_attribute()[index]
        
    def get_agent_ids_for_submodel(self, submodel):
        return self.interaction_dataset.get_id_attribute_of_dataset(1)[self.model.observations_mapping[submodel]]
                                                 
    def compute_variables(self, variables=None):
        if variables is not None:
            var_list_for_this_choice_set = variables
        else:
            var_list_for_this_choice_set = \
                    self.specified_coefficients.get_variables_without_constants_and_reserved_names()
        if var_list_for_this_choice_set is not None and len(var_list_for_this_choice_set) > 0:
            self.interaction_dataset.compute_variables(var_list_for_this_choice_set,
                                                           dataset_pool=self.model.dataset_pool,
                                                           resources = self.interaction_resources)

    def prepare_data_for_simulation(self, submodel):
        # free up memory from previous chunks
        if submodel in self.data.keys():
            del self.data[submodel]
            gc.collect()
             
        self.submodel_coefficients[submodel] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients, submodel)
        self.data[submodel] = self.interaction_dataset.create_logit_data(self.submodel_coefficients[submodel], 
                                                                            index = self.model.observations_mapping[submodel])

    def prepare_data_for_estimation(self, submodel):
        self.submodel_coefficients[submodel] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients, submodel)
        self.data[submodel] = self.interaction_dataset.create_logit_data_from_beta_alt(
                                                                  self.submodel_coefficients[submodel], 
                                                                  index=self.model.observations_mapping[submodel])
           
    def convert_data_from_estimation_to_simulation_format(self, submodel):
        from numpy import repeat, newaxis, sort, reshape
        from opus_core.ndimage import sum as ndimage_sum
        coef = self.submodel_coefficients[submodel]
        data = self.data[submodel]
        nvar = coef.get_coefficient_values().shape[1]
        if data.shape[2] == nvar: return data # no difference
        labels = repeat(coef.get_coefmap_alt()[newaxis,...]+1, data.shape[1], axis=0)
        for i in range(1, labels.shape[0]):
            labels[i,:] = labels[i,:] + i*nvar
        index = repeat(unique(coef.get_coefmap_alt())[newaxis,...]+1, data.shape[1], axis=0)
        for i in range(1, index.shape[0]):
            index[i,:] = index[i,:] + i*nvar
        data_sim = zeros((data.shape[0], data.shape[1], nvar), dtype=data.dtype)
        for i in range(data_sim.shape[0]):
            data_sim[i,:,:] = reshape(array(ndimage_sum(data[i,:,:], labels, index=index)), index.shape)
        return data_sim
    
    def get_submodel_coefficients(self, submodel):
        return self.submodel_coefficients[submodel]
        
    def remove_rows_from_data(self, where_not_remove, submodel):
        self.data[submodel] = compress(where_not_remove, self.data[submodel], axis=0)
        
    def get_data(self, submodel):
        return self.data[submodel]
        
    def create_specified_coefficients(self, coefficients, specification, choice_ids=None):
        equation_ids=None
        if len(choice_ids.shape) > 1:
            same_ids = True
            for i in range(choice_ids.shape[1]):
                if not alltrue(choice_ids[:,i]==choice_ids[0,i]):
                    same_ids=False
                    break
            if same_ids:
                equation_ids = choice_ids[0,:]
        else:
            equation_ids = choice_ids

        nchoices = self.model.get_choice_set_size()
        self.specified_coefficients = SpecifiedCoefficients().create(coefficients, specification, neqs=nchoices, 
                                                                     equation_ids=equation_ids)
            
    def get_specified_coefficients(self):
        return self.specified_coefficients
    
    def get_submodels(self):
        return self.specified_coefficients.get_submodels()

    def set_chosen_choice_if_necessary(self, agents_index=None, chosen_choice=None):
        if 'chosen_choice' not in self.interaction_dataset.get_known_attribute_names():
            self.set_chosen_choice(agents_index=agents_index, chosen_choice=chosen_choice)
        else:
            self.chosen_choice = self.get_chosen_choice_index()
            
    def set_chosen_choice(self, agents_index=None, chosen_choice=None):
        if chosen_choice is None: 
            if agents_index is None:
                raise ValueError, "Either agents_index or chosen_choice must be specified"
            else: 
                chosen_choice = self.choice_set.get_id_index(id=
                                                                 self.agent_set.get_attribute_by_index(self.choice_set.get_id_name()[0],
                                                                                                       agents_index)
                                                                 )            
        if chosen_choice.ndim==1:
            data = (self.get_choice_index() - chosen_choice[:, newaxis]) == 0
        elif chosen_choice.ndim==2:
            data = chosen_choice
        assert data.shape == self.get_choice_index().shape
        self.interaction_dataset.add_attribute(data=data,
                                               name="chosen_choice")
        
        self.chosen_choice = self.get_chosen_choice_index()
            
    def get_chosen_choice_index(self):
        if 'chosen_choice' in self.interaction_dataset.get_known_attribute_names():
            chosen_choice_index = self.get_choice_index()[self.interaction_dataset.get_attribute('chosen_choice')]

        return chosen_choice_index
    
    def get_chosen_choice(self):
        if "chosen_choice" in self.interaction_dataset.get_known_attribute_names():
            chosen_choice = self.interaction_dataset.get_attribute("chosen_choice")

        return chosen_choice

    def set_chosen_choice_for_submodel_and_update_data(self, submodel):
        chosen_choice = self.get_chosen_choice()
        is_submodel_chosen_choice = take(chosen_choice, indices=self.model.observations_mapping[submodel],
                                                                                            axis=0)
        # remove choices not being chosen by any agents
        is_submodel_chosen_choice = take(is_submodel_chosen_choice, 
                                               indices=self.submodel_coefficients[submodel].get_equations_index(), 
                                               axis=1)
        sumchoice = is_submodel_chosen_choice.sum(axis=1, dtype=int32)
        where_not_remove = where(sumchoice == 0, False, True)
        if False in where_not_remove:
            is_submodel_chosen_choice = compress(where_not_remove, is_submodel_chosen_choice, axis=0)
            self.remove_rows_from_data(where_not_remove, submodel)
        self.chosen_choice_per_submodel[submodel] = is_submodel_chosen_choice
        return is_submodel_chosen_choice
    
    def get_chosen_choice_for_submodel(self, submodel):
        return self.chosen_choice_per_submodel[submodel]
        
    def get_coefficient_names(self, submodel):
        return self.submodel_coefficients[submodel].get_coefficient_names_from_alt()
        
    def get_variable_names(self, submodel):
        return self.submodel_coefficients[submodel].get_variable_names_from_alt()
        
    def get_variable_names_for_simulation(self, submodel):
        return array(self.submodel_coefficients[submodel].get_variable_names())
        
    def get_coefficient_fixed_values(self, submodel):
        return self.specified_coefficients.specification.get_coefficient_fixed_values_for_submodel(submodel)
        
    def is_there_data(self, submodel):
        if (self.data[submodel].shape[0] <= 0) or (self.data[submodel].size <= 0):
            return False
        return True
    
if __name__=="__main__":
    import os
    import tempfile
    from shutil import rmtree
    from opus_core.tests import opus_unittest
    from numpy import ma, alltrue
    from opus_core.ndimage import sum as ndimage_sum
    from opus_core.tests.stochastic_test_case import StochasticTestCase
    from opus_core.simulation_state import SimulationState
    from opus_core.misc import load_table_from_text_file, unique


    class Test(StochasticTestCase):
        def tearDown(self):
            SimulationState().remove_base_cache_directory()

        def test_do_nothing_if_no_agents(self):
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(
                table_name = 'households',
                table_data = {
                    "household_id": arange(10000)+1,
                    "autos": array(10000*[-1])
                    }
                )

            #create households
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

            # create coefficients and specification
            coefficients = Coefficients(names=("costcoef", ), values=(-0.001,))
            specification = EquationSpecification(variables=("autos", ), coefficients=("costcoef", ))

            # run the model
            cm = ChoiceModel(choice_set=[0,1,2,3], choices = "opus_core.random_choices_from_index")
            result = cm.run(specification, coefficients, agent_set=households, agents_index=array([], dtype='int32'), debuglevel=1)
            # check
            self.assertEqual(result.size , 0)

        def test_agents_do_not_choose_certain_mode_if_low_income(self):
            """4 modes;
            10,000 households - 5000 with no low income, 5000 with low income
            Attractiveness for mode 4 if low income is -100, otherwise 0.001.
            Result: No household with low income should choose mode 4. The number of households that chose
                    remaining modes should be equally distributed.
            """
            #create households
            household_data = {"household_id": arange(10000)+1, "is_low_income": array(5000*[0]+5000*[1])}
            modes=array([1,2,3,4])
            # create coefficients and specification (different coefficient names for each equation)
            coefficients = Coefficients(names=("li1", "li2","li3","li4"), values=(0.001, 0.001, 0.001, -100))
            specification = EquationSpecification(variables=("household.is_low_income", "household.is_low_income",
                                                   "household.is_low_income", "household.is_low_income"),
                                                  coefficients=("li1", "li2","li3","li4"),
                                                  equations=(1,2,3,4))
            # using ASCs
#            coefficients = Coefficients(names=("li1", "asc2", "li2", "asc3", "li3", "asc4", "li4"),
#                                        values=(0, 0.1, 0, 0.1, 0, 0.1, -100))
#            specification = EquationSpecification(variables=("household.is_low_income", "constant", "household.is_low_income",
#                                                             "constant", "household.is_low_income", "constant", "household.is_low_income"),
#                                                  coefficients=("li1", "asc2", "li2", "asc3", "li3", "asc4", "li4"),
#                                                  equations=(1,2,2,3,3,4,4))
            tmp = ones(5000, dtype="int32")
            # run the model
            def run_model():
                storage = StorageFactory().get_storage('dict_storage')

                storage.write_table(
                    table_name = 'households', 
                    table_data = household_data)

                households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

                cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")

                result = cm.run(specification, coefficients, agent_set=households,
                             chunk_specification={'nchunks':1},
                             debuglevel=1)

                nli = ndimage_sum(tmp, labels=result[0:5000], index=modes)
                li = ndimage_sum(tmp, labels=result[5000:10000], index=modes)

                return array(nli+li)

            # first 4 - distribution of modes should be the same for households with no low income
            # second 4 - distribution of modes 1-3 should be the same for households with low income and 0 for mode 4.
            expected_results = array(4*[1250]+3*[1667]+[0])
            self.run_stochastic_test(__file__, run_model, expected_results, 10)


        def test_estimate_and_simulate_4_mode_model(self):
            """4 modes;
            10,000 households - 5000 with no low income, 5000 with low income
            The modes 1-4 are equally distributed among households that don't have low income.
            Households with low income decided equally for choices 2 and 3 (2490 hhs per choice) and only few of them decided for choices
            1 and 4 (10 households per choice).
            Coefficients for "is_low_income" are estimated separately for each choice where the first
            choice is the reference alternative (coef. li2, li3, li4).
            Result: Coefficient li4 should be close to 0, since the same number of households with low income  decided for
            alternative 1 and 4.  Coefficient li2 and li3 should be positive and equal.
            A simulation with the estimated coefficients is run and the resulting distribution should correspond to the original
            data.
            """
            storage = StorageFactory().get_storage('dict_storage')

            household_data = {
                'household_id': arange(10000)+1,
                'is_low_income': array(5000*[0]+5000*[1]),
                'choice_id':array(1250*[1] + 1250*[2] + 1250*[3] + 1250*[4] + 10*[4] + 2490*[3] + 10*[1] + 2490*[2])
                }

            storage.write_table(
                table_name = 'households', 
                table_data = household_data)

            # create households
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

            modes=array([1,2,3,4])

            specification = EquationSpecification(variables=("household.is_low_income",
                                                             "household.is_low_income",
                                                             "household.is_low_income", "constant"),
                                                  coefficients=( "li2", "li3","li4","c"),
                                                  equations=(2,3,4,1))
            cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
            coef, dummy = cm.estimate(specification, agent_set = households,
                                       procedure="opus_core.bhhh_mnl_estimation", debuglevel=4)
            li2=coef.get_values_of_one_coefficient("li2")
            li3=coef.get_values_of_one_coefficient("li3")
            li4=coef.get_values_of_one_coefficient("li4")
            self.assertEqual(ma.allclose(li2, li3 , rtol=0.00001), True)
            self.assertEqual(li2 > 1, True)
            self.assertEqual(ma.allclose(li4, 0 , rtol=0.00001), True)

            tmp = ones(5000, dtype="int32")

            def run_model():
                storage = StorageFactory().get_storage('dict_storage')

                storage.write_table(
                    table_name = 'households', 
                    table_data = household_data)

                households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")
                cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
                # run a simulation with the estimated coefficients
                result = cm.run(specification, coef, agent_set=households,
                                 chunk_specification={'nchunks':1},
                                 debuglevel=1, run_config=Resources({"demand_string": "choice.demand"}))
                nli = ndimage_sum(tmp, labels=result[0:5000], index=modes)
                li = ndimage_sum(tmp, labels=result[5000:10000], index=modes)
                self.demand = cm.choice_set.get_attribute("demand")
                return array(nli+li)
            # distribution of modes should correspond to the original data
            expected_results = array(4*[1250] + [10, 2490, 2490, 10])
            self.run_stochastic_test(__file__, run_model, expected_results, 10)
            #check aggregated demand
            self.assertEqual(ma.allclose(self.demand, array([1260, 3740, 3740, 1260]) , rtol=0.1), True)
            
            # estimate with a fixed value of one coefficient and check that the value of this coefficint is the assigned one
            specification = EquationSpecification(variables=("household.is_low_income",
                                                             "household.is_low_income",
                                                             "household.is_low_income", "constant", "__dummy"),
                                                  coefficients=( "li2", "li3","li4","c", "a"),
                                                  equations=(2,3,4,1,1),
                                                  fixed_values=(0,0,0,0,2))
            coef, dummy = cm.estimate(specification, agent_set = households,
                                       procedure="opus_core.bhhh_mnl_estimation", debuglevel=4)
            a=coef.get_values_of_one_coefficient("a")
            self.assertEqual(ma.allclose(a, 2 , rtol=0.00001), True)

        def test_estimate_and_simulate_4_mode_model_with_reference_equation(self):
            """Like test_estimate_and_simulate_4_mode_model, but the reference equation (the first one) does not have any terms.
            Furthermore, the equations have arbitrary ids.
            """
            storage = StorageFactory().get_storage('dict_storage')

            household_data = {
                'household_id': arange(10000)+1,
                'is_low_income': array(5000*[0]+5000*[1]),
                'choice_id':array(1250*[3] + 1250*[5] + 1250*[10] + 1250*[25] + 10*[25] + 2490*[10] + 10*[3] + 2490*[5])
                }

            storage.write_table(
                table_name = 'households', 
                table_data = household_data)

            # create households
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

            modes=array([3,5,10,25])

            specification = EquationSpecification(variables=("household.is_low_income", "constant",
                                                             "household.is_low_income", "constant",
                                                             "household.is_low_income", "constant"),
                                                  coefficients=( "li2", "c2", "li4", "c4", "li3", "c3"),
                                                  equations=(5,5,25,25,10,10))
            cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
            coef, dummy = cm.estimate(specification, agent_set = households,
                                       procedure="opus_core.bhhh_mnl_estimation", debuglevel=4)
            li2=coef.get_values_of_one_coefficient("li2")
            li3=coef.get_values_of_one_coefficient("li3")
            li4=coef.get_values_of_one_coefficient("li4")
            self.assertEqual(ma.allclose(li2, li3 , rtol=0.00001), True)
            self.assertEqual(li2 > 1, True)
            self.assertEqual(ma.allclose(li4, 0 , rtol=0.00001), True)
            
            tmp = ones(5000, dtype="int32")

            def run_model():
                storage = StorageFactory().get_storage('dict_storage')

                storage.write_table(
                    table_name = 'households', 
                    table_data = household_data)

                households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")
                cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
                # run a simulation with the estimated coefficients
                result = cm.run(specification, coef, agent_set=households,
                                 chunk_specification={'nchunks':1},
                                 debuglevel=1, run_config=Resources({"demand_string": "choice.demand"}))
                nli = ndimage_sum(tmp, labels=result[0:5000], index=modes)
                li = ndimage_sum(tmp, labels=result[5000:10000], index=modes)
                self.demand = cm.choice_set.get_attribute("demand")
                return array(nli+li)
            # distribution of modes should correspond to the original data
            expected_results = array(4*[1250] + [10, 2490, 2490, 10])
            self.run_stochastic_test(__file__, run_model, expected_results, 10)
            #check aggregated demand
            self.assertEqual(ma.allclose(self.demand, array([1260, 3740, 3740, 1260]) , rtol=0.1), True)
            
        def test_estimate_and_simulate_2_mode_model_with_reference_equation(self):
            """2 modes;
            10,000 households - 5000 with no low income, 5000 with low income
            The modes 1-2 are equally distributed among households that don't have low income.
            Most of the households with low income decided for choice 1 (4700) and much less households decided for choice 2 (300).
            Coefficient for "is_low_income" (li) is estimated for choice 1 (the second choice is the reference alternative 
            and does not have any entries in the specification).
            Result: Coefficient li should be positive.
            A simulation with the estimated coefficient is run and the resulting distribution should correspond to the original
            data.
            """
            storage = StorageFactory().get_storage('dict_storage')

            household_data = {
                'household_id': arange(10000)+1,
                'is_low_income': array(5000*[0]+5000*[1]),
                'choice_id':array(2500*[1] + 2500*[2] + 4700*[1] + 300*[2])
                }

            storage.write_table(
                table_name = 'households', 
                table_data = household_data)

            # create households
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

            modes=array([1,2])

            specification = EquationSpecification(variables=("household.is_low_income", "constant"),
                                                  coefficients=( "li", "c"),
                                                  equations=(1,1))
            cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
            coef, dummy = cm.estimate(specification, agent_set = households,
                                       procedure="opus_core.bhhh_mnl_estimation", debuglevel=4)
            li=coef.get_values_of_one_coefficient("li")[0]
            self.assertEqual(li > 1, True)
            
            tmp = ones(5000, dtype="int32")

            def run_model():
                storage = StorageFactory().get_storage('dict_storage')

                storage.write_table(
                    table_name = 'households', 
                    table_data = household_data)

                households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")
                cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices")
                # run a simulation with the estimated coefficients
                result = cm.run(specification, coef, agent_set=households,
                                 chunk_specification={'nchunks':1},
                                 debuglevel=1, run_config=Resources({"demand_string": "choice.demand"}))
                nli = ndimage_sum(tmp, labels=result[0:5000], index=modes)
                li = ndimage_sum(tmp, labels=result[5000:10000], index=modes)
                self.demand = cm.choice_set.get_attribute("demand")
                return array(nli+li)
            # distribution of modes should correspond to the original data
            expected_results = array(2*[2500] + [4700, 300])
            self.run_stochastic_test(__file__, run_model, expected_results, 10)
            #check aggregated demand
            self.assertEqual(ma.allclose(self.demand, array([7200, 2800]) , rtol=0.1), True)
             
        def test_run_model_and_write_simulation_data(self):
            temp_dir = tempfile.mkdtemp(prefix='opus_choice_model_test')
            storage = StorageFactory().get_storage('dict_storage')

            household_data = {
                'household_id': arange(100)+1,
                'is_low_income': array(50*[0]+50*[1])
                }
            location_data = {
                 'location_id': arange(500) +1,
                 'cost': array(100*[20] + 100*[30] + 100*[50] + 200*[100])
                 }
            storage.write_table(
                table_name = 'households', 
                table_data = household_data)
            storage.write_table(
                table_name = 'locations', 
                table_data = location_data)
            specification = EquationSpecification(variables=("household.is_low_income*location.cost",),
                                                  coefficients=("lic",))
            coef = Coefficients(names=("lic",), values=(0.01,))
            # create households
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")
            locations = Dataset(in_storage=storage, in_table_name='locations', id_name="location_id", dataset_name="location")
            
            cm = ChoiceModel(choice_set=locations, choices = "opus_core.random_choices",
                             sampler='opus_core.samplers.weighted_sampler')
            cm.run(specification, coef, agent_set=households,
                                 chunk_specification={'nchunks':2},
                                 debuglevel=1, 
                                 run_config=Resources({"sample_size_locations": 10,
                                                       "export_simulation_data": True,
                                                       "simulation_data_file_name": os.path.join(temp_dir, 'sim_data.txt') })
                                 )
            probs = load_table_from_text_file(os.path.join(temp_dir, 'sim_data_probabilities.txt'))[0]
            self.assert_(all(probs.shape == array([100, 11])))
            self.assertEqual(unique(probs[:,0]).size == 100, True)
            choices = load_table_from_text_file(os.path.join(temp_dir, 'sim_data_choices.txt'))[0]
            self.assert_(all(choices.shape == array([100, 11])))
            self.assertEqual(unique(choices[:,0]).size == 100, True)
            rmtree(temp_dir)
    opus_unittest.main()
