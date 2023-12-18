# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from math import exp, log
from numpy import array
from opus_core.configuration import Configuration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.distribute_unplaced_jobs_model_configuration_creator import DistributeUnplacedJobsModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator
import os, copy


UNIT_PRICE_RANGE = (exp(3), exp(7))
class UrbansimParcelConfiguration(AbstractUrbansimConfiguration):
    def __init__(self):
        AbstractUrbansimConfiguration.__init__(self)
        models_configuration = self['models_configuration']
        
        self['project_name'] = 'urbansim_parcel'
        ## employment_location_choice_model is defined for gridcells at urbansim package 
        if "home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["home_based_employment_location_choice_model"]
        if "non_home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["non_home_based_employment_location_choice_model"]
        models_configuration['workplace_choice_model_for_resident'] = {
                       "estimation":"opus_core.bhhh_mnl_estimation",
                       "sampler":"opus_core.samplers.weighted_sampler",
                       "sample_size_locations":30,
                       "weights_for_estimation_string":"is_placed_job=(urbansim_parcel.job.zone_id > 0).astype(int32)",
                       "compute_capacity_flag":True,
                       "capacity_string":"urbansim_parcel.job.is_untaken_non_home_based_job",
                       #"capacity_string":"(job.building_type==2).astype(int32)",  
                         ### each non home-based job can only be chosen once by one person
                       "number_of_units_string":"(job.building_type==2).astype(int32)",
                        'lottery_max_iterations': 10,
                        'number_of_agents_string': 'job.number_of_agents(person)',
#                       "sampler":"opus_core.samplers.stratified_sampler",
#                       "stratum":"district_id = job.disaggregate(psrc_parcel.building.district_id)",
#                       "sample_size_from_each_stratum": 5,
#                       "sample_size_from_chosen_stratum":4,
#                       "include_chosen_choice":True,
#                       "sample_size_locations":95,
#                       "weights_for_estimation_string":"is_placed_job=(urbansim_parcel.job.zone_id > 0).astype(int32)",
#                       "compute_capacity_flag":True,
#                       "capacity_string":"(job.building_type==2).astype(int32)",  
#                        ### each non home-based job can only be chosen once by one person
#                       "number_of_units_string":"(job.building_type==2).astype(int32)",

        }
        
        my_controller_configuration = {
         'real_estate_price_model': {
            "import": {"urbansim.models.real_estate_price_model":
                                                "RealEstatePriceModel"},
            "init": {
                "name": "RealEstatePriceModel",
                "arguments": {"submodel_string": "'land_use_type_id'",
                              "outcome_attribute": "'ln_unit_price=ln(urbansim_parcel.parcel.unit_price)'",
                              "filter_attribute": "'numpy.logical_or(urbansim_parcel.parcel.building_sqft, urbansim_parcel.parcel.is_land_use_type_vacant)'",
                              "dataset_pool": "dataset_pool",
                              "estimate_config": "{'save_predicted_values_and_errors':True}"
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                               "coefficients_storage": "base_cache_storage",
                               "coefficients_table": "'real_estate_price_model_coefficients'"},
                "output": "(specification, coefficients)"
                },
            "run": {
                "arguments": {
                              "specification": "specification",
                              "coefficients":"coefficients",
                              "dataset": "parcel",
                              "data_objects": "datasets",
                              "run_config": "Resources({'exclude_outliers_from_initial_error': True, 'outlier_is_less_than': %s, 'outlier_is_greater_than': %s})" % (log(UNIT_PRICE_RANGE[0]), log(UNIT_PRICE_RANGE[1]))
                              }
                    },
            "prepare_for_estimate": {
                "name": "prepare_for_estimate",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                              "filter_variable":"'numpy.logical_and(urbansim_parcel.parcel.unit_price>%s,urbansim_parcel.parcel.unit_price<%s, urbansim_parcel.parcel.existing_units>100)'" % (UNIT_PRICE_RANGE[0], UNIT_PRICE_RANGE[1]),
                              "dataset": "parcel",
                              "threshold": 0},
                "output": "(specification, index)"
                },
            "estimate": {
                "arguments": {
                              "specification": "specification",
                              "outcome_attribute": "'ln_unit_price=ln(urbansim_parcel.parcel.unit_price)'",
                              "dataset": "parcel",
                              "index": "index",
                              "data_objects": "datasets",
                              "debuglevel": 'debuglevel',
                              #'procedure': "'opus_core.bma_for_linear_regression_r'",
                              },
                "output": "(coefficients, dummy)"
                }
        
          },

         'employment_transition_model': 
                  EmploymentTransitionModelConfigurationCreator(
            location_id_name="building_id"
            ).execute(),
 
        'employment_relocation_model': 
                  EmploymentRelocationModelConfigurationCreator(
                               location_id_name = 'building_id',
                               output_index = 'erm_index').execute(),
                                       
         'employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                sample_size_locations = 60,
                                location_set = "building",
                                input_index = 'erm_index',
                                estimation_weight_string = None,
                                #agents_for_estimation_table = None, # will take standard jobs table 
                                agents_for_estimation_table = "jobs_for_estimation",
                                join_datasets = True,
                                #estimation_size_agents = 0.3,
                                number_of_units_string = "total_SSS_job_space",
                                filter = "building.non_residential_sqft>0",
                                filter_for_estimation = "numpy.logical_and(job.building_id>0, job.disaggregate(building.non_residential_sqft) > 0)",
                                #filter_for_estimation = "numpy.logical_and(job.building_id>0,job.join_flag<3)",
                                portion_to_unplace = 0,
                                capacity_string = "vacant_SSS_job_space",
                                variable_package = "urbansim_parcel",
                                lottery_max_iterations = 10
                                ).execute(),
                                       
            'home_based_employment_location_choice_model': 
                   EmploymentLocationChoiceModelConfigurationCreator(
                                location_set = "building",
                                input_index = 'erm_index',
                                estimation_weight_string = "vacant_home_based_job_space", #"pre_2001=building.year_built<=2000",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                estimation_size_agents = 0.4,
                                number_of_units_string = None,
                                filter = "numpy.logical_and(building.residential_units, building.sqft_per_unit)", 
                                filter_for_estimation = "numpy.logical_and(job.building_id>0, job.disaggregate(building.sqft_per_unit>0))",
                                portion_to_unplace = 0,
                                capacity_string = "vacant_home_based_job_space",
                                variable_package = "urbansim_parcel",
                                lottery_max_iterations = 7
                                ).execute(),
            'distribute_unplaced_jobs_model':  DistributeUnplacedJobsModelConfigurationCreator(
                                    location_set = 'building',
                                    filter = 'urbansim_parcel.building.is_governmental',
                                    agents_filter = 'urbansim.job.is_in_employment_sector_group_scalable_sectors'
                                                                                  ).execute(),
            'distribute_unplaced_mining_utilities_jobs_model':  DistributeUnplacedJobsModelConfigurationCreator(
                                    location_set = 'building',
                                    filter = None,
                                    agents_filter = 'numpy.logical_or(job.sector_id==1, job.sector_id==9)'
                                                                                  ).execute(),
            'governmental_employment_location_choice_model': 
                   GovernmentalEmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        location_set = 'building',
                        filter = 'urbansim_parcel.building.is_governmental'
                        ).execute(),                       
                "household_relocation_model" : {
                    "import": {"urbansim.models.household_relocation_model_creator":
                                    "HouseholdRelocationModelCreator"
                              },
                    "init": {
                        "name": "HouseholdRelocationModelCreator().get_model",
                        "arguments": {
                                      "debuglevel": 'debuglevel',
                                      "location_id_name": "'building_id'",
                                      },
                        },
                     "prepare_for_run": {
                         "name": "prepare_for_run",
                         "arguments": {"what": "'households'",  "rate_storage": "base_cache_storage",
                                           "rate_table": "'annual_relocation_rates_for_households'"},
                         "output": "hrm_resources"
                        },
                    "run": {
                        "arguments": {"agent_set": "household", "resources": "hrm_resources"},
                        "output": "hrm_index"
                        }
                    },
                    
        "process_pipeline_events":{
                     "import": {"urbansim_parcel.models.process_pipeline_events":
                                                         "ProcessPipelineEvents"},
                     "init": {
                        "name": "ProcessPipelineEvents"},
                     "run": {
                        "arguments": {'building_dataset': 'building',
                                      'year':'year',
                                      "storage": "base_cache_storage"},
                        "output": "scheduled_development_events"
                        }
                 },

        "tour_schedule_model":{
                     "import": {"urbansim_parcel.models.tour_schedule_model":
                                                         "TourScheduleModel"},
                     "init": {
                         "name": "TourScheduleModel"},
                     "run": {
                        "arguments": {'person_set': 'person',
                                      'tour_set': 'tour',
                                      'tour_filter': "'tour.w2h_act == 1'"
                                      },
                        "output": "sampled_tour"
                        }
                 },
                
        'household_transition_model': {
            'import': {
                'urbansim_parcel.models.household_transition_model': 'HouseholdTransitionModel'
                },
            'init': {
                'arguments': {'debuglevel': 'debuglevel'},
                'name': 'HouseholdTransitionModel'
                },
            'prepare_for_run': {
                'arguments': {'storage': 'base_cache_storage'},
                'name': 'prepare_for_run',
                'output': '(control_totals, characteristics)'
                },
            'run': {
                'arguments': {
                    'characteristics': 'characteristics',
                    'control_totals': 'control_totals',
                    'person_set': 'person',
                    'household_set': 'household',
                    'year': 'year'
                    }
                }
            },
            
        # configuration for parcel-based developer model
         'expected_sale_price_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_regression_model":
                       "DevelopmentProjectProposalRegressionModel"},
            "init": {
                "name": "DevelopmentProjectProposalRegressionModel",
                "arguments": {"submodel_string": "'land_use_type_id=development_project_proposal.disaggregate(development_template.land_use_type_id)'", 
                              #"submodel_string": "'building_type_id=development_project_proposal.disaggregate(development_template.building_type_id)'", 
                              #"filter_attribute": "'urbansim_parcel.development_project_proposal.is_viable'",
                              "filter_attribute": "'urbansim_parcel.development_project_proposal.is_size_fit'",
                              "outcome_attribute_name":"'ln_unit_price_expected'",
                              "dataset_pool": "dataset_pool"
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"parcel_filter_for_new_development":"'has_vacant_land=urbansim_parcel.parcel.vacant_land_area > 0'",
                              "parcel_filter_for_redevelopment":"'low_improvement_ratio_of_parcels_with_bldg=(parcel.number_of_agents(building)>0)*(urbansim_parcel.parcel.improvement_value / ( urbansim_parcel.parcel.unit_price * urbansim_parcel.parcel.existing_units ) < 0.1)*(parcel.aggregate(urbansim_parcel.building.age_masked, function=mean)>30)'",
                              "template_filter":"'development_template.is_active > 0'",
                              "specification_storage": "base_cache_storage",
                              "specification_table": "'real_estate_price_model_specification'",
                               "coefficients_storage": "base_cache_storage",
                               "coefficients_table": "'real_estate_price_model_coefficients'",
                               "spec_replace_module_variable_pair": "('psrc_parcel.estimation.repm_specification', 'variables_for_development_project_proposal')",
                               "dataset_pool": "dataset_pool",},
                "output": "(development_project_proposal, specification, coefficients)"
                },
            "run": {
                "arguments": {
                              "specification": "specification",
                              "coefficients":"coefficients",
                              "dataset": 'development_project_proposal',  
                              "data_objects": "datasets" },
                "output":"development_project_proposal"  #get the development project proposal back
                    },
          },

         'development_proposal_choice_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_sampling_model":
                       "DevelopmentProjectProposalSamplingModel"},
            "init": {
                "name": "DevelopmentProjectProposalSamplingModel",
                "arguments": {"proposal_set": "development_project_proposal",
                              #weight_string omitted to use defalut value "exp_ROI = exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",                      
                              "filter_attribute": None, # the filter has been handled in the process of creating proposal set 
                                                        # (prepare_for_run in expected_sale_price_model)
                              },
                },
            "run": {
                "arguments": {'n':500,  # sample 500 proposal at a time, evaluate them one by one
                              },
                "output":"(development_project_proposal, demolished_buildings)"
                    },
          },
         
         'development_project_proposal_choice_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_choice_model":
                       "DevelopmentProjectProposalChoiceModel"},
            "init": {
                "name": "DevelopmentProjectProposalChoiceModel",
                "arguments": {"proposal_set": "development_project_proposal",
                              #weight_string omitted to use defalut value "exp_ROI = exp(urbansim_parcel.development_project_proposal.expected_rate_of_return_on_investment)",
                              "filter": "'development_project_proposal.status_id==4'"  # id_tentative
                              },
                },            
            "prepare_for_run":{                
                "name": "prepare_for_run",
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'development_project_proposal_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table':"'development_project_proposal_choice_model_specification'",
                    },
                'output': '(specification, coefficients)'
                },
            "run": {
                "arguments": {
                    'n':500,  # sample 500 proposal at a time, evaluate them one by one
                    "specification": "specification",
                    "coefficients":"coefficients",
                    #"agent_set": 'development_project_proposal',

                              },
                "output":"(development_project_proposal, demolished_buildings)"
                    },
            "prepare_for_estimate": {
                 "name": "prepare_for_estimate",                                      
                 "arguments": {
                     "agent_set":"development_project_proposal",
                     "agents_for_estimation_storage": "base_cache_storage",
                     "agents_for_estimation_table": "'development_project_proposals_for_estimation'",
                     "filter_for_estimation_set":None,
                     "data_objects": "datasets"
                     },
                 "output": "(specification, index)"
                 },
            'estimate': {
                'arguments': {
                    'agent_set': 'development_project_proposal',
                    'agents_index':'index',
                    'data_objects': 'datasets',
                    'debuglevel': 0,
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                 },
            },
                                       
         'building_construction_model': {
             "import": {"urbansim_parcel.models.building_construction_model":
                       "BuildingConstructionModel"},
             "init": {
                "name": "BuildingConstructionModel"
                },
             "run": {
                "arguments": {
                   "development_proposal_set": "development_project_proposal",
                   "building_dataset": "building",
                   "dataset_pool": "dataset_pool",
                   "buildings_to_be_demolished": "demolished_buildings"
                   }
                 }
          },
         
       # models related to workplace_choice_model
