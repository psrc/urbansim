# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.chunk_specification import ChunkSpecification
from numpy import zeros, array, arange, ones, float32, concatenate, where
from numpy import int8, take, put, greater, resize
from scipy import ndimage
from numpy.random import permutation
from numpy import ma
from opus_core.sampler_factory import SamplerFactory
from opus_core.choice_model import ChoiceModel
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from opus_core.opus_error import OpusError

class LocationChoiceModel(ChoiceModel):
    """
        LCM is associated with a location_set (Dataset) and a upc_sequence. Method 'run' runs a simulation for a given agent_set,
        where agents choose locations among locations. Locations can be sampled for each agent using given sampling procedure.
        Method 'estimate' runs an estimation process.
    """
    model_name = "Location Choice Model"
    model_short_name = "LCM"

    def __init__(self, location_set, sampler="opus_core.samplers.weighted_sampler",
                        utilities="opus_core.linear_utilities",
                        probabilities="opus_core.mnl_probabilities",
                        choices="opus_core.random_choices",
                        interaction_pkg="urbansim.datasets",
                        filter=None, submodel_string=None,
                        location_id_string = None,
                        run_config=None, estimate_config=None,
                        debuglevel=0, dataset_pool=None, **kwargs):
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
        ChoiceModel.__init__(self, choice_set=location_set, utilities=utilities,
                        probabilities=probabilities, choices=choices, sampler=sampler,
                        submodel_string=submodel_string,
                        interaction_pkg=interaction_pkg,
                        run_config=run_config, estimate_config=estimate_config,
                        debuglevel=debuglevel, dataset_pool=dataset_pool, **kwargs)
        self.model_interaction = ModelInteractionLCM(self, interaction_pkg, [self.choice_set])
        self.filter = filter
        self.location_id_string = location_id_string
        if self.location_id_string is not None:
            self.location_id_string = VariableName(self.location_id_string)
            #self.location_id_string.set_alias(location_set.get_id_name()[0])

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
        self.dataset_pool.add_datasets_if_not_included({agent_set.get_dataset_name():agent_set})
        
        if self.location_id_string is not None:
            agent_set.compute_variables(self.location_id_string, dataset_pool=self.dataset_pool)
        if self.run_config.get("agent_units_string", None): # used when agents take different amount of capacity from the total capacity
            agent_set.compute_variables([self.run_config["agent_units_string"]], dataset_pool=self.dataset_pool)

        self.compute_capacity_flag = self.run_config.get("compute_capacity_flag",  False)
        self.capacity_string = None
        if self.compute_capacity_flag:
            try:
                self.capacity_string = self.run_config["capacity_string"]
            except:
                raise KeyError, \
                    "Entry 'capacity_string' has to be specified in 'run_config' if 'compute_capacity_flag' is True"
        return ChoiceModel.run(self,specification, coefficients, agent_set,
                agents_index=agents_index, chunk_specification=chunk_specification, run_config=run_config,
                debuglevel=debuglevel)


    def run_chunk(self, agents_index, agent_set, specification, coefficients):

        # move movers out
        id_name = self.choice_set.get_id_name()[0]
        if  (id_name not in agent_set.get_known_attribute_names()):
            agent_set.add_attribute(name=id_name, data=resize(array([-1]), agent_set.size()))
        else:
            agent_set.set_values_of_one_attribute(id_name,resize(array([-1]), agents_index.size), agents_index)

        self.capacity = None
        if self.compute_capacity_flag:
            self.capacity = ma.filled(self.determine_units_capacity(agent_set, agents_index), 0.0)
            if self.capacity is not None:
                logger.log_status("Available capacity: %s units." % self.capacity.sum())
        self.run_config.merge({"capacity":self.capacity})
        if self.run_config.get("agent_units_string", None):
            self.run_config["agent_units_all"] = agent_set.get_attribute_by_index(self.run_config["agent_units_string"], agents_index)

        choices = ChoiceModel.run_chunk(self,agents_index, agent_set, specification, coefficients)

        #modify locations
        agent_set.set_values_of_one_attribute(id_name, choices, agents_index)
        self.run_config["capacity"] = None
        return choices

    def simulate_submodel(self, data, coefficients, submodel):
        if self.run_config.get("agent_units_all", None) is not None:
            self.run_config["agent_units"] = self.run_config["agent_units_all"][self.observations_mapping[submodel]]

        return ChoiceModel.simulate_submodel(self, data, coefficients, submodel)

    def get_demand_for_submodel(self, submodel=0):
        """Return aggregated probabilities for each location for the submodel."""
        probs = self.upc_sequence.get_probabilities()
        demand = ndimage.sum(probs.ravel().astype("float32"), labels=self.run_config["index"].ravel()+1,
                             index=arange(self.choice_set.size())+1)
        return demand


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

        if estimate_config == None:
            estimate_config = Resources()
        self.estimate_config = estimate_config.merge_with_defaults(self.estimate_config)
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if self.location_id_string is not None:
            agent_set.compute_variables(self.location_id_string, dataset_pool=self.dataset_pool)

        self.compute_capacity_flag_for_estimation = self.estimate_config.get(
                                                "compute_capacity_flag", False)
        self.capacity_string_for_estimation = None
        if self.compute_capacity_flag_for_estimation:
            try:
                self.capacity_string_for_estimation = self.estimate_config["capacity_string"]
            except:
                raise KeyError, \
                    "Entry 'capacity_string' has to be specified in 'estimate_config' if 'compute_capacity_flag' is True"
        self.capacity_for_estimation = None
        if self.compute_capacity_flag_for_estimation:
            self.capacity_for_estimation = ma.filled(self.determine_units_capacity_for_estimation(
                                                        agent_set, agents_index), 0.0)
        self.estimate_config.merge({"capacity":self.capacity_for_estimation})
        return ChoiceModel.estimate(self,specification, agent_set,
                agents_index, procedure, estimate_config=estimate_config, debuglevel=debuglevel)

    def determine_units_capacity(self, agent_set, agents_index):
        """Return capacity for each location.
        """
        if self.capacity_string is None:
            return None
        
        capacity = self.choice_set.compute_variables(self.capacity_string, dataset_pool=self.dataset_pool)
        return capacity

    def determine_units_capacity_for_estimation(self, agent_set, agents_index):
        try:
            self.choice_set.compute_variables(self.capacity_string_for_estimation, dataset_pool=self.dataset_pool)
            return self.choice_set.get_attribute(self.capacity_string_for_estimation)
        except:
            logger.log_warning("Computing capacity for estimation failed (%s)" % self.capacity_string_for_estimation)
        return None


    def get_weights_for_sampling_locations(self, agent_set=None, agents_index=None):
        """Return a tuple where the first element is as array of weights and the second is an index of locations which
        the weight array corresponds to. The array of weights can be a 2D array (if weights are agent specific).
        Weights can be determined by a variable name given in 'weights_for_simulation_string' in run_config. 
        If it is not given, it is assumed that weights are proportional to the capacity. If it is the equal sign (i.e. '='),
        all weights are equal.
        """
        weight_string = self.run_config.get("weights_for_simulation_string", None)
        if weight_string is None:
            return (self.capacity, None)
        if weight_string == '=':
            return (ones(self.choice_set.size()), None)
        self.choice_set.compute_variables([weight_string], dataset_pool=self.dataset_pool)
        weight_name = VariableName(weight_string)
        return (self.choice_set.get_attribute(weight_name.get_alias()), None)
    
    def get_weights_for_sampling_locations_for_estimation (self, agent_set=None, agents_index=None):
        weight_string = self.estimate_config.get("weights_for_estimation_string", None)
        if weight_string == None:
            return (None, None)
        self.choice_set.compute_variables([weight_string], dataset_pool=self.dataset_pool)
        weight_name = VariableName(weight_string)
        return (self.choice_set.get_attribute(weight_name.get_alias()), None)

    def get_agents_order(self, movers):
        return permutation(movers.size())

    def set_choice_set_size(self):
        """If "sample_size_locations" is specified in run_config, it is considered as the choice set size. Otherwise
        the value of resources entry "sample_proportion_locations" is considered as determining the proportion of
        all locations to be the choice set size.
        """
        if self.sampler_class is not None:
            pchoices =     self.run_config.get("sample_proportion_locations", None)
            nchoices =     self.run_config.get("sample_size_locations", None)
            if nchoices == None:
                if pchoices == None:
                    logger.log_warning("Neither 'sample_proportion_locations' nor 'sample_size_locations' " +
                                       "given. Locations will not be sampled.")
                    nchoices = self.choice_set.size()
                else:
                    nchoices = int(pchoices*self.choice_set.size())
        else:
            nchoices = self.choice_set.size()
        self.choice_set_size =  min(nchoices, self.choice_set.size())

    def get_choice_index(self, agent_set, agents_index, agent_subset):
        self.weights = None
        nchoices = self.get_number_of_elemental_alternatives()
        if (nchoices == self.choice_set.size()) and (self.filter is None):
            return None            
        self.weights, location_index = self.get_weights_for_sampling_locations(agent_set, agents_index)
        self.weights = self.apply_filter(self.filter, self.weights, agent_set, agents_index)
        if (nchoices == self.choice_set.size()): # take all alternatives that pass through the filter and have eights larger than 0
            index = where(self.weights > 0)[0]
            self.choice_set_size = index.size # modify the choice set size
            index = resize(index, (agents_index.size, self.choice_set_size))
            return index
        self.debug.print_debug("Sampling locations ...",3)
        # the following model component must return a 2D array of sampled locations per agent
        try:
            index, chosen_choice = self.sampler_class.run(agent_subset, self.choice_set, index2=location_index, sample_size=nchoices,
                weight=self.weights, resources=self.run_config)
        except Exception, e:
            logger.log_warning("Problem with sampling alternatives.\n%s" % e)
            index = None
        if index == None: # sampler produced an error
            index = array([], dtype="int32")
        return index

    def get_choice_index_for_estimation_and_selected_choice(self, agent_set,
                                                            agents_index, agent_subset=None, submodels=[1]):
        """Performs sampling if required. It can be done in several chunks, which is useful especially if the sampling weights
        is a 2D array. The chunking is controlled by an entry 'chunk_specification_for_estimation' in estimate_config.
        The method returns a tuple with a 2D index (for each agent in index of sampled choices) and an array of indices
        of selected choices.
        """
        ### TODO: This needs to be rewritten as part of the ModelInteraction class. 
        self.model_interaction.set_selected_choice(agents_index)
        selected_choice = self.model_interaction.get_selected_choice()
        self.weights = None
        nchoices = self.get_number_of_elemental_alternatives()
        if nchoices < self.choice_set.size():
            chunk_specification = self.estimate_config.get("chunk_specification_for_estimation", ChunkSpecification({"nchunks":1}))
            logger.log_status("Sampling locations for estimation ...")
            index = zeros((agents_index.size, nchoices), dtype='int32')
            selected_choice = zeros((agents_index.size,), dtype='int32')
            if (len(submodels) > 1) or ((len(submodels) > 0) and (self.observations_mapping[submodels[0]].size < agents_index.size)):
                for submodel in submodels:
                    nagents_in_submodel = self.observations_mapping[submodel].size
                    if nagents_in_submodel <= 0:
                        continue
                    nchunks = chunk_specification.nchunks(self.observations_mapping[submodel])
                    chunksize = chunk_specification.chunk_size(self.observations_mapping[submodel])
                    logger.log_status("Submodel %s sampled in %s chunk(s)." % (submodel, nchunks))
                    for ichunk in range(nchunks):
                        this_agents_index = self.observations_mapping[submodel][(ichunk*chunksize):min(((ichunk+1)*chunksize),
                                                                                                       nagents_in_submodel)]
                        this_weights, location_index, index1, chosen_choice = self.apply_filter_on_weights_and_choose_choice(agent_set, agents_index[this_agents_index],
                                                                                                                             submodel, nchoices)
                        index[this_agents_index, :] = index1
                        selected_choice[this_agents_index] = chosen_choice.astype(selected_choice.dtype)
            else:
                if len(submodels) <= 0:
                    subm = -2
                else:
                    subm = submodels[0]
                nagents = agents_index.size
                nchunks = chunk_specification.nchunks(agents_index)
                chunksize = chunk_specification.chunk_size(agents_index)
                logger.log_status("Sampling done in %s chunk(s)." % nchunks)
                for ichunk in range(nchunks):
                    this_agents_index = arange((ichunk*chunksize),min(((ichunk+1)*chunksize),nagents))
                    this_weights, location_index, index1, chosen_choice = self.apply_filter_on_weights_and_choose_choice(agent_set, agents_index[this_agents_index],
                                                                                                                    subm, nchoices)
                    index[this_agents_index,:] = index1
                    selected_choice[this_agents_index] = chosen_choice
            self.model_interaction.set_selected_choice_for_LCM(selected_choice)
        else:
            index, selected_choice = ChoiceModel.get_choice_index_for_estimation_and_selected_choice(self,
                                        agent_set, agents_index, agent_subset,
                                        submodels=submodels)        
        return (index, selected_choice)

    def apply_filter_on_weights_and_choose_choice(self, agent_set, agents_index, submodel, nchoices):
        """ TODO: document me
        """
        ### TODO: self.weight must be transformed in a local variable
        self.weights, location_index = self.get_weights_for_sampling_locations_for_estimation(agent_set, agents_index)
        this_weights = self.apply_filter(self.filter, self.weights, agent_set, agents_index, submodel)
        index1, chosen_choice = self.sampler_class.run(agent_set, self.choice_set,
            index1=agents_index, index2=location_index, sample_size=nchoices,
            weight=this_weights, include_chosen_choice=True, resources=self.estimate_config)
        return (this_weights, location_index, index1, chosen_choice)


    def apply_filter(self, filter, weights, agent_set, agents_index, submodel=-2):
        """ Multiply given filter with weights. If filter is a dictionary, it choses the one for the given submodel.
        """
        if (filter == None) :
            if weights is not None:
                return weights
            else:
                return ones(self.choice_set.size(), dtype=int8)

        #if weights is None and filter is not None, apply filter with equal weights
        if (weights == None):
            weights = ones(self.choice_set.size())

        if isinstance(filter, dict):
            submodel_filter = filter[submodel]
        else:
            submodel_filter = filter
        if isinstance(submodel_filter, str):
            self.choice_set.compute_variables([submodel_filter], dataset_pool=self.dataset_pool)
            filter_name = VariableName(submodel_filter)
            my_filter = greater(self.choice_set.get_attribute(filter_name.get_alias()), 0)
        else:
            my_filter = greater(submodel_filter, 0)
        if weights.ndim <> my_filter.ndim:
            logger.log_warning("LCM: Mismatch in the rank of weights and filter. No filter applied.")
            return weights
        return weights*my_filter

    def plot_choice_histograms(self, capacity=None, main =""):
        if capacity is None:
            capacity = self.capacity_string
        if isinstance(capacity, str):
            capacity_values = self.choice_set.get_attribute(capacity)
        else:
            capacity_values = capacity
        self.upc_sequence.plot_choice_histograms(capacity=capacity_values, main=main)
        self.upc_sequence.show_plots()

from opus_core.choice_model import ModelInteraction
class ModelInteractionLCM(ModelInteraction):
    def set_selected_choice_for_LCM(self, selected_choice):
        self.selected_choice[0] = selected_choice