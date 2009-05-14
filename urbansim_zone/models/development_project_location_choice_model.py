# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import re
from numpy import logical_and, where, ones, take, argsort, arange, bool8, int8, int32
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from opus_core.logger import logger
from urbansim_zone.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.datasets.development_project_dataset import DevelopmentProjectCreator
from urbansim.models.location_choice_model import LocationChoiceModel

class DevelopmentProjectLocationChoiceModel(LocationChoiceModel):

    model_name = "Development Project Location Choice Model"
    model_short_name = "DPLCM"
    
    def __init__(self, project_type, location_set,
                  sampler = "opus_core.samplers.weighted_sampler", 
                  utilities = "opus_core.linear_utilities", 
                  choices = "urbansim.first_agent_first_choices", 
                  probabilities = "opus_core.mnl_probabilities",
                  estimation = "opus_core.bhhh_mnl_estimation",
                  capacity_string = "urbansim_zone.zone.vacant_SSS_job_space",
                  estimation_weight_string = None, 
                  simulation_weight_string = None, # if this is None, the weights are proportional to how many projects fits into locations
                  sample_proportion_locations = None, 
                  sample_size_locations = 30, 
                  estimation_size_agents = 1.0, 
                  compute_capacity_flag = True,
                  filter = None,
                  submodel_string = None, 
                  location_id_string = None,
                  run_config = None, 
                  estimate_config=None, 
                  debuglevel=0):

        if capacity_string:
            capacity_string = re.sub('SSS', project_type, capacity_string)
        if estimation_weight_string:
            estimation_weight_string = re.sub('SSS', project_type, estimation_weight_string)
        if simulation_weight_string:
            simulation_weight_string = re.sub('SSS', project_type, simulation_weight_string)
            
        run_config = merge_resources_if_not_None(run_config, [ 
            ("sample_proportion_locations", sample_proportion_locations), 
            ("sample_size_locations", sample_size_locations), 
            ("compute_capacity_flag", compute_capacity_flag),
            ("capacity_string", capacity_string),
            ("weights_for_simulation_string", simulation_weight_string),
                    ])     
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents),
                    ("weights_for_estimation_string", estimation_weight_string)])         
        
        self.project_type = project_type
        self.model_name = "%s %s" % (self.project_type, self.model_name)
        self.model_short_name = "%s %s" % (self.project_type[:3], self.model_short_name)
        
        LocationChoiceModel.__init__(self, location_set, 
                                                     sampler=sampler, 
                                                     utilities=utilities, 
                                                     probabilities=probabilities, 
                                                     choices=choices, 
                                                     filter=filter,
                                                     submodel_string=submodel_string, 
                                                     location_id_string = location_id_string,
                                                     run_config=run_config, 
                                                     estimate_config=estimate_config, 
                                                     debuglevel=debuglevel)

    def run(self, *args, **kargs):
        agent_set = kargs["agent_set"]
        if agent_set is None:
            logger.log_status("No development projects for this model")
            return None
        return LocationChoiceModel.run(self, *args, **kargs)
    
    def get_weights_for_sampling_locations(self, agent_set, agents_index):
        weight_string = self.run_config.get("weights_for_simulation_string", None)
        if weight_string is not None:
            return LocationChoiceModel.get_weights_for_sampling_locations(self, agent_set, agents_index)
        if self.capacity is None:
            RuntimeError, "The capacity string must be given."
        where_developable = self.capacity > 0
        if self.filter is not None:
            self.choice_set.compute_variables([self.filter], dataset_pool = self.dataset_pool)
            where_developable = logical_and(self.capacity > 0, self.choice_set.get_attribute(self.filter) > 0)
        where_developable = where(where_developable)[0]
        weight_array = (ones((agents_index.size, where_developable.size), dtype=int8)).astype(bool8)
        
        max_capacity = self.capacity[where_developable]

        if max_capacity.sum() == 0:
            raise RuntimeError, "There are no choices with any capacity for %s projects" % agent_set.what

        #how many projects fit in each developable location
        proposed_project_sizes = agent_set.get_attribute_by_index(agent_set.get_attribute_name(),
                                                                  agents_index)
        for iagent in arange(agents_index.size):
            proposed_project_size = proposed_project_sizes[iagent]
            weight_array[iagent, :] = proposed_project_size <= max_capacity

        # for memory reasons, discard columns that have only zeros
        logger.log_status("shape of weight_array: ", weight_array.shape)
        keep = where(weight_array.sum(axis=0, dtype=int32))[0]
        where_developable = where_developable[keep]
        if where_developable.size <= 0:
            logger().log_warning("No developable locations available.")
        weight_array = take(weight_array, keep, axis=1)
        return (weight_array, where_developable)
    
    def get_agents_order(self, movers):
        """Sort in descending order according to the size in order to locate larger agents first.
        """
        return argsort(movers.get_attribute(movers.parent.get_attribute_name()))[arange(movers.size()-1,-1,-1)]
    
    def determine_units_capacity(self, agent_set, agents_index):
        capacity = LocationChoiceModel.determine_units_capacity(self, agent_set, agents_index)
        # subtract locations taken in previous chunks
        taken_locations = self.choice_set.sum_over_ids(agent_set.get_attribute(self.choice_set.get_id_name()[0]),
                                                       ones((agent_set.size(),)))
        return capacity - taken_locations
    
    def prepare_for_estimate(self, specification_dict = None, specification_storage=None,
                              specification_table=None,
                              events_for_estimation_storage=None,
                              events_for_estimation_table=None, urbansim_constant=None, base_year=0, units='job_spaces',
                              categories=None):

        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        projects = None
        # create agents for estimation
        if events_for_estimation_storage is not None:
            event_set = DevelopmentEventDataset(
                                            in_storage = events_for_estimation_storage,
                                            in_table_name= events_for_estimation_table)
            event_set.remove_non_recent_data(base_year, urbansim_constant['recent_years'])
            projects = DevelopmentProjectCreator().create_projects_from_history(
                                               event_set, self.project_type,
                                               units, categories)
        return (specification, projects)
    
    def prepare_for_run(self, *args, **kwargs):
        spec, coef, dummy = LocationChoiceModel.prepare_for_run(self, *args, **kwargs)
        return (spec, coef)