#        'household_person_consistency_keeper':{
#            "import": {"urbansim_parcel.models.persons_consistency_keeper_model":"PersonDatasetConsistencyKeeperModel"},
#            "init": { 
#                "name": "PersonDatasetConsistencyKeeperModel",
#                "arguments": {},
#                },
#            "run": {
#                "arguments": {"household_set": "household",
#                              "person_set":"person",
#                              "expand_person_set":True,
#                          }
#                },
#            },
         'job_person_consistency_keeper':{
             "import": {"urbansim_parcel.models.persons_consistency_keeper_model":"PersonDatasetConsistencyKeeperModel"},
             "init": { 
                 "name": "PersonDatasetConsistencyKeeperModel",
                 "arguments": {},
                 },                                  
             "run": {
                 "arguments": {"job_set": "job",
                               "person_set":"person",
                               "expand_person_set":False,
                           }
                 },
             },
             
         'workplace_choice_model_for_resident': {
             "import": {"urbansim_parcel.models.workplace_choice_model":"WorkplaceChoiceModel"},
             "init": { 
                 "name": "WorkplaceChoiceModel",
                 "arguments": {
                     "location_set":"job",
                     "model_name":"'Non-home-based Workplace Choice Model for residents'",
                     "short_name":"'NHBWCM'",
                     "choices":"'urbansim.lottery_choices'",
                     "submodel_string":None, #"'psrc.person.household_income'",
                     "filter": "'urbansim_parcel.job.is_untaken_non_home_based_job'",
                     "location_id_string":"'job_id'",
                     "run_config":models_configuration['workplace_choice_model_for_resident'],
                     "estimate_config":models_configuration['workplace_choice_model_for_resident']
                     }},
             "prepare_for_run": {
                 "name": "prepare_for_run",
                 "arguments": {"specification_storage": "base_cache_storage", #"models_configuration['specification_storage']",
                               "specification_table": "'workplace_choice_model_for_resident_specification'",
                               "coefficients_storage": "base_cache_storage", #"models_configuration['coefficients_storage']",
                               "coefficients_table": "'workplace_choice_model_for_resident_coefficients'",
                               },
                 "output": "(specification, coefficients)"
                 },
             "run": {
                 "arguments": {"specification": "specification",
                               "coefficients":"coefficients",
                               "agent_set": "person",
                               "agents_index": None,
                               "agents_filter":"'urbansim_parcel.person.is_non_home_based_worker_without_job'",
                               "data_objects": "datasets",
                               "chunk_specification":"{'records_per_chunk':50000}",
                               "debuglevel": 'debuglevel',
                               },
                 },
             
             # the estimate method is not available before the estimation data is ready
             "prepare_for_estimate": {
                 "name": "prepare_for_estimate",                                      
                 "arguments": {
                     "agent_set":"person",
                     "household_set": "household",
                     "join_datasets": "True",
                     "agents_for_estimation_storage": "base_cache_storage",
                     "agents_for_estimation_table": "'persons_for_estimation'",
                     "households_for_estimation_table":"'households_for_estimation'",
                     "filter":"'urbansim_parcel.person.is_non_home_based_worker_with_job'",
                     "data_objects": "datasets"
                     },
                 "output": "(specification, workers_index)"
                 },
             "estimate": {
                 "arguments": {
                     "specification": "specification",
                     "agent_set": "person",
                     "agents_index": "workers_index",
                     "data_objects": "datasets",
                     "debuglevel": 'debuglevel',
                     },  
                 "output": "(coefficients, dummy)"                     
                 },
             },
         'work_at_home_choice_model': {
            'import': {
                'urbansim_parcel.models.work_at_home_choice_model': 'WorkAtHomeChoiceModel'
                },
            'init': {
                'arguments': {
                    'choice_set': 'job',
                    'filter': "'urbansim_parcel.job.is_untaken_home_based_job'",
                    },
                'name': 'WorkAtHomeChoiceModel'
                },
            'prepare_for_run': {
                "name": "prepare_for_run",
                'arguments': {
                    'coefficients_storage': 'base_cache_storage',
                    'coefficients_table': "'work_at_home_choice_model_coefficients'",
                    'specification_storage': 'base_cache_storage',
                    'specification_table': "'work_at_home_choice_model_specification'",
                    'agent_set': 'person',
                    'agents_filter': "'urbansim_parcel.person.is_worker_without_job'",
                    'data_objects': 'datasets'
                    },
                'output': '(specification, coefficients, _index)'
                },
            'run': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_index' : '_index',
                    'choose_job_only_in_residence_zone': False,
                    'chunk_specification': "{'nchunks':1}",
                    'coefficients': 'coefficients',
                    'data_objects': 'datasets',
                    'specification': 'specification'
                    }
                },                
             "prepare_for_estimate": {
                 "name": "prepare_for_estimate",                                      
                 "arguments": {
                     "agent_set":"person",
                     "household_set": "household",
                     "join_datasets": "True",
                     "agents_for_estimation_storage": "base_cache_storage",
                     "agents_for_estimation_table": "'persons_for_estimation'",
                     "households_for_estimation_table":"'households_for_estimation'",
                     "filter":"'urbansim_parcel.person.is_worker'",
                     "data_objects": "datasets"
                     },
                 "output": "(specification, agents_index)"
                 },
            'estimate': {
                'arguments': {
                    'agent_set': 'person',
                    'agents_index': 'agents_index',
                    'data_objects': 'datasets',
                    'debuglevel': 0,
                    'procedure': "'opus_core.bhhh_mnl_estimation'",
                    'specification': 'specification'
                    },
                'output': '(coefficients, _)'
                 },
            },
             
