# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.models.location_choice_model import LocationChoiceModel
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import probsample_noreplace, sample_noreplace
from opus_core.datasets.dataset import Dataset
from numpy import where, arange, concatenate, array, ndarray, zeros, resize
from opus_core.resources import Resources
from opus_core.misc import unique
from numpy import ma, intersect1d, ones_like
from opus_core.logger import logger
from opus_core.models.model import prepare_for_estimate
import copy

class AgentLocationChoiceModel(LocationChoiceModel):
    """Child class of the LocationChoiceModel. Re-run LocationChoiceModel 
    if there are unplaced agents after a run.
    """

    model_name = "Agent Location Choice Model"
    model_short_name = "ALCM"
    
    def __init__(self, location_set, 
                 run_config=None, 
                 estimate_config=None, 
                 variable_package = "urbansim", 
                 *args,
                 **kwargs):
        """
        :number_of_units_string:
          number of units string is used to determine whether a choice is over-filled, 
          by comparing it with number_of_agents_string in get_locations_vacancy().  
          TODO: How does it differ from capacity_string?
           
        """
        if (run_config is not None) and not isinstance(run_config, Resources):
            run_config = Resources(run_config)
        if (estimate_config is not None) and not isinstance(estimate_config, Resources):
            estimate_config = Resources(estimate_config)
        self.add_prefix_to_variable_names(["capacity_string", "number_of_agents_string", "number_of_units_string"],
                                           location_set, variable_package, run_config)
        self.add_prefix_to_variable_names("weights_for_estimation_string",
                                           location_set, variable_package, estimate_config)

        LocationChoiceModel.__init__(self, 
                                     location_set=location_set, 
                                     run_config=run_config,
                                     estimate_config=estimate_config,
                                     *args, **kwargs
                                    )

    def run(self, specification, coefficients, agent_set,
            agents_index=None, agents_filter=None,
            chunk_specification=None, data_objects=None,
            run_config=None, debuglevel=0, maximum_runs=10):

        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)

        bindex = zeros(agent_set.size(), dtype='b')
        if agents_filter is not None:
            bfilter = agent_set.compute_variables(agents_filter, 
                                                  dataset_pool=self.dataset_pool)

            if agents_index is not None:
                bindex[agents_index] = True
                agents_index = where(bindex * bfilter)[0]
            else:
                agents_index = where(bfilter)[0]
        else:
            if agents_index is not None:
                agents_index = agents_index
            else:
                agents_index = arange(agent_set.size())

        if not isinstance(agents_index, ndarray):
            try:
                agents_index = array(agents_index)
            except:
                raise TypeError, "Argument agents_index is of wrong type (numpy array or list allowed.)"

        if agents_index.size == 0:
            logger.log_status("Nothing to be done.")
            return array([], dtype='int32')

        if run_config == None:
            run_config = Resources()
        self.run_config = run_config.merge_with_defaults(self.run_config)
        #this is handled by choices module (in UPC sequence)
        self.number_of_units_string = self.run_config.get("number_of_units_string", None)
        #self.number_of_agents_string = self.run_config.get(
        #                "number_of_agents_string",
        #                "%s.number_of_agents(%s)" % (self.choice_set.get_dataset_name(), agent_set.get_dataset_name()))
            
        if self.number_of_units_string is None:
            maximum_runs = 1

        unplaced = ones_like(agents_index).astype('bool')
        #boolean of the same shape as agents_index
        end_choices = -1 * ones_like(agents_index)
        id_name = self.choice_set.get_id_name()[0]
        demand_string = self.run_config.get("demand_string")
        supply_string = self.run_config.get("supply_string")
        for run in range(maximum_runs):
            unplaced_size_before = unplaced.sum()
            choices = LocationChoiceModel.run(self, 
                                              specification=specification, 
                                              coefficients=coefficients, 
                                              agent_set=agent_set,
                                              agents_index=agents_index[unplaced], 
                                              chunk_specification=chunk_specification, 
                                              debuglevel=debuglevel)
            end_choices[unplaced] = choices
            if run > 0:
                ## delete demand_string and supply string for later iterations to 
                ## avoid these variables being distorted by assigning overfilled agents
                if demand_string: del self.run_config["demand_string"]
                if supply_string: del self.run_config["supply_string"]
                
            unplaced = agent_set[id_name][agents_index] <= 0
            ## these two lines are inside the loop because self.observations_mapping is 
            ## not initialized before calling LocationChoiceModel.run
            agents_size_mapped = self.observations_mapping['mapped_index'].size
            agents_size_unmapped = agents_index.size - agents_size_mapped
            
            logger.log_status("Agent Location Choice Model iteration %s/%s: %s unplaced agents" % \
                              (run+1, maximum_runs, unplaced.sum()))
            if unplaced.sum() in (0, unplaced_size_before, agents_size_unmapped):
                logger.log_status("All agents placed or number of unplaced agents doesn't change; exit ALCM.")
                break

            agent_set.set_values_of_one_attribute(id_name, -1, agents_index[unplaced])
            
        if demand_string: self.run_config["demand_string"] = demand_string
        if supply_string: self.run_config["supply_string"] = supply_string
        
        return end_choices

    def add_prefix_to_variable_names(self, variable_names, dataset, variable_package, resources):
        """
        ##TODO: refactor to require variable_package to be provided with variable_names

        Add a prefix of 'package.dataset_name.' to variable_names from resources.
        """
        if resources is None:
            return
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

    def create_interaction_dataset(self, agent_set, agents_index, config, **kwargs):
        if config is not None and config.get("estimate", False):
            id_name = self.choice_set.get_id_name()[0]
            mod_id_name = "__%s__" % id_name
            # This should be only true when reestimating, since the agents for estimation were unplaced
            # in the previous run and their original locations were stored in mod_id_name
            if mod_id_name in agent_set.get_known_attribute_names():
                agent_set.set_values_of_one_attribute(id_name, agent_set.get_attribute(mod_id_name))
                result = LocationChoiceModel.create_interaction_dataset(self, agent_set,
                                                                        agents_index, config, **kwargs)                
                return result

        return LocationChoiceModel.create_interaction_dataset(self, agent_set,
                                                              agents_index, config, **kwargs)

    def prepare_for_run(self, *args, **kwargs):
        spec, coef, dummy = LocationChoiceModel.prepare_for_run(self, *args, **kwargs)
        return (spec, coef)
    
    def prepare_for_estimate(self, 
                             agent_set=None, 
                             index_to_unplace=None, 
                             portion_to_unplace=1.0,
                             compute_lambda=False, 
                             grouping_location_set=None,
                             movers_variable=None, 
                             movers_index=None,
                             location_id_variable=None,
                             data_objects={},
                             *args, **kwargs
                            ):
        """Put 'location_id_variable' always in, if the location id is to be computed on the estimation set,
        i.e. if it is not a primary attribute of the estimation set. Set 'index_to_unplace' to None, if 'compute_lambda' is True.
        In such a case, the annual supply is estimated without unplacing agents. 'grouping_location_set', 'movers_variable' and
        'movers_index' must be given, if 'compute_lambda' is True.
        """
        from urbansim.functions import compute_supply_and_add_to_location_set

        if (agent_set is not None) and (index_to_unplace is not None):
            if self.location_id_string is not None:
                agent_set.compute_variables(self.location_id_string, 
                                            resources=Resources(data_objects))
            if portion_to_unplace < 1:
                unplace_size = int(portion_to_unplace*index_to_unplace.size)
                end_index_to_unplace = sample_noreplace(index_to_unplace, unplace_size)
            else:
                end_index_to_unplace = index_to_unplace
            logger.log_status("Unplace " + str(end_index_to_unplace.size) + " agents.")
            agent_set.modify_attribute(self.choice_set.get_id_name()[0],
                                        resize(array([-1]), end_index_to_unplace.size), 
                                       end_index_to_unplace)
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

        specification, index = prepare_for_estimate(agent_set=agent_set,
                                                    *args, **kwargs)

        return (specification, index)

### In order to remove a circular dependency between this file and
### household_location_choice_model_creator, these unit tests were moved into
### urbansim.tests.test_agent_location_choice_model.
