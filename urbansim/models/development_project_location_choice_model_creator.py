# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.development_project_location_choice_model import DevelopmentProjectLocationChoiceModel

class DevelopmentProjectLocationChoiceModelCreator(object):
    """
    Class for creating an instance of a development project location choice model.
    Uses information in the development_projects configuration to specialize 
    a development project location choice model for the given type of project,
    e.g. for 'commercial'.  The set of allowed types of projects are defined
    by the contents of the development_projects configuration.
    """
    
    estimation_weight_string_default = None

    def get_model(self, 
                  project_type,
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
                  filter = "",
                  submodel_string = "size_category", 
                  model_configuration = None,
                  location_id_string = None,
                  run_config = None, 
                  estimate_config = None, 
                  debuglevel = 0,
                  units = '',
                  developable_maximum_unit_variable_full_name = '',
                  developable_minimum_unit_variable_full_name = '',
                  residential = False):
        
        if model_configuration is not None:
            units = model_configuration['units']
            developable_maximum_unit_variable_full_name = model_configuration['developable_maximum_unit_variable_full_name']
            developable_minimum_unit_variable_full_name = model_configuration['developable_minimum_unit_variable_full_name']
        
        default_capacity_attribute = "urbansim.gridcell.is_developable_for_%s" % units
        default_filter = "urbansim.gridcell.developable_%s" % units
        if filter == "":
            filter = default_filter
        run_config = merge_resources_if_not_None(run_config, [ 
            ("sample_proportion_locations", sample_proportion_locations), 
            ("sample_size_locations", sample_size_locations), 
            ("compute_capacity_flag", compute_capacity_flag)])
        run_config = merge_resources_with_defaults(run_config, 
            [("capacity_string", default_capacity_attribute)])
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents)])         
        estimate_config = merge_resources_with_defaults(estimate_config, 
            [("weights_for_estimation_string", self.estimation_weight_string_default)])
        
        return DevelopmentProjectLocationChoiceModel(location_set, 
                                                     project_type=project_type, 
                                                     units=units,
                                                     developable_maximum_unit_variable_full_name=developable_maximum_unit_variable_full_name,
                                                     developable_minimum_unit_variable_full_name=developable_minimum_unit_variable_full_name,
                                                     model_name="Development Project %s Location Choice Model" % project_type,
#                                                     residential = residential,
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
