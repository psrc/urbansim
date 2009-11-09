# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from multiple_runs_modification import MultipleRunsModification

class MultipleRunsModificationHana(MultipleRunsModification):
    models_with_normally_sampled_coefficients = [
             "real_estate_price_model",
             "employment_location_choice_model",
             "household_location_choice_model",
             'workplace_choice_model_for_resident',
             'work_at_home_choice_model',
             "household_relocation_choice_model",
             "workplace_relocation_choice_model"
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
                                                                         'parameters': {'a': 0.001, 'b': 2, 'center_around_value': False}
                                                                         }
                                                        },
                    "workplace_relocation_choice_model": {'b1_tt': {'distribution': 'uniform',
                                                                         'parameters': {'a': 0.001, 'b': 1, 'center_around_value': False}
                                                                         }
                                                        }
                                              }
    firstyear_models = [
                "real_estate_price_model_with_sampled_coef",
                "expected_sale_price_model",
                "development_proposal_choice_model",
                "building_construction_model",
                "modify_workers_jobs_after_moving_households", # from demolished buildings
                "modify_workers_jobs_after_moving_jobs", # from demolished buildings
                "household_transition_model", 
                "employment_transition_model",
                'job_person_consistency_keeper',
                "household_relocation_choice_model_with_sampled_coef",
                "household_location_choice_model_with_sampled_coef",
                "employment_relocation_model_with_sampled_rr",
                {"employment_location_choice_model_with_sampled_coef":{'group_members': ['non_home_based']}},
                'distribute_unplaced_jobs_model',
                'distribute_unplaced_mining_utilities_jobs_model',
                'work_at_home_choice_model_with_sampled_coef',
                'workplace_relocation_choice_model_with_sampled_coef',
                'workplace_choice_model_for_resident_with_sampled_coef'
                ]

