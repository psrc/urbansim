# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class HouseholdLocationChoiceModelCreator(object):
    capacity_string_default = "vacant_residential_units" # attribute name of location_set that contains 
                                                             # capacity
    estimation_weight_string_default = "residential_units"
    number_of_agents_string_default = "number_of_households"
    number_of_units_string_default = "residential_units"
    
    def get_model(self, location_set,
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities", 
            estimation = "opus_core.bhhh_mnl_estimation", 
            sample_proportion_locations = None, 
            sample_size_locations = 30, 
            estimation_size_agents = 1.0, 
            compute_capacity_flag = True, 
            filter=None,
            submodel_string = None, location_id_string = None,
            demand_string = None, # if not None, the aggregate demand for locations will be stored in this attribute
            run_config = None, estimate_config=None, debuglevel=0, dataset_pool=None):
        run_config = merge_resources_if_not_None(run_config, [ 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("compute_capacity_flag", compute_capacity_flag)])
        run_config = merge_resources_with_defaults(run_config, 
            [("capacity_string", self.capacity_string_default),
            ("number_of_agents_string", self.number_of_agents_string_default),
            ("number_of_units_string", self.number_of_units_string_default)
              ])
        if demand_string:
            run_config["demand_string"] = demand_string
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents)])         
        estimate_config = merge_resources_with_defaults(estimate_config, 
            [("weights_for_estimation_string", self.estimation_weight_string_default)])
        return AgentLocationChoiceModel(location_set,
                                        model_name="Household Location Choice Model", 
                                        short_name="HLCM", 
                                        sampler=sampler, 
                                        utilities=utilities, 
                                        probabilities=probabilities, 
                                        choices=choices, 
                                        filter=filter, 
                                        submodel_string=submodel_string,  
                                        location_id_string=location_id_string,
                                        run_config=run_config, 
                                        estimate_config=estimate_config, 
                                        debuglevel=debuglevel, dataset_pool=dataset_pool)