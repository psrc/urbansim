# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import re
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.agent_location_choice_model_member import AgentLocationChoiceModelMember

class EmploymentLocationChoiceModel(AgentLocationChoiceModelMember):
    
    def __init__(self, group_member, location_set, 
            agents_grouping_attribute = 'job.building_type',
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities", 
            estimation = "opus_core.bhhh_mnl_estimation", 
            capacity_string = "vacant_SSS_job_space",
            estimation_weight_string = "total_number_of_possible_SSS_jobs",
            simulation_weight_string = None, # if this is None, weights are proportional to the capacity 
            number_of_agents_string = "number_of_SSS_jobs",
            number_of_units_string = "total_number_of_possible_SSS_jobs",
            sample_proportion_locations = None, 
            sample_size_locations = 30, 
            estimation_size_agents = 1.0, 
            compute_capacity_flag = True, 
            filter = None,
            submodel_string = "sector_id", location_id_string = None,
            demand_string = None, # if not None, the aggregate demand for locations will be stored in this attribute
            run_config = None, estimate_config=None, debuglevel=0, dataset_pool=None,
            variable_package="urbansim"):
        """ 'group_member' is of type ModelGroupMember. All SSS in variable names are replaced by the group member name.
        """
        group_member_name = group_member.get_member_name()
        if capacity_string:
            capacity_string = re.sub('SSS', group_member_name, capacity_string)
        if estimation_weight_string:
            estimation_weight_string = re.sub('SSS', group_member_name, estimation_weight_string)
        if simulation_weight_string:
            simulation_weight_string = re.sub('SSS', group_member_name, simulation_weight_string)
        if number_of_agents_string:
            number_of_agents_string = re.sub('SSS', group_member_name, number_of_agents_string)
        if number_of_units_string:
            number_of_units_string = re.sub('SSS', group_member_name, number_of_units_string)
        if demand_string:
            demand_string = re.sub('SSS', group_member_name, demand_string)
            
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

        AgentLocationChoiceModelMember.__init__(self, group_member, location_set, 
                                        agents_grouping_attribute, 
                                        model_name = "Employment Location Choice Model", 
                                        short_name = "ELCM", 
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
                                        variable_package=variable_package)
