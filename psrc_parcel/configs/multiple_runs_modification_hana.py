#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from multiple_runs_modification import MultipleRunsModification

class MultipleRunsModificationHana(MultipleRunsModification):
    models_with_normally_sampled_coefficients = [
             "real_estate_price_model",
             "employment_location_choice_model", "home_based_employment_location_choice_model",
             "household_location_choice_model",
             'workplace_choice_model_for_resident',
             'work_at_home_choice_model',
             ]
    models_with_sampled_control_totals = [
#                       "employment_transition_model",
#                       "household_transition_model"
                       ]
    models_with_sampled_relocation_rates = [
                       "employment_relocation_model",
                       "household_relocation_model"
                       ]
    models_with_mixed_sampled_coefficients = {
                    "household_relocation_choice_model": {'b1_tt': {'distribution': 'uniform',
                                                                         'parameters': {'a': 0.001, 'b': 1, 'center_around_value': False}
                                                                         }
                                                        },
                    "workplace_relocation_choice_model": {'b1_tt': {'distribution': 'uniform',
                                                                         'parameters': {'a': 0.001, 'b': 1, 'center_around_value': False}
                                                                         }
                                                        }
                                              }
#    firstyear_models = [
#                "real_estate_price_model_with_sampled_coef",
#                "expected_sale_price_model",
#                "development_proposal_choice_model",
#                "building_construction_model",
#                "modify_workers_jobs_after_moving_households", # from demolished buildings
#                "modify_workers_jobs_after_moving_jobs", # from demolished buildings
#                "household_transition_model", 
#                "employment_transition_model",
#               'job_person_consistency_keeper',
#               "household_relocation_choice_model_with_sampled_coef",
#                #"household_relocation_model_with_sampled_rr",
#                "household_location_choice_model_with_sampled_coef",
#                "modify_workers_jobs_after_moving_households",
#                "employment_relocation_model_with_sampled_rr",
#                {"employment_location_choice_model_with_sampled_coef":{'group_members': ['non_home_based']}},
#                'distribute_unplaced_jobs_model',
#                'distribute_unplaced_mining_utilities_jobs_model',
#                "modify_workers_jobs_after_moving_jobs",
#                'work_at_home_choice_model_with_sampled_coef',
#                'workplace_relocation_choice_model_with_sampled_coef',
#                'workplace_choice_model_for_resident_with_sampled_coef'
#                ]

    firstyear_models = [
                "real_estate_price_model",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "modify_workers_jobs_after_moving_households", # from demolished buildings
                "modify_workers_jobs_after_moving_jobs", # from demolished buildings
                "household_transition_model", 
                "employment_transition_model",
               'job_person_consistency_keeper',
               "household_relocation_choice_model_with_sampled_coef",
                #"household_relocation_model_with_sampled_rr",
                "household_location_choice_model",
                #"modify_workers_jobs_after_moving_households",
                "employment_relocation_model",
                {"employment_location_choice_model":{'group_members': ['non_home_based']}},
                'distribute_unplaced_jobs_model',
                'distribute_unplaced_mining_utilities_jobs_model',
                "modify_workers_jobs_after_moving_jobs",
                'work_at_home_choice_model',
                'workplace_relocation_choice_model_with_sampled_coef',
                'workplace_choice_model_for_resident'
                ]
