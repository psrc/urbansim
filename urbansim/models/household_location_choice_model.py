# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel

class HouseholdLocationChoiceModel(AgentLocationChoiceModel):
    
    model_name = "Household Location Choice Model"
    model_short_name = "HLCM"
    
    def __init__(self, location_set,
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities",
            estimation = "opus_core.bhhh_mnl_estimation",
            capacity_string = "vacant_residential_units",
            estimation_weight_string = "residential_units", 
            simulation_weight_string = None, # if this is None, weights are proportional to the capacity 
            number_of_agents_string = "number_of_households",
            number_of_units_string = "residential_units",            
            sample_proportion_locations = None, 
            sample_size_locations = 30, 
            estimation_size_agents = 1.0, 
            compute_capacity_flag = True, 
            filter=None,
            submodel_string = None, location_id_string = None,
            demand_string = None, # if not None, the aggregate demand for locations will be stored in this attribute
            run_config = None, estimate_config=None, debuglevel=0, dataset_pool=None,
            variable_package="urbansim",
            **kwargs):
        run_config = merge_resources_if_not_None(run_config, [ 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("compute_capacity_flag", compute_capacity_flag),
                    ("capacity_string", capacity_string),
                    ("number_of_agents_string", number_of_agents_string),
                    ("number_of_units_string", number_of_units_string),
                    ("weights_for_simulation_string", simulation_weight_string),
                    ("demand_string", demand_string)                                                          
                                          ])
        estimate_config = merge_resources_if_not_None(estimate_config, [ 
                    ("estimation", estimation), 
                    ("sample_proportion_locations", sample_proportion_locations), 
                    ("sample_size_locations", sample_size_locations), 
                    ("estimation_size_agents", estimation_size_agents),
                    ("weights_for_estimation_string", estimation_weight_string)])         
    
        AgentLocationChoiceModel.__init__(self, location_set,
                                        model_name=self.model_name, 
                                        short_name=self.model_short_name, 
                                        sampler=sampler, 
                                        utilities=utilities, 
                                        probabilities=probabilities, 
                                        choices=choices, 
                                        filter=filter, 
                                        submodel_string=submodel_string,  
                                        location_id_string=location_id_string,
                                        run_config=run_config, 
                                        estimate_config=estimate_config, 
                                        debuglevel=debuglevel, dataset_pool=dataset_pool,
                                        variable_package=variable_package,
                                        **kwargs)
