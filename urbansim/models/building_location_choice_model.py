# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import re
from opus_core.resources import Resources
from opus_core.chunk_specification import ChunkSpecification
from opus_core.datasets.dataset import DatasetSubset
from urbansim.models.agent_location_choice_model_member import AgentLocationChoiceModelMember
from urbansim.models.location_choice_model import LocationChoiceModel
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.datasets.building_dataset import BuildingCreator
from opus_core.misc import clip_to_zero_if_needed
from opus_core.misc import unique_values
from opus_core.variables.variable_name import VariableName
from opus_core.resources import merge_resources_with_defaults
from numpy import zeros, arange, where, ones, logical_and, int32
from numpy import take, argsort, array, sort, minimum, reshape, concatenate
from numpy import ma
from numpy.random import randint
from opus_core.logger import logger

class BuildingLocationChoiceModel(AgentLocationChoiceModelMember):


    def __init__(self, group_member, location_set,
            agents_grouping_attribute = 'building.building_type_id',
            sampler = "opus_core.samplers.weighted_sampler",
            utilities = "opus_core.linear_utilities",
            choices = "urbansim.first_agent_first_choices",
            probabilities = "opus_core.mnl_probabilities",
            estimation = "opus_core.bhhh_mnl_estimation",
            capacity_string = "is_developable_for_buildings_UNITS",
            estimation_weight_string = None,
            developable_maximum_unit_variable = "developable_maximum_buildings_UNITS",
            developable_minimum_unit_variable = "developable_minimum_UNITS", # None means don't consider any minimum. For default, set it to empty string
            number_of_agents_string = "buildings_SSS_space",
            number_of_units_string = "total_maximum_development_SSS",
            sample_proportion_locations = None,
            sample_size_locations = 30,
            estimation_size_agents = 1.0,
            compute_capacity_flag = True,
            filter = "developable_maximum_buildings_UNITS", # None doesn't use any filter
            submodel_string = "size_category_SSS", # Put here None, if no submodels should be used.
            nrecords_per_chunk_for_estimation_sampling = 1000, # put here None, if everything in 1 chunk
            location_id_string = None,
            run_config = None, estimate_config=None, debuglevel=0, dataset_pool=None, variable_package = "urbansim"):
        """ 'group_member' is of type ModelGroupMember.
        """
        group_member_name = group_member.get_member_name()
        units = group_member.get_attribute_value("units")[0]

        if capacity_string:
            capacity_string = re.sub("UNITS", units, capacity_string)
            capacity_string = re.sub("SSS", group_member_name, capacity_string)
        if filter:
            filter = re.sub("UNITS", units, filter)
            filter = re.sub("SSS", group_member_name, filter)
        if developable_maximum_unit_variable:
            developable_maximum_unit_variable = re.sub("UNITS", units, developable_maximum_unit_variable)
            developable_maximum_unit_variable = re.sub("SSS", group_member_name, developable_maximum_unit_variable)
        if developable_minimum_unit_variable == "":
            developable_minimum_unit_variable = "developable_minimum_%s" % units
        elif developable_minimum_unit_variable:
            developable_minimum_unit_variable = re.sub("UNITS", units, developable_minimum_unit_variable)
            developable_minimum_unit_variable = re.sub("SSS", group_member_name, developable_minimum_unit_variable)
        if submodel_string:
            submodel_string = re.sub("UNITS", units, submodel_string)
            submodel_string = re.sub("SSS", group_member_name, submodel_string)
        if number_of_agents_string:
            number_of_agents_string = re.sub('UNITS', units, number_of_agents_string)
            number_of_agents_string = re.sub('SSS', group_member_name, number_of_agents_string)
        if number_of_units_string:
            number_of_units_string = re.sub('UNITS', units, number_of_units_string)
            number_of_units_string = re.sub('SSS', group_member_name, number_of_units_string)

        # create full names from (possibly) short names
        tmpdict = Resources({"filter": filter, "max": developable_maximum_unit_variable,
                             "min": developable_minimum_unit_variable})
        self.add_prefix_to_variable_names(["filter", "max", "min"], location_set, variable_package, resources=tmpdict)
        filter = tmpdict["filter"]
        if tmpdict["max"]:
            self.developable_maximum_unit_variable = VariableName(tmpdict["max"])
        else:
            self.developable_maximum_unit_variable = None

        if tmpdict["min"]:
            self.developable_minimum_unit_variable = VariableName(tmpdict["min"])
        else:
            self.developable_minimum_unit_variable = None

        self.project_type = group_member_name
        self.units = units

        run_config = merge_resources_with_defaults(run_config, [
            ("sample_proportion_locations", sample_proportion_locations),
            ("sample_size_locations", sample_size_locations),
            ("compute_capacity_flag", compute_capacity_flag),
            ("capacity_string", capacity_string),
            ("agent_units_string", "urbansim.building.building_size"),
            ("number_of_agents_string", number_of_agents_string),
            ("number_of_units_string", number_of_units_string),
            ])
        estimate_config = merge_resources_with_defaults(estimate_config, [
                    ("estimation", estimation),
                    ("sample_proportion_locations", sample_proportion_locations),
                    ("sample_size_locations", sample_size_locations),
                    ("estimation_size_agents", estimation_size_agents),
                    ("weights_for_estimation_string", estimation_weight_string),
                    ("capacity_string", capacity_string),
                    ("compute_capacity_flag", compute_capacity_flag)])
        if nrecords_per_chunk_for_estimation_sampling:
            estimate_config["chunk_specification_for_estimation"] = ChunkSpecification({
                                             "records_per_chunk": nrecords_per_chunk_for_estimation_sampling})
        AgentLocationChoiceModelMember.__init__(self, group_member, location_set,
                                        agents_grouping_attribute,
                                        model_name = "Building Location Choice Model",
                                        short_name = "BLCM",
                                        sampler=sampler,
                                        utilities=utilities,
                                        probabilities=probabilities,
                                        choices=choices,
                                        filter=filter,
                                        submodel_string=submodel_string,
                                        location_id_string=location_id_string,
                                        run_config=run_config,
                                        estimate_config=estimate_config,
                                        debuglevel=debuglevel,
                                        dataset_pool=dataset_pool,
                                        variable_package=variable_package)


    def run(self, *args, **kargs):
        agent_set = kargs["agent_set"]
        run_config = kargs.get("run_config", {})
        self.units_full_name = "%s.%s.%s" % (run_config.get("agent_variables_package", "urbansim"),
                                             agent_set.get_dataset_name(), self.units)
        data_objects = kargs.get("data_objects",{})
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        agent_set.compute_variables(self.units_full_name, dataset_pool=self.dataset_pool)
        #logger.log_status("Buildings size: %d" % (agent_set.get_attribute_by_index(self.units_full_name).sum()))
        return AgentLocationChoiceModelMember.run(self, *args, **kargs)

    def get_sampling_weights(self, config, agent_set=None, agents_index=None, **kwargs):
        where_developable = AgentLocationChoiceModelMember.apply_filter(self, self.filter, None, agent_set,
                                                                        agents_index)
        if self.developable_maximum_unit_variable:
            varlist = [self.developable_maximum_unit_variable]
        else:
            varlist = []
        if self.developable_minimum_unit_variable is not None:
            varlist.append(self.developable_minimum_unit_variable)
        self.choice_set.compute_variables(varlist, dataset_pool = self.dataset_pool)
        if self.developable_maximum_unit_variable is not None:
            max_capacity = clip_to_zero_if_needed(self.choice_set.get_attribute_by_index(
                                 self.developable_maximum_unit_variable, where_developable),
                              "get_weights_for_sampling_locations - computing developable_maximum_unit_variable")
        else:
            max_capacity = ones(where_developable.size) * agent_set.get_attribute(self.units).max()

        if self.developable_minimum_unit_variable is not None:
            min_capacity = clip_to_zero_if_needed(self.choice_set.get_attribute_by_index(
                             self.developable_minimum_unit_variable, where_developable),
                              "get_weights_for_sampling_locations - computing developable_minimum_unit_variable")
        else:
            min_capacity = zeros(max_capacity.size)

        if max_capacity.sum(dtype="float32") == 0:
            raise RuntimeError, "There are no choices with any capacity for %s buildings." % agent_set.what

        #how many buildings fit in each developable location
        max_building_size = sort(max_capacity)[-max(50,int(where_developable.size*0.001))]
        proposed_building_sizes = agent_set.get_attribute_by_index(self.units_full_name, agents_index)
        if proposed_building_sizes.max() > max_building_size: # change the size if there is not enough space
            logger.log_status("Maximum building size: %s" % proposed_building_sizes.max())
            self.modify_agents_size(agent_set, minimum(proposed_building_sizes,max_building_size), agents_index)
            proposed_building_sizes = agent_set.get_attribute_by_index(self.units_full_name, agents_index)
            if self.run_config.get("agent_units_string", None): # needs to be corrected
                self.run_config["agent_units_all"] = agent_set.get_attribute_by_index(self.run_config["agent_units_string"], agents_index)
            logger.log_warning("Not enough building capacity. Large building sizes reduced to %s" % max_building_size)
        proposed_building_sizes = reshape(proposed_building_sizes, (proposed_building_sizes.size,1))
        weight_array = logical_and(proposed_building_sizes >= reshape(min_capacity, (1, min_capacity.size)),
                        (reshape(max_capacity, (1, max_capacity.size)) >=
                             proposed_building_sizes))

        # for memory reasons, discard columns that have only zeros
        keep = where(weight_array.sum(axis=0, dtype=int32))[0]
        where_developable = where_developable[keep]
        weight_array = take(weight_array, keep, axis=1)
        if where_developable.size <= 0:
            logger.log_warning("No developable locations available.")
            
        self.filter_index = where_developable
         
        return weight_array