#         "job_change_model":{
#             "import": {"urbansim.models.agent_relocation_model":
#                        "AgentRelocationModel"
#                        },         
#             "init": {
#                 "name": "AgentRelocationModel",
#                 "arguments": {"choices":"opus_core.random_choices",
#                               "probabilities":"psrc.job_change_probabilities",
#                               "location_id_name":"job_id",
#                               "model_name":"job change model",
#                               "debuglevel": 'debuglevel',
#                               },
#                 },
#             "prepare_for_run": {
#                 "name": "prepare_for_run",
#                 "arguments": {"what": "'person'",  "rate_storage": "base_cache_storage",
#                               "rate_table": "'annual_job_change_rates_for_workers'"},
#                 "output": "jcm_resources"
#                 },
#             "run": {
#                 "arguments": {"agent_set": "person", "resources": "jcm_resources"},
#                 "output": "jcm_index"
#                 }
#             },

        'modify_workers_jobs_after_moving_households': {
            "import": {"opus_core.join_attribute_modification_model": "JoinAttributeModificationModel"},
            "init": {"name": "JoinAttributeModificationModel"},
            "run": {"arguments": {
                          "dataset": "person",
                          "secondary_dataset": "household",
                          #"index": "hrm_index", # this must be the same that goes into the HLCM argument 'agents_index'
                          "attribute_to_be_modified": "'job_id'",
                          "value": -1,
                          "filter": "'household.building_id <> urbansim.household.building_id_lag1'"
                                  }
                                                 },
                            },
                            
        'modify_workers_jobs_after_moving_jobs': {
            "import": {"opus_core.join_attribute_modification_model": "JoinAttributeModificationModel"},
            "init": {"name": "JoinAttributeModificationModel"},
            "run": {"arguments": {
                          "dataset": "person",
                          "secondary_dataset": "job",
                          #"index": "erm_index", # this must be the same that goes into the ELCM argument 'agents_index'
                          "attribute_to_be_modified": "'job_id'",
                          "value": -1,
                          "filter": "'job.building_id <> urbansim.job.building_id_lag1'"
                                  }
                                                 },
                            },
                            

         'water_demand_model': {
            "import": {"psrc_parcel.models.water_demand_model":"WaterDemandModel"},
            "init": {
                "name": "WaterDemandModel",
                "arguments": {"submodel_string": "'land_use_type_id'",
                              "outcome_attribute": "'ln_month_combination_2'",
                              "filter_attribute": None,
                              "dataset_pool": "dataset_pool",
                              },
                },
            "prepare_for_run": {
                "name": "prepare_for_run",
                "arguments": {"specification_storage": "base_cache_storage",
                              "specification_table": "'water_demand_model_specification_for_month_combination_2'",
                               "coefficients_storage": "base_cache_storage",
                               "coefficients_table": "'water_demand_model_coefficients_for_month_combination_2'"},
                "output": "(specification, coefficients, _)"
                },
            "run": {
                "arguments": {
                              "specification": "specification",
                              "coefficients":"coefficients",
                              "dataset": "parcel",
                              "data_objects": "datasets",
                }
                },
            },
         }
        
        for month in range(2, 13, 2):
            month_string = "month_combination_" + str(month)
            my_controller_configuration['water_demand_model_for_' + month_string] = copy.deepcopy(my_controller_configuration['water_demand_model'])
            my_controller_configuration['water_demand_model_for_' + month_string]['init']['arguments']['outcome_attribute'] = "'%s'" % month_string
            my_controller_configuration['water_demand_model_for_' + month_string]['prepare_for_run']['arguments']['specification_table'] = "'water_demand_model_specification_for_%s'" % month_string
            my_controller_configuration['water_demand_model_for_' + month_string]['prepare_for_run']['arguments']['coefficients_table'] = "'water_demand_model_coefficients_for_%s'" % month_string
        
        my_controller_configuration["workplace_choice_model_for_immigrant"] = copy.deepcopy(my_controller_configuration["workplace_choice_model_for_resident"])
        my_controller_configuration["workplace_choice_model_for_immigrant"]["init"]["arguments"]["model_name"] = "'Non-home-based Workplace Choice Model for immigrants'"
        my_controller_configuration["workplace_choice_model_for_immigrant"]["prepare_for_run"]["arguments"]["specification_table"] = "'workplace_choice_model_for_immigrant_specification'"
        my_controller_configuration["workplace_choice_model_for_immigrant"]["prepare_for_run"]["arguments"]["coefficients_table"] = "'workplace_choice_model_for_immigrant_coefficients'"
        my_controller_configuration["workplace_choice_model_for_immigrant"]["run"]["arguments"]["agents_filter"] = "'psrc.person.is_immigrant_worker_without_job'"        
        
        for model in list(my_controller_configuration.keys()):
            if model not in list(self["models_configuration"].keys()):
                self["models_configuration"][model] = {}
            self['models_configuration'][model]['controller'] = my_controller_configuration[model]
        
        #settings for the HLCM
        hlcm_controller = self["models_configuration"]["household_location_choice_model"]["controller"]
        hlcm_controller["init"]["arguments"]["location_set"] = "building"
        hlcm_controller["init"]["arguments"]["location_id_string"] = "'building_id'"
        hlcm_controller["init"]["arguments"]["estimation_weight_string"] = "'urbansim_parcel.building.vacant_residential_units'"
        hlcm_controller["init"]["arguments"]["simulation_weight_string"] = "'has_vacant_units=urbansim_parcel.building.vacant_residential_units>0'"
        hlcm_controller["init"]["arguments"]["capacity_string"] = "'urbansim_parcel.building.vacant_residential_units'"
        #hlcm_controller["init"]["arguments"]["estimation_weight_string"] = "'has_eg_1_units=building.residential_units>=1'"
        #hlcm_controller["init"]["arguments"]["capacity_string"] = "'has_eg_1_units=building.residential_units>=1'"
        hlcm_controller["init"]["arguments"]['sample_size_locations']=30
        hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
        #hlcm_controller["init"]["arguments"]["submodel_string"] = "'urbansim.household.income_category'"
        hlcm_controller["init"]["arguments"]["estimation_size_agents"] = None
        #hlcm_controller["init"]["arguments"]["number_of_units_string"] = None
        hlcm_controller["init"]["arguments"]["variable_package"] = "'urbansim_parcel'"
        hlcm_controller["init"]["arguments"]["run_config"] = "{'lottery_max_iterations': 7}"
        hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(urbansim_parcel.building.is_residential, numpy.logical_and(numpy.logical_and(building.residential_units, building.sqft_per_unit), urbansim_parcel.building.unit_price > 0))'" 
        #hlcm_controller["init"]["arguments"]["filter"] = "'urbansim_parcel.building.is_residential'" 
