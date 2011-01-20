# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import arange, logical_and, where, zeros
from opus_core.misc import unique
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from opus_core.logger import logger
from urbansim.models.development_project_location_choice_model import DevelopmentProjectLocationChoiceModel

class RegionalDevelopmentProjectLocationChoiceModel(DevelopmentProjectLocationChoiceModel):
    """
    """
    large_area_id_name = "large_area_id"
    estimation_weight_string_default = None

    def __init__(self, 
                  project_type,
                  location_set,
                  model_configuration,
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
                  location_id_string = None,
                  run_config = None, 
                  estimate_config=None, 
                  debuglevel=0):
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
        
        DevelopmentProjectLocationChoiceModel.__init__(self, location_set, 
                                                     project_type=project_type, 
                                                     units=units,
                                                     developable_maximum_unit_variable_full_name=developable_maximum_unit_variable_full_name,
                                                     developable_minimum_unit_variable_full_name=developable_minimum_unit_variable_full_name,
                                                     model_name="Regional Development Project %s Location Choice Model" % project_type,
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

    def run(self, specification, coefficients, agent_set, agents_index=None,  **kwargs):
        if agent_set is None:
            logger.log_status("No development projects for this model.")
            return None
        if agents_index is None:
            agents_index = arange(agent_set.size())
        large_areas = agent_set.compute_variables(["washtenaw.%s.%s" % (agent_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        self.choice_set.compute_variables(["washtenaw.%s.%s" % (self.choice_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        unique_large_areas = unique(large_areas[agents_index])
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        for area in unique_large_areas:
            self.this_large_area = area
            new_index = where(logical_and(cond_array, large_areas == area))[0]
            logger.log_status("DPLCM for area %s" % area)
            DevelopmentProjectLocationChoiceModel.run(self, specification=specification, coefficients=coefficients, 
                                                      agent_set=agent_set, agents_index=new_index, **kwargs)
            
    def determine_capacity(self, capacity_string=None, agent_set=None, **kwargs):
        """Filter the available capacity through the current large_area_id
        """
        capacity = DevelopmentProjectLocationChoiceModel.determine_capacity(self, capacity_string=capacity_string, 
                                                                            agent_set=agent_set, 
                                                                            **kwargs)
        is_large_area = self.choice_set.compute_variables(["%s.%s == %s" % (self.choice_set.get_dataset_name(), self.large_area_id_name, 
                                                            self.this_large_area)],
                                          dataset_pool=self.dataset_pool)
        return where(logical_and(capacity, is_large_area), capacity, 0)
