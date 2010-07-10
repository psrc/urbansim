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
from opus_core.model_component_creator import ModelComponentCreator
from opus_core.misc import DebugPrinter
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.chunk_model import ChunkModel
from opus_core.class_factory import ClassFactory
from opus_core.model import get_specification_for_estimation, prepare_specification_and_coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from numpy import where, zeros, array, arange, ones, take, ndarray, resize, concatenate, alltrue
from numpy import int32, compress, float64
from numpy.random import permutation

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
                        submodel_string=None,
                        choice_attribute_name="choice_id",
                        interaction_pkg="opus_core",
                        upper_level_choice_set=None,
                        run_config=None, estimate_config=None, debuglevel=0,
                        dataset_pool=None):
        """
        Arguments:
            choice_set - Dataset or array/list of choices.
            utilities - name of utilities module
            probabilities - name of probabilities module
            choices - name of module for computing agent choices
            submodel_string - character string specifying what agent attribute determines submodels.
            choice_attribute_name - name of the attribute that identifies the choices. This argument is
                only relevant if choice_set is not an instance of Dataset.
                Otherwise the choices are identified by the unique identifier of choice_set.
            interaction_pkg - only relevant if there is an implementation of an interaction dataset
                that corresponds to interaction between agents and choices.
            upper_level_choice_set - Dataset for hierarchical choice models, e.g. nested logit. It is either a Dataset or
                                    dataset name. In the latter case it is loaded from dataset_pool.
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
        self.submodel_string = submodel_string # which attribute determines submodels
        self.run_config = run_config
        if self.run_config == None:
            self.run_config = Resources()
        self.estimate_config = estimate_config
        if self.estimate_config == None:
            self.estimate_config = Resources()
        self.result_choices = None
        self.dataset_pool = self.create_dataset_pool(dataset_pool)
        self.coefficient_names = {}
        self.model_interaction = ModelInteraction(self, interaction_pkg, [self.choice_set, upper_level_choice_set])
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
        self.run_config = run_config.merge_with_defaults(self.run_config)

        if agents_index==None:
            agents_index=arange(agent_set.size())

        if self.compute_choice_attribute:
            agent_set.compute_variables([self.choice_attribute_name], dataset_pool=self.dataset_pool)
            
        if self.run_config.get("demand_string", None):
            self.choice_set.add_primary_attribute(name=self.run_config.get("demand_string"),
                                          data=zeros(self.choice_set.size(), dtype="float32"))
            self.compute_demand_flag = True
        else:
            self.compute_demand_flag = False

        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        self.model_interaction.set_agent_set(agent_set)
        self.result_choices = ChunkModel.run(self, chunk_specification, agent_set, agents_index, int32,
                                 specification=specification, coefficients=coefficients)
        return self.result_choices

    def run_chunk(self, agents_index, agent_set, specification, coefficients):

        if agents_index.size <= 0:
            return array([], dtype='int32')
        agentsubset = DatasetSubset(agent_set, agents_index)

        self.set_choice_set_size()  
        index = self.get_choice_index(agent_set, agents_index, agentsubset)
        nchoices = self.get_choice_set_size()
        logger.log_status("Choice set size: %s" % str(nchoices))
        
        if isinstance(index, ndarray):
            if (index.size <= 0) or ((index.ndim > 1) and (index.shape[1]<=0)):
                return zeros(agents_index.size, dtype="int32")
        #create interaction set
        self.model_interaction.create_interaction_datasets(agents_index, {0: index})

        logger.log_status("Create specified coefficients ...")
        self.model_interaction.create_specified_coefficients(coefficients, specification, self.choice_set.get_id_attribute()[index])
        self.run_config.merge({"index":index})

        submodels = self.model_interaction.get_submodels()
#        logger.log_status("Number of submodels: %s" % str(submodels))
        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        self.map_agents_to_submodels(submodels, self.submodel_string, agent_set, agents_index,
                                      dataset_pool=self.dataset_pool, resources = Resources({"debug": self.debug}))
        
        # simulate
        choice_indices = self.simulate_chunk()
        choice_set_ids = self.choice_set.get_id_attribute()
        choices = where(choice_indices < 0, -1, choice_set_ids[choice_indices])
        del self.run_config["index"]
        return choices

    def simulate_chunk(self):
        logger.log_status("Compute variables ...")
        self.increment_current_status_piece()
        self.model_interaction.compute_variables()
        coef = {}
        result = resize(array([-1], dtype="int32"), self.observations_mapping["index"].size)
        index = self.run_config["index"]
        logger.log_status("Simulate ...")
        for submodel in self.model_interaction.get_submodels():
            self.model_interaction.prepare_data_for_simulation(submodel)
            coef[submodel] = self.model_interaction.get_submodel_coefficients(submodel)
#            logger.log_status("   submodel: %s   nobs: %s" % (submodel, self.observations_mapping[submodel].size))
            self.increment_current_status_piece()
            if self.model_interaction.is_there_data(submodel): # observations for this submodel available
                if index is not None:
                    self.run_config["index"] = take (index, indices=self.observations_mapping[submodel], axis=0)
                coefficients = coef[submodel].get_coefficient_values()
                res = self.simulate_submodel(self.get_all_data(submodel), coefficients, submodel)
                restmp = res.astype(int32)
                res_positive_idx = where(res>=0)[0]
                if index is not None:
                    if index.shape[1] <> coef[submodel].nequations():
                        restmp[res_positive_idx] = array(map(lambda x:
                            index[x,coef[submodel].get_equations_index()[res[x]]], res_positive_idx)).astype(int32)
                else: # this is bypassed with no-change models.....
                    restmp[res_positive_idx] = coef[submodel].get_equations_index()[res[res_positive_idx]].astype(int32)
                result[self.observations_mapping[submodel]] = restmp
        return result

    def simulate_submodel(self, data, coefficients, submodel=0):
        result = self.upc_sequence.run(data, coefficients, resources=self.run_config)
        if self.compute_demand_flag:
            self.compute_demand(submodel)
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
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)

        self.procedure=procedure
        if self.procedure == None:
            self.procedure = self.estimate_config.get("estimation", None)
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

        estimation_set = DatasetSubset(agent_set, agents_index)

        self.set_choice_set_size() #<-- determines size of choiceset - 28 may 09, mm 
        nchoices = self.get_choice_set_size()

        estimation_size_agents = estimate_config.get("estimation_size_agents", None) # should be a proportion of the agent_set
        if estimation_size_agents == None:
            estimation_size_agents = 1.0
        else:
            estimation_size_agents = max(min(estimation_size_agents,1.0),0.0) # between 0 and 1

        if estimation_size_agents < 1.0:
            self.debug.print_debug("Sampling agents for estimation ...",3)
            agents_for_estimation_idx = sample_noreplace(arange(estimation_set.size()),
                                                         int(estimation_set.size()*estimation_size_agents))
        else:
            agents_for_estimation_idx = arange(estimation_set.size())

        if agents_index is not None:
            agents_for_estimation_idx = agents_index[agents_for_estimation_idx]

        self.debug.print_debug("Number of agents for estimation: " + str(agents_for_estimation_idx.size),2)
        if agents_for_estimation_idx.size <= 0:
            self.debug.print_debug("Nothing to be done.",4)
            return None

        submodels = specification.get_distinct_submodels() #<-- determines # of submodels - 28 may 09, mm 
        self.get_status_for_gui().update_pieces_using_submodels(submodels=submodels, leave_pieces=2)
        self.map_agents_to_submodels(submodels, self.submodel_string, agent_set,
                                      agents_for_estimation_idx,
                                      dataset_pool = self.dataset_pool,
                                      resources = Resources({"debug": self.debug}))
                
        index, self.selected_choice = \
            self.get_choice_index_for_estimation_and_selected_choice(agent_set,
                        agents_for_estimation_idx, estimation_set, submodels)

#        self.debug.print_debug("Choice set size: " + str(nchoices),2)

        # create interaction set
        self.model_interaction.create_interaction_datasets(agents_for_estimation_idx, {0: index})
        
        self.estimate_config.merge({"index":index})
        self.coefficients = create_coefficient_from_specification(specification)
        self.model_interaction.create_specified_coefficients(self.coefficients, specification, self.choice_set.get_id_attribute()[index])        
        #run estimation
        result = self.estimate_step()
        del self.estimate_config["selected_choice"]
        del self.estimate_config["index"]
        return (self.coefficients, result)

    def estimate_step(self):
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        self.model_interaction.compute_variables()
        coef = {}
        result = {}
        index = self.estimate_config["index"]
        self.debug.print_debug("Estimate ...",4)
        for submodel in self.model_interaction.get_submodels():
            logger.log_status("submodel: %s" % submodel)
            self.increment_current_status_piece()
            self.model_interaction.prepare_data_for_estimation(submodel)
            coef[submodel] = self.model_interaction.get_submodel_coefficients(submodel)            
            self.coefficient_names[submodel] = self.model_interaction.get_coefficient_names(submodel)
            if self.model_interaction.is_there_data(submodel):   # observations for this submodel available
                if index <> None:
                    self.estimate_config["index"] = take (index, indices=self.observations_mapping[submodel], axis=0)
                # remove not used choices
                is_submodel_selected_choice = self.model_interaction.get_selected_choice_for_submodel_and_update_data(submodel)
                self.estimate_config["selected_choice"] = is_submodel_selected_choice
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
                    self.export_estimation_data(submodel, is_submodel_selected_choice, self.get_all_data(submodel),
                                                coef[submodel].get_coefficient_names_from_alt(),
                                                self.estimate_config["estimation_data_file_name"],
                                                self.estimate_config["use_biogeme_data_format"])

            self.coefficients.fill_coefficients(coef)
            self.estimate_config["coefficient_names"]=None
            self.estimate_config["variable_names"]=None
        return result

    def estimate_submodel(self, data, submodel=0):
        if self.model_interaction.is_there_data(submodel):
            return self.procedure.run(data, upc_sequence=self.upc_sequence, resources=self.estimate_config)
        return {}
        
    def export_estimation_data(self, submodel, is_selected_choice, data, coef_names, file_name, use_biogeme_data_format=False):
        from numpy import concatenate, newaxis, reshape
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
                    is_selected_choice[i,:] = is_selected_choice[i,:][iid[i,:,0]]

                coef_names = coef_names + ['stratum', 'sampling_prob']
                nvars += 2
                logger.log_status("added variables specific to stratified sampler")
            except:
                pass

            selected_choice = where(is_selected_choice)[1] + 1
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

            data_for_biogeme[:, 0] = selected_choice
            ids = reshape(arange(nobs)+1, (nobs,1))
            data_for_biogeme = concatenate((ids, data_for_biogeme),axis=1)
            data = data_for_biogeme

            header = ['ID', 'choice'] + biogeme_var_names
            nrows, ncols = data.shape
        else:
            nobs, alts, nvars = data.shape
            ids = reshape(arange(nobs)+1, (nobs,1,1))
            data = concatenate((ids, is_selected_choice[...,newaxis], data),axis=2)
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

    def get_agents_order(self, agents):
        return permutation(agents.size())

    def set_choice_set_size(self):
        self.choice_set_size = self.choice_set.size()
        
    def get_choice_set_size(self):
        return self.choice_set_size

    def get_choice_index(self, agent_set=None, agents_index=None, agent_subset=None):
        return None

    def get_choice_index_for_estimation_and_selected_choice(self, agent_set=None,
                                                            agents_index=None, agent_subset=None,
                                                            submodels=[1]):
        """ Return tuple of index of choices to be considered for each agent that will be passed
        to the interaction, and index of selected choices (within the whole choice_set).
        """
        self.model_interaction.set_selected_choice(agents_index)
        selected_choice = self.model_interaction.get_selected_choice()
        return (None, selected_choice)

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

    def get_data_as_dataset(self, submodel=-2):
        """Like get_all_data, but the retuning value is a InteractionDataset containing attributes that
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
    """ This class handles all the work that involves the interaction dataset of the Choice model. It supports
    hierarchical models, i.e. when there are more choice sets."""
    def __init__(self, model, package=None, choice_sets = []):
        self.interaction_package = package
        self.choice_sets = {}
        for i in range(len(choice_sets)):
            set = choice_sets[i]
            if (set is not None):
                if isinstance(set, str): # can be a dataset name
                    set = model.dataset_pool.get_dataset(set)
                self.choice_sets[i] = set
        self.number_of_choice_sets = len(self.choice_sets.keys())
        self.interaction_modules = {}
        self.interaction_class_names = {}
        self.interaction_datasets = {}
        self.model = model
        self.interaction_resources = None
        self.data = {}
        self.specified_coefficients = {}
        self.selected_choice = {}
        self.submodel_coefficients = {}
        
    def set_agent_set(self, agent_set):
        self.agent_set = agent_set
        factory = DatasetFactory()
        for i in range(self.number_of_choice_sets):
            self.interaction_modules[i], self.interaction_class_names[i] = \
                factory.compose_interaction_dataset_name(self.agent_set.get_dataset_name(),
                                                         self.choice_sets[i].get_dataset_name())

    def create_interaction_datasets(self, agents_index, choice_set_index):
        # free memory of existing interaction sets
        for i in self.interaction_datasets.keys():
            if isinstance(self.interaction_datasets[i], InteractionDataset):
                self.interaction_datasets[i].unload_all_attributes()
                gc.collect()
                
        self.interaction_resources = Resources({"debug":self.model.debug})
        for i in range(self.number_of_choice_sets):
            index = choice_set_index.get(i, None)
            try:
                self.interaction_datasets[i] = ClassFactory().get_class(
                                self.interaction_package+"."+self.interaction_modules[i],
                                class_name=self.interaction_class_names[i],
                                    arguments={"dataset1":self.agent_set, "dataset2":self.choice_sets[i],
                                               "index1":agents_index, "index2":index})
            except ImportError:
                self.interaction_datasets[i] = InteractionDataset(dataset1=self.agent_set, dataset2=self.choice_sets[i],
                                              index1=agents_index, index2=index, debug=self.model.debug)

    def compute_variables(self, variables=None):
        for i in range(self.number_of_choice_sets):
            if variables is not None:
                if self.number_of_choice_sets == 1:
                    var_list_for_this_choice_set = variables
                else:
                    var_list_for_this_choice_set = []
                    for var in variables: # choose variables for this choice set
                        dataset_name = var.get_dataset_name()
                        if (dataset_name == self.interaction_datasets[i].get_dataset_name()) or \
                            (self.interaction_datasets[i].get_owner_dataset_and_index(dataset_name)[0] is not None):
                            var_list_for_this_choice_set.append(var)
            else:
                var_list_for_this_choice_set = \
                        self.specified_coefficients[i].get_variables_without_constants_and_reserved_names()
            self.interaction_datasets[i].compute_variables(var_list_for_this_choice_set,
                                                           dataset_pool=self.model.dataset_pool,
                                                           resources = self.interaction_resources)

    def prepare_data_for_simulation(self, submodel):
        # free up memory from previous chunks
        if submodel in self.data.keys():
            del self.data[submodel]
            gc.collect()
            
        self.data[submodel] = {}
        self.submodel_coefficients[submodel] = {}
        for i in range(self.number_of_choice_sets):
            self.submodel_coefficients[submodel][i] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients[i], 
                                                                                        submodel)
            self.data[submodel][i] = self.interaction_datasets[i].create_logit_data(self.submodel_coefficients[submodel][i], 
                                                                            index = self.model.observations_mapping[submodel])

    def prepare_data_for_estimation(self, submodel):
        self.data[submodel] = {}
        self.submodel_coefficients[submodel] = {}
        for i in range(self.number_of_choice_sets):
            self.submodel_coefficients[submodel][i] = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients[i], 
                                                                                        submodel)
            self.data[submodel][i] = self.interaction_datasets[i].create_logit_data_from_beta_alt(
                                                                      self.submodel_coefficients[submodel][i], 
                                                                      index=self.model.observations_mapping[submodel])

            
    def get_submodel_coefficients(self, submodel):
        if self.number_of_choice_sets == 1:
            return self.submodel_coefficients[submodel][0]
        return self.submodel_coefficients[submodel]
        
    def remove_rows_from_data(self, where_not_remove, submodel, idx):
        self.data[submodel][idx] = compress(where_not_remove, self.data[submodel][idx], axis=0)
        
    def get_data(self, submodel):
        if self.number_of_choice_sets == 1:
            return self.data[submodel][0]
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
        for i in range(self.number_of_choice_sets):
            if i == 0:
                nchoices = self.model.get_choice_set_size()
            else:
                nchoices = self.choice_sets[i].size()
            self.specified_coefficients[i] = SpecifiedCoefficients().create(coefficients, specification, neqs=nchoices, equation_ids=equation_ids)
            
    def get_specified_coefficients(self):
        if self.number_of_choice_sets == 1:
            return self.specified_coefficients[0]
        return self.specified_coefficients
    
    def get_submodels(self):
        return self.specified_coefficients[0].get_submodels()
        
    def set_selected_choice(self, agents_index):
        for i in range(self.number_of_choice_sets):
            self.selected_choice[i] = self.choice_sets[i].get_id_index(id=
                                        self.agent_set.get_attribute_by_index(self.choice_sets[i].get_id_name()[0],
                                        agents_index))
            
    def get_selected_choice(self):
        if self.number_of_choice_sets == 1:
            return self.selected_choice[0]
        return self.selected_choice
    
    def get_selected_choice_2d(self):
        selected_choice_2d = {}
        for i in range(self.number_of_choice_sets):
            selected_choice_2d[i] = zeros((self.selected_choice[i].size, self.specified_coefficients[i].nequations()), 
                                          dtype="int32")
            selected_choice_2d[i][arange(self.selected_choice[i].size), self.selected_choice[i]] = 1
        return selected_choice_2d

    def get_selected_choice_for_submodel_and_update_data(self, submodel):
        is_submodel_selected_choice = {}
        selected_choice_2d = self.get_selected_choice_2d()
        for i in range(self.number_of_choice_sets):           
            is_submodel_selected_choice[i] = take (selected_choice_2d[i], indices=self.model.observations_mapping[submodel],
                                                                                                axis=0)
            # remove not used choices
            is_submodel_selected_choice[i] = take (is_submodel_selected_choice[i], 
                                                   indices=self.submodel_coefficients[submodel][i].get_equations_index(), 
                                                   axis=1)
            sumchoice = is_submodel_selected_choice[i].sum(axis=1, dtype=int32)
            where_not_remove = where(sumchoice == 0, False, True)
            if False in where_not_remove:
                is_submodel_selected_choice[i] = compress(where_not_remove, is_submodel_selected_choice[i], axis=0)
                self.remove_rows_from_data(where_not_remove, submodel, i)

        if self.number_of_choice_sets == 1:
            return is_submodel_selected_choice[0]
        return is_submodel_selected_choice
    
    def get_coefficient_names(self, submodel):
        return self.submodel_coefficients[submodel][0].get_coefficient_names_from_alt()
        
    def get_variable_names(self, submodel):
        return self.submodel_coefficients[submodel][0].get_variable_names_from_alt()
        
    def get_coefficient_fixed_values(self, submodel):
        return self.specified_coefficients[0].specification.get_coefficient_fixed_values_for_submodel(submodel)
        
    def is_there_data(self, submodel):
        for i in range(self.number_of_choice_sets):
            if (self.data[submodel][i].shape[0] <= 0) or (self.data[submodel][i].size <= 0):
                return False
        return True
    