#        hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(numpy.logical_and(building.residential_units, building.sqft_per_unit), numpy.logical_and(urbansim_parcel.building.unit_price > %s, urbansim_parcel.building.unit_price< %s))'" % (UNIT_PRICE_RANGE[0], UNIT_PRICE_RANGE[1])
        #hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(building.residential_units, building.sqft_per_unit)'"
        hlcm_controller["init"]["arguments"]["estimate_config"] = "{'wesml_sampling_correction_variable':'psrc_parcel.building.wesml_sampling_correction_variable'}"
        hlcm_controller["prepare_for_estimate"]["arguments"]["agents_for_estimation_table"] = "'households_for_estimation'"
        hlcm_controller["prepare_for_estimate"]["arguments"]["filter"] = "'numpy.logical_and(household.building_id>1, household.disaggregate(building.sqft_per_unit>0)) * household.move'" # filtering out agents for estimation with valid location
        #hlcm_controller["prepare_for_estimate"]["arguments"]["filter"] = "'household.move==1'" # filtering out agents for estimation with valid location
        hlcm_controller["run"]["arguments"]["chunk_specification"] ="{'records_per_chunk':50000}"
        hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = True
        hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'hrm_index'  #None
        # settng estimation procedure
        #hlcm_controller["estimate"]["arguments"]["procedure"] = "'bhhh_wesml_mnl_estimation'"
        hlcm_controller["estimate"]["arguments"]["procedure"] = "'bhhh_mnl_estimation'"
        
        models_configuration['household_location_choice_model']["controller"].replace(hlcm_controller)
                
        self["datasets_to_preload"] = {
                'zone':{},
                'household':{},
                'building':{},
                'parcel':{'package_name':'urbansim_parcel'},
                "building_type":{'package_name':'urbansim_parcel'},
                'travel_data':{}
                }
        models_configuration['governmental_employment_location_choice_model']['controller']['import'] =  {
           'urbansim_parcel.models.scaling_jobs_model': 'ScalingJobsModel'}
        models_configuration['distribute_unplaced_jobs_model']['controller']['import'] =  {
           'urbansim_parcel.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'}
        models_configuration['distribute_unplaced_mining_utilities_jobs_model']['controller']['import'] =  {
           'urbansim_parcel.models.distribute_unplaced_jobs_model': 'DistributeUnplacedJobsModel'}
        models_configuration['real_estate_price_model_for_all_parcels'] = Configuration(models_configuration['real_estate_price_model'])
        models_configuration['real_estate_price_model_for_all_parcels']['controller']['init']['arguments']['filter_attribute'] = None

config = UrbansimParcelConfiguration()
