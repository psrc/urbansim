# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class EmploymentLocationChoiceModelCreator(object):
    
    capacity_string_default = "number_of_jobs_in_neighborhood"
    estimation_weight_string_default = "number_of_jobs_in_neighborhood"
    
    def get_model(self, location_set,
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities", 
            estimation = "opus_core.bhhh_mnl_estimation", 
            sample_proportion_locations = None, 
            sample_size_locations = 20, 
            estimation_size_agents = 1.0, 
            compute_capacity_flag = False, 
            filter = None,
            submodel_string = "sector_id",
            run_config = None, estimate_config=None, debuglevel=0):
        run_config = merge_resources_if_not_None(run_config, [ 
            ("sample_proportion_locations", sample_proportion_locations), 
            ("sample_size_locations", sample_size_locations), 
            ("compute_capacity_flag", compute_capacity_flag)])
        run_config = merge_resources_with_defaults(run_config, 
            [("capacity_string", self.capacity_string_default)])
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents)])         
        estimate_config = merge_resources_with_defaults(estimate_config, 
            [("weights_for_estimation_string", self.estimation_weight_string_default)])

        return AgentLocationChoiceModel(location_set, agent_name="job", 
            model_name="Employment Location Choice Model", \
            short_name="ELCM", sampler=sampler, utilities=utilities, 
            probabilities=probabilities, choices=choices, filter=filter, submodel_string=submodel_string, 
            run_config=run_config, estimate_config=estimate_config, 
            debuglevel=debuglevel)