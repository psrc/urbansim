# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.models.location_choice_model import LocationChoiceModel
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import probsample_noreplace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from numpy import where, arange, concatenate, array, ndarray, zeros, resize
from opus_core.resources import Resources
from opus_core.misc import unique_values
from numpy import ma
from opus_core.logger import logger

class AgentLocationChoiceModel(LocationChoiceModel):
    """Similar to the LocationChoiceModel. In addition, after a run it checks
    for over-filled locations and in case of collisions, it runs itself again.
    """

    def __init__(self, location_set, model_name, short_name,
                        sampler="opus_core.samplers.weighted_sampler", utilities="opus_core.linear_utilities",
                        probabilities="opus_core.mnl_probabilities", choices="opus_core.random_choices",
                        filter=None, submodel_string=None, location_id_string = None,
                        run_config=None, estimate_config=None, debuglevel=0, dataset_pool=None,
                        variable_package = "urbansim"):
        self.model_name = model_name
        self.model_short_name = short_name
        if (run_config is not None) and not isinstance(run_config, Resources):
            run_config = Resources(run_config)
        if (estimate_config is not None) and not isinstance(estimate_config, Resources):
            estimate_config = Resources(estimate_config)
        self.add_prefix_to_variable_names(["capacity_string", "number_of_agents_string", "number_of_units_string"],
                                           location_set, variable_package, run_config)
        self.add_prefix_to_variable_names("weights_for_estimation_string",
                                           location_set, variable_package, estimate_config)

        LocationChoiceModel.__init__(self, location_set=location_set, sampler=sampler, utilities=utilities,
                        probabilities=probabilities, choices=choices,
                        filter=filter,
                        submodel_string=submodel_string, location_id_string=location_id_string,
                        run_config=run_config, estimate_config=estimate_config,
                        debuglevel=debuglevel, dataset_pool=dataset_pool)

    def run(self, specification, coefficients, agent_set,
            agents_index=None, agents_filter=None,
            chunk_specification=None, data_objects=None,
            run_config=None, debuglevel=0, maximum_runs=10):

        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        if agents_index is None:
            if agents_filter is not None:
                agent_set.compute_variables(agents_filter, dataset_pool=self.dataset_pool)
                agents_index = where(agent_set.get_attribute(VariableName(agents_filter).get_alias()))[0]
            else:
                agents_index = arange(agent_set.size())
        if not isinstance(agents_index, ndarray):
            try:
                agents_index = array(agents_index)
            except:
                raise TypeError, "Argument agents_index is of wrong type (numpy array or list allowed.)"

        if agents_index.size <= 0:
            logger.log_status("Nothing to be done.")
            return array([], dtype='int32')

        if run_config == None:
            run_config = Resources()
        self.run_config = run_config.merge_with_defaults(self.run_config)
        self.number_of_units_string = self.run_config.get("number_of_units_string", None)
        self.number_of_agents_string = self.run_config.get(
                        "number_of_agents_string",
                        "%s.number_of_agents(%s)" % (self.choice_set.get_dataset_name(), agent_set.get_dataset_name()))
            
        if self.number_of_units_string is None:
            maximum_runs = 1
        unplaced = arange(agents_index.size)
        id_name = self.choice_set.get_id_name()[0]
        for run in range(maximum_runs):
            unplaced_size_before_model = unplaced.size
            choices = LocationChoiceModel.run(self, specification, coefficients, agent_set,
                    agents_index[unplaced], chunk_specification, debuglevel=debuglevel)
            if run == 0:
                all_choices=choices
            else:
                all_choices[unplaced]=choices
            unplaced = self.get_movers_from_overfilled_locations(agent_set, agents_index)
            if (unplaced.size <= 0) or (unplaced_size_before_model == unplaced.size) or (unplaced.size == (unplaced_size_before_model - self.observations_mapping['mapped_index'].size)):
                break
            agent_set.set_values_of_one_attribute(id_name, -1, agents_index[unplaced])
        return all_choices

    def run_chunk(self, agents_index, agent_set, specification, coefficients):
        result = LocationChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)
        return result

    def simulate_submodel(self, data, coefficients, submodel):
        """Keeps agent's probabilities."""
        result = LocationChoiceModel.simulate_submodel(self, data, coefficients, submodel)
        return result

    def get_movers_from_overfilled_locations(self, agent_set, agents_index):
        """Returns an index (relative to agents_index) of agents that should be removed from their locations.
        """
        agents_locations = agent_set.get_attribute_by_index(
                self.choice_set.get_id_name()[0], agents_index)
        # check if there was an overfilling of locations
        movers = array([], dtype='int32')

        if self.compute_capacity_flag:
            new_locations_vacancy = self.get_locations_vacancy(agent_set)
            movers = self.choose_agents_to_move_from_overfilled_locations(new_locations_vacancy,
                                                        agent_set, agents_index, agents_locations)
        return concatenate((movers, where(agents_locations <= 0)[0]))

    def get_locations_vacancy(self, agent_set):
        if (self.number_of_units_string is not None) and (self.number_of_agents_string is not None):
            self.dataset_pool.add_datasets_if_not_included({agent_set.get_dataset_name():agent_set})
            self.choice_set.compute_variables([self.number_of_agents_string, self.number_of_units_string],
                                      dataset_pool=self.dataset_pool)
            number_of_agents = self.choice_set.get_attribute(self.number_of_agents_string)
            number_of_units = self.choice_set.get_attribute(self.number_of_units_string)
            return number_of_units - number_of_agents
        return None
        
        
    def choose_agents_to_move_from_overfilled_locations(self, capacity,
                                                        agent_set, agents_index, agents_locations):
        """Iterates over locations that are overfilled and selects randomly agents placed in those locations
        to be removed."""
        if capacity is None:
            return array([], dtype='int32')
        index_valid_agents_locations = where(agents_locations > 0)[0]
        valid_agents_locations = agents_locations[index_valid_agents_locations]
        index_consider_capacity = unique_values(self.choice_set.get_id_index(valid_agents_locations))
        capacity_of_affected_locations = capacity[index_consider_capacity]
        overfilled = where(capacity_of_affected_locations < 0)[0]
        movers = array([], dtype='int32')
        choice_ids = self.choice_set.get_id_attribute()
        for loc in overfilled:
            agents_to_move = where(valid_agents_locations == choice_ids[index_consider_capacity[loc]])[0]
            if agents_to_move.size > 0:
                n = int(-1*capacity_of_affected_locations[loc])
                sampled_agents = probsample_noreplace(index_valid_agents_locations[agents_to_move], 
                                                      min(n, agents_to_move.size))
                movers = concatenate((movers, sampled_agents))
        return movers

    def add_prefix_to_variable_names(self, variable_names, dataset, variable_package, resources):
        """Add a prefix of 'package.dataset_name.' to variable_names from resources.
        """
        if not isinstance(variable_names, list):
            variable_names = [variable_names]
        for variable_name in variable_names:
            variable_string = resources.get(variable_name, None)
            if variable_string is not None:
                variable_string_name = VariableName(variable_string)
                if (variable_string_name.get_dataset_name() == None) and \
                            (variable_string_name.get_autogen_class() is None) :
                    add_string = ""
                    if variable_string_name.get_package_name() == None:
                        add_string = "%s." % variable_package
                    add_string = add_string + dataset.get_dataset_name() + "."
                    resources.merge({
                        variable_name:add_string+variable_string})

    def get_choice_index_for_estimation_and_selected_choice(self, agent_set,
                                                            agents_index, *args, **kwargs):
        id_name = self.choice_set.get_id_name()[0]
        mod_id_name = "__%s__" % id_name
        # This should be only true when reestimating, since the agents for estimation were unplaced
        # in the previous run and their original locations were stored in mod_id_name
        if mod_id_name in agent_set.get_known_attribute_names():
            agent_set.set_values_of_one_attribute(id_name, agent_set.get_attribute(mod_id_name))
        result = LocationChoiceModel.get_choice_index_for_estimation_and_selected_choice(self, agent_set,
                                                            agents_index, *args, **kwargs)
        #logger.log_status("Unplace agents for estimation.")
        # Copy the agents locations into a temporary attribute (called e.g. __grid_id__)
        # in case it will be needed for reestimation
        #if  (mod_id_name not in agent_set.get_known_attribute_names()):
        #    agent_set.add_attribute(name=mod_id_name, data=array(agent_set.get_attribute(id_name))) # must be a copy
        # Agents for estimation are unplaced in order not to influence the location characteristics
        #agent_set.set_values_of_one_attribute(id_name,resize(array([-1.0]), agents_index.size), agents_index)
        return result

    def prepare_for_run(self, *args, **kwargs):
        spec, coef, dummy = LocationChoiceModel.prepare_for_run(self, *args, **kwargs)
        return (spec, coef)
    
    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None, agent_set=None, 
                              agents_for_estimation_storage=None,
                              agents_for_estimation_table=None, join_datasets=False,
                              index_to_unplace=None, portion_to_unplace=1.0,
                              compute_lambda=False, grouping_location_set=None,
                              movers_variable=None, movers_index=None,
                              filter=None, location_id_variable=None,
                              data_objects={}):
        """Put 'location_id_variable' always in, if the location id is to be computed on the estimation set,
        i.e. if it is not a primary attribute of the estimation set. Set 'index_to_unplace' to None, if 'compute_lambda' is True.
        In such a case, the annual supply is estimated without unplacing agents. 'grouping_location_set', 'movers_variable' and
        'movers_index' must be given, if 'compute_lambda' is True.
        """
        from opus_core.model import get_specification_for_estimation
        from urbansim.functions import compute_supply_and_add_to_location_set
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        if (agent_set is not None) and (index_to_unplace is not None):
            if self.location_id_string is not None:
                agent_set.compute_variables(self.location_id_string, resources=Resources(data_objects))
            if portion_to_unplace < 1:
                unplace_size = int(portion_to_unplace*index_to_unplace.size)
                end_index_to_unplace = sample_noreplace(index_to_unplace, unplace_size)
            else:
                end_index_to_unplace = index_to_unplace
            logger.log_status("Unplace " + str(end_index_to_unplace.size) + " agents.")
            agent_set.modify_attribute(self.choice_set.get_id_name()[0],
                                        resize(array([-1]), end_index_to_unplace.size), end_index_to_unplace)
        if compute_lambda:
            movers = zeros(agent_set.size(), dtype="bool8")
            if movers_index is not None:
                movers[movers_index] = 1
            agent_set.add_primary_attribute(movers, "potential_movers")
            self.estimate_config["weights_for_estimation_string"] = self.estimate_config["weights_for_estimation_string"]+"_from_lambda"
            compute_supply_and_add_to_location_set(self.choice_set, grouping_location_set,
                                                   self.run_config["number_of_units_string"],
                                                   self.run_config["capacity_string"],
                                                   movers_variable,
                                                   self.estimate_config["weights_for_estimation_string"],
                                                   resources=Resources(data_objects))

        # create agents for estimation
        if (agents_for_estimation_storage is not None) and (agents_for_estimation_table is not None):
            estimation_set = Dataset(in_storage = agents_for_estimation_storage,
                                      in_table_name=agents_for_estimation_table,
                                      id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
            if location_id_variable is not None:
                estimation_set.compute_variables(location_id_variable, resources=Resources(data_objects))
                # needs to be a primary attribute because of the join method below
                estimation_set.add_primary_attribute(estimation_set.get_attribute(location_id_variable), VariableName(location_id_variable).get_alias())
            if filter:
                values = estimation_set.compute_variables(filter, resources=Resources(data_objects))
                index = where(values > 0)[0]
                estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)

            if join_datasets:
                agent_set.join_by_rows(estimation_set, require_all_attributes=False,
                                    change_ids_if_not_unique=True)
                index = arange(agent_set.size()-estimation_set.size(),agent_set.size())
            else:
                index = agent_set.get_id_index(estimation_set.get_id_attribute())
        else:
            if agent_set is not None:
                if filter is not None:
                    values = agent_set.compute_variables(filter, resources=Resources(data_objects))
                    index = where(values > 0)[0]
                else:
                    index = arange(agent_set.size())
            else:
                index = None
        return (specification, index)



### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_location_choice_model.