if __name__=="__main__":
    from opus_core.tests import opus_unittest
    from numpy import ma, alltrue
    from scipy.ndimage import sum as ndimage_sum
    from opus_core.tests.stochastic_test_case import StochasticTestCase
    from opus_core.simulation_state import SimulationState


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
             
        def test_estimate_cross_nested_logit(self):
            ## BUG: What is this test doing?
            """
            This is in an experimental mode, since nested logit is not implemented yet.
            100 households choose between 4 modes: bus, train, car, bike (1,2,3,4)
            There are 2 nests: public = {bus, train}, private = {car, bike}
            """
            storage = StorageFactory().get_storage('dict_storage')

            household_data = {
                'household_id': arange(100)+1,
                't_public': array(30*[10]+30*[20]+30*[25]+10*[30]),
                't_private': array(30*[20]+30*[10]+30*[25]+10*[10]),
                'mode_id': array(30*[1] + 30*[4] + 15*[2] + 15*[3] + 10*[3], dtype="int32"),
                'nest_id': array(30*[1] + 30*[2] + 15*[1] + 15*[2] + 10*[2], dtype="int32"),
                'has_car': array(30*[1]+30*[0]+30*[1]+10*[0], dtype="bool8"),
                'dist_to_train': array(30*[100]+30*[50]+30*[10]+10*[70])
                }

            storage.write_table(table_name='households', table_data=household_data)
            storage.write_table(table_name='modes',
                table_data={"mode_id": arange(1,5), "nest_id": array([1,1,2,2])}
                )
            storage.write_table(table_name='nests',
                table_data = {"nest_id": array([1,2])}
                )

            # create datasets
            households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id",
                                 dataset_name="household")
            modes = Dataset(in_storage=storage, in_table_name='modes', id_name="mode_id",
                                 dataset_name="mode")
            nests = Dataset(in_storage=storage, in_table_name='nests', id_name="nest_id",
                                 dataset_name="nest")

            specification = EquationSpecification(variables=("household.t_public", "household.t_private", "__lambda",
                                                             "household.dist_to_train", "__alpha",
                                                             "household.has_car", "__alpha"),
                                                  coefficients=( "tpub", "tpriv", "l", "dtt", "a1", "hc", "a2"),
                                                  other_fields={"dim_nest_id": array([0, 0, 0, 1, 1, 2, 2])})

            cm = ChoiceModel(choice_set=modes, choices = "opus_core.random_choices", upper_level_choice_set=nests)
#            coef, dummy = cm.estimate(specification, agent_set = households,
#                                       procedure="opus_core.bhhh_cnl_two_levels_estimation", debuglevel=4)

    opus_unittest.main()
