#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.resources import merge_resources_if_not_None, merge_resources_with_defaults
from urbansim.models.development_project_zone_location_choice_model import DevelopmentProjectZoneLocationChoiceModel

class DevelopmentProjectZoneLocationChoiceModelCreator(object):
    """
    Class for creating an instance of a development project zone location choice model.
    """

    def get_model(self, 
                  project_type,
                  location_set,
                  model_configuration,
                  sampler = "opus_core.samplers.weighted_sampler", 
                  utilities = "opus_core.linear_utilities", 
                  choices = "urbansim.lottery_choices", 
                  probabilities = "opus_core.mnl_probabilities", 
                  estimation = "opus_core.bhhh_mnl_estimation", 
                  sample_proportion_locations = None, 
                  sample_size_locations = 30, 
                  estimation_size_agents = 1.0, 
                  compute_capacity_flag = True, 
                  filter = None,
                  submodel_string = "size_category", 
                  location_id_string = 'urbansim.development_project.zone_id',
                  run_config = None, 
                  estimate_config=None, 
                  debuglevel=0):
        units = model_configuration['units']        
        default_capacity_attribute = "urbansim.zone.developable_maximum_%s" % units
        estimation_weight_string_default = "urbansim.zone.developable_maximum_%s" % units
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
            [("weights_for_estimation_string", estimation_weight_string_default)])
        
        return DevelopmentProjectZoneLocationChoiceModel(location_set, 
                                                     project_type=project_type, 
                                                     units=units,
                                                     model_name="Development Project %s Location Choice Model" % project_type,
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
