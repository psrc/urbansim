# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 


# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from randstad.models.landuse_development_location_choice_model import LandUseDevelopmentLocationChoiceModel

class LandUseDevelopmentLocationChoiceModelCreator:
    """
    Class for creating an instance of a development project location choice model.
    Uses information in the development_projects configuration to specialize 
    a development project location choice model for the given type of project,
    e.g. for 'commercial'.  The set of allowed types of projects are defined
    by the contents of the development_projects configuration.
    """
    
    estimation_weight_string_default = None
    
    def get_model(self, 
                  location_set,
                  sampler = "opus_core.samplers.weighted_sampler", 
                  utilities = "opus_core.linear_utilities", 
                  choices = "urbansim.first_agent_first_choices", 
                  probabilities = "opus_core.mnl_probabilities", 
                  estimation = "opus_core.bhhh_mnl_estimation", 
                  sample_proportion_locations = None, 
                  sample_size_locations = 30, 
                  estimation_size_agents = 1.0, 
                  compute_capacity_flag = True, 
                  filter = "randstad.gridcell.is_developable",
                  submodel_string = "development_type_id",
                  run_config = None, 
                  estimate_config=None, 
                  debuglevel=0):

        default_capacity_string = "randstad.gridcell.is_developable"
        run_config = merge_resources_if_not_None(run_config, [ 
            ("sample_proportion_locations", sample_proportion_locations), 
            ("sample_size_locations", sample_size_locations), 
            ("compute_capacity_flag", compute_capacity_flag)
            ("filter", filter)])
        run_config = merge_resources_with_defaults(run_config, 
            [("capacity_string", default_capacity_string),
            ("simulation_sampling_include_current_choice", False)])
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents)])         
        estimate_config = merge_resources_with_defaults(estimate_config, 
            [("weights_for_estimation_string", self.estimation_weight_string_default),
            ("simulation_sampling_include_current_choice", True)])
        
        return LandUseDevelopmentLocationChoiceModel(location_set, 
                                                     opus_package='randstad',
                                                     model_name="Landuse Development Location Choice Model",
                                                     sampler=sampler, 
                                                     utilities=utilities, 
                                                     probabilities=probabilities, 
                                                     choices=choices, 
                                                     filter=filter,
                                                     submodel_string=submodel_string, 
                                                     run_config=run_config, 
                                                     estimate_config=estimate_config, 
                                                     debuglevel=debuglevel)

        