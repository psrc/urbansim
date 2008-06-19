#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique_values
from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel
import re
from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.agent_location_choice_model_member import AgentLocationChoiceModelMember

class SubAreaEmploymentLocationChoiceModel(EmploymentLocationChoiceModel):
    """Run the urbansim ELCM separately for each subarea."""
    model_name = "SubArea Employment Location Choice Model" 

    def __init__(self, group_member, location_set, 
            agents_grouping_attribute = 'job.building_type',
            sampler = "opus_core.samplers.weighted_sampler", 
            utilities = "opus_core.linear_utilities", 
            choices = "opus_core.random_choices", 
            probabilities = "opus_core.mnl_probabilities", 
            estimation = "opus_core.bhhh_mnl_estimation", 
            capacity_string = "vacant_SSS_job_space",
            estimation_weight_string = "total_number_of_possible_SSS_jobs",
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
            variable_package="urbansim",
            subarea_id_name="faz_id"):
        """ 'group_member' is of type ModelGroupMember. All SSS in variable names are replaced by the group member name.
        """
        group_member_name = group_member.get_member_name()
        if capacity_string:
            capacity_string = re.sub('SSS', group_member_name, capacity_string)
        if estimation_weight_string:
            estimation_weight_string = re.sub('SSS', group_member_name, estimation_weight_string)
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
        self.subarea_id_name = subarea_id_name

    
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        regions = agent_set.get_attribute(self.subarea_id_name)
        self.choice_set.compute_variables(["urbansim_parcel.%s.%s" % (self.choice_set.get_dataset_name(), self.subarea_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_region = where(regions[agents_index] > 0)[0]
        if valid_region.size > 0:
            unique_regions = unique_values(regions[agents_index][valid_region])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_region]] = True
            for area in unique_regions:
                new_index = where(logical_and(cond_array, regions == area))[0]
                self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.subarea_id_name, area)
                logger.log_status("ELCM for area %s" % area)
                EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=new_index, **kwargs)
        no_region = where(regions[agents_index] <= 0)[0]
        if no_region.size > 0: # run the ELCM for jobs that don't have assigned region
            self.filter = None
            logger.log_status("ELCM for jobs with no area assigned")
            choices = EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                                 agents_index=agents_index[no_region], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = self.choice_set.get_id_index(choices[where_valid_choice])
            chosen_regions = self.choice_set.get_attribute_by_index(self.subarea_id_name, choices_index)
            agent_set.modify_attribute(name=self.subarea_id_name, data=chosen_regions, 
                                       index=no_region[where_valid_choice])