#    def apply_filter(self, filter, agent_set=None, agents_index=None, **kwargs):
#        """Do nothing since filter was already applied get_weights_for_sampling_locations."""
#        if weights is not None:
#            return weights
#        else:
#            return ones(self.choice_set.size())

    def get_agents_order(self, movers):
        """Sort in descending order according to the size in order to locate larger agents first.
        """
        return argsort(movers.get_attribute(self.units_full_name))[arange(movers.size()-1,-1,-1)]

    def choose_agents_to_move_from_overfilled_locations(self, capacity,
                                                        agent_set, agents_index, agents_locations):
        """Agents with the smallest number of units should move again.
        """
        if capacity is None:
            return array([], dtype='int32')
        index_valid_agents_locations = where(agents_locations > 0)[0]
        valid_agents_locations = agents_locations[index_valid_agents_locations].astype("int32")
        unique_locations = unique_values(valid_agents_locations).astype("int32")
        index_consider_capacity = self.choice_set.get_id_index(unique_locations)
        capacity_of_affected_locations = capacity[index_consider_capacity]
        overfilled = where(capacity_of_affected_locations < 0)[0]
        movers = array([], dtype='int32')
        indexed_individuals = DatasetSubset(agent_set, agents_index[index_valid_agents_locations])
        ordered_agent_indices = self.get_agents_order(indexed_individuals)
        sizes = indexed_individuals.get_attribute(self.units_full_name)[ordered_agent_indices]
        choice_ids = self.choice_set.get_id_attribute()
        for loc in overfilled:
            agents_to_move = where(valid_agents_locations == choice_ids[index_consider_capacity[loc]])[0]
            if agents_to_move.size > 0:
                n = int(-1*capacity_of_affected_locations[loc])
                this_sizes = sizes[agents_to_move]
                csum = this_sizes[arange(this_sizes.size-1,-1,-1)].cumsum() # ordered increasingly
                csum = csum[arange(csum.size-1, -1,-1)] # ordered back decreasingly
                w = where(csum < n)[0]
                if w.size < agents_to_move.size: #add one more agent in order the cumsum be larger than n
                    w = concatenate((array([agents_to_move.size-w.size-1]), w))
                idx = ordered_agent_indices[agents_to_move[w]]
                movers = concatenate((movers, idx))
        return movers

    def estimate(self, *args, **kargs):
        agent_set = kargs["agent_set"]
        data_objects = kargs.get("data_objects", {})
        data_objects[agent_set.get_dataset_name()] = agent_set
        estimate_config = kargs.get("estimate_config", {})
        self.units_full_name = "%s.%s.%s" % (estimate_config.get("agent_variables_package", "urbansim"),
                                             agent_set.get_dataset_name(), self.units)
        agent_set.compute_variables(self.units_full_name, dataset_pool=self.dataset_pool, resources=Resources(data_objects))
        #logger.log_status("Buildings size: %d" % (agent_set.get_attribute_by_index(self.units_full_name).sum()))
        return AgentLocationChoiceModelMember.estimate(self, *args, **kargs)

    def create_interaction_dataset(self, agent_set, agents_index, config, *args, **kwargs):
        if config is not None and config.get("estimate", False):
                id_name = self.choice_set.get_id_name()[0]
                mod_id_name = "__%s__" % id_name
                if mod_id_name in agent_set.get_known_attribute_names():
                    agent_set.set_values_of_one_attribute(id_name, agent_set.get_attribute(mod_id_name))
                result = LocationChoiceModel.create_interaction_dataset(self, agent_set,
                                                                        agents_index, config, **kwargs)
                # select randomly buildings to unplace
                ntounplace = int(agents_index.size/4.0)
                #ntounplace = 1
                #self.dataset_pool.get_dataset("urbansim_constant")["recent_years"])
                #idx = sample_noreplace(agents_index, ntounplace)
                tmp = randint(0, agents_index.size, ntounplace)
                utmp = unique_values(tmp)
                idx = agents_index[utmp]
                logger.log_status("Unplace %s buildings." % utmp.size)
                if  (mod_id_name not in agent_set.get_known_attribute_names()):
                    agent_set.add_attribute(name=mod_id_name, data=array(agent_set.get_attribute(id_name)))
                agent_set.set_values_of_one_attribute(id_name,-1.0*ones((idx.size,)), idx)
                
                return result

        return LocationChoiceModel.create_interaction_dataset(self, agent_set,
                                                              agents_index, config, **kwargs)

    def prepare_for_estimate(self, agent_set, add_member_prefix=True, specification_dict=None, specification_storage=None,
                              specification_table=None, urbansim_constant=None, building_categories=None,
                              location_id_variable=None, dataset_pool=None, **kwargs):
        """Return index of buildings that are younger than 'recent_years'+2"""
        type = self.group_member.get_member_name()
        if location_id_variable:
            agent_set.compute_variables(location_id_variable, dataset_pool=dataset_pool)
        agent_set.resources["building_categories"] = building_categories
        agent_set.compute_variables("urbansim.%s.size_category_%s" % (agent_set.get_dataset_name(), self.group_member.get_member_name()),
                           dataset_pool=dataset_pool)
        agent_set.compute_variables(["urbansim.%s.building_age" % agent_set.get_dataset_name(),
                                     "urbansim.%s.is_building_type_%s" % (agent_set.get_dataset_name(),
                                     type)], dataset_pool=dataset_pool)
        index = where(logical_and(ma.filled(agent_set.get_attribute("building_age"),
                                         urbansim_constant['recent_years']+2) <= urbansim_constant['recent_years']+1,
                                  agent_set.get_attribute("is_building_type_%s" % type)))[0]
        specification, dummy = AgentLocationChoiceModelMember.prepare_for_estimate(self, add_member_prefix,
                                                               specification_dict, specification_storage,
                                                               specification_table,
                                                               location_id_variable=location_id_variable,
                                                               data_objects=dataset_pool.datasets_in_pool(),
                                                                                   **kwargs)
        return (specification, index)

    def prepare_for_estimate_alt(self, agent_set, add_member_prefix=True, specification_dict=None, specification_storage=None,
                              specification_table=None, events_for_estimation_storage=None,
                              events_for_estimation_table=None, urbansim_constant=None, base_year=0,
                              building_categories=None,
                              location_id_variable=None, dataset_pool=None, **kwargs):
        """Remove new buildings of this type and add new projects from event history instead."""
        type = self.group_member.get_member_name()
        agent_set.resources["building_categories"] = building_categories
        agent_set.compute_variables(["urbansim.%s.building_age" % agent_set.get_dataset_name(),
                                     "urbansim.%s.is_building_type_%s" % (agent_set.get_dataset_name(),
                                     type)], dataset_pool = dataset_pool)
        idx_new_buildings = where(logical_and(where(ma.filled(agent_set.get_attribute("building_age"),
                                         urbansim_constant['recent_years'] + 1) <= urbansim_constant['recent_years'], 1, 0),
                                  agent_set.get_attribute("is_building_type_%s" % type)))[0]
        # create agents for estimation
        if events_for_estimation_storage is not None:
            agent_set.remove_elements(idx_new_buildings)
            event_set = DevelopmentEventDataset(urbansim_constant,
                                            in_storage = events_for_estimation_storage,
                                            in_table_name= events_for_estimation_table)
            event_set.remove_non_recent_data(base_year, urbansim_constant['recent_years'])
            BuildingCreator().add_events_from_history_to_existing_buildings(agent_set,
                                               event_set, type,
                                               self.group_member.get_member_code(),
                                               self.units, building_categories, dataset_pool=dataset_pool)
        if location_id_variable:
            agent_set.compute_variables(location_id_variable, dataset_pool=dataset_pool)

        if events_for_estimation_storage is None:
            agent_set.compute_variables(["urbansim.%s.size_category_%s" % (agent_set.get_dataset_name(),
                                                                           self.group_member.get_member_name()),
                                         "urbansim.%s.building_age" % agent_set.get_dataset_name()],
                           dataset_pool = dataset_pool)
        idx_new_buildings = where(ma.filled(agent_set.get_attribute("building_age"),
                                         urbansim_constant['recent_years']+1) <= urbansim_constant['recent_years'])[0]
        if (specification_dict is not None) or (specification_storage is not None):
            specification, dummy = AgentLocationChoiceModelMember.prepare_for_estimate(self, add_member_prefix,
                                                               specification_dict, specification_storage,
                                                               specification_table,
                                                               location_id_variable=location_id_variable,
                                                               data_objects=dataset_pool.datasets_in_pool(), **kwargs)
        else:
            specification = None
        return (specification, idx_new_buildings)

    def modify_agents_size(self, agent_set, size, index, non_residential_attr_name="sqft", 
                           residential_attr_name="residential_units"):
        if re.search("sqft", self.units_full_name):
            attr_name = non_residential_attr_name
        else:
            attr_name = residential_attr_name
        agent_set.modify_attribute(attr_name, size, index)
        agent_set.compute_variables(self.units_full_name, dataset_pool = self.dataset_pool)
