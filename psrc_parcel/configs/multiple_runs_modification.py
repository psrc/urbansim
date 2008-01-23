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

from opus_core.configuration import Configuration

class MultipleRunsModification:
    models_with_normally_sampled_coefficients = [
             "real_estate_price_model",
             "employment_location_choice_model", "home_based_employment_location_choice_model",
             "household_location_choice_model",
             ]
    models_with_sampled_control_totals = [
                       "employment_transition_model",
                       "household_transition_model"
                       ]
    models_with_sampled_relocation_rates = [
                       "employment_relocation_model",
                       "household_relocation_model"
                       ]
    def modify_configuration(self, config):
        self.modify_by_local_configuration(config)
        self.modify_controller_for_first_year(config)
            
    def modify_by_local_configuration(self, config):
        # some models in the first year have sampled inputs and therefore different controller
        if 'models_in_year' not in config.keys():
            config['models_in_year'] = {}
        config['models_in_year'][config['base_year']+1]= [
                "real_estate_price_model_with_sampled_coef",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "household_transition_model_with_sampled_ct",
                "employment_transition_model_with_sampled_ct",
                "household_relocation_model_with_sampled_rr",
                "household_location_choice_model_with_sampled_coef",
                "employment_relocation_model_with_sampled_rr",
                {"employment_location_choice_model_with_sampled_coef":{'group_members': ['_all_']}},
                'distribute_unplaced_jobs_model'
                ]
        
    def modify_controller_for_first_year(self, config):
        for model_name in self.models_with_normally_sampled_coefficients:
            new_model_name = "%s_with_sampled_coef" % model_name
            config["models_configuration"][new_model_name] = Configuration(config["models_configuration"][model_name])
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["sample_coefficients"] = \
                                                True
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["cache_storage"] = \
                                                "base_cache_storage" 
        for model_name in self.models_with_sampled_control_totals:
            new_model_name = "%s_with_sampled_ct" % model_name
            config["models_configuration"][new_model_name] = config["models_configuration"][model_name]
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["sample_control_totals"] = \
                                                True
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["variance"] = 0.0001
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["base_year"] = "base_year"
        for model_name in self.models_with_sampled_relocation_rates:
            new_model_name = "%s_with_sampled_rr" % model_name
            config["models_configuration"][new_model_name] = config["models_configuration"][model_name]
            config["models_configuration"][new_model_name]["controller"]["prepare_for_run"]["arguments"]["sample_rates"] = True
                                                