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

#from urbansim.estimation.config import config
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from opus_core.configuration import Configuration
from numpy import array
import os
from math import exp, log
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator

UNIT_PRICE_RANGE = (exp(3), exp(7))
class UrbansimParcelConfiguration(AbstractUrbansimConfiguration):
    def __init__(self):
        AbstractUrbansimConfiguration.__init__(self)
        models_configuration = self['models_configuration']
        
        if "home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["home_based_employment_location_choice_model"]
        if "non_home_based_employment_location_choice_model" in models_configuration:
            del models_configuration["non_home_based_employment_location_choice_model"]
        models_configuration["business_location_choice_model"] = {
                             "estimation":"opus_core.bhhh_mnl_estimation",
                             "sampler":"opus_core.samplers.weighted_sampler",
                             "sample_size_locations":30,
        #                     "weights_for_estimation_string":"urbansim.zone.number_of_non_home_based_jobs",
                             "specification_table":"business_location_choice_model_specification",
                             "coefficients_table":"business_location_choice_model_coefficients",
                             "compute_capacity_flag":True,
                             "capacity_string":"urbansim_parcel.building.building_sqft",
                             "number_of_agents_string":"business.sqft",
                             "number_of_units_string":"urbansim_parcel.building.vacant_building_sqft",
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
                              "dataset_pool": "dataset_pool"
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
                              "threshold": 1},
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
                                location_set = "building",
                                input_index = 'erm_index',
                                estimation_weight_string = "vacant_SSS_job_space",
                                agents_for_estimation_table = None, # will take standard jobs table 
                                #agents_for_estimation_table = "jobs_for_estimation",
                                estimation_size_agents = 0.1,
                                number_of_units_string = "total_SSS_job_space",
                                filter = "building.non_residential_sqft",
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
        
        # configuration for parcel-based developer model
         'expected_sale_price_model': {
            "import": {"urbansim_parcel.models.development_project_proposal_regression_model":
                       "DevelopmentProjectProposalRegressionModel"},
            "init": {
                "name": "DevelopmentProjectProposalRegressionModel",
                "arguments": {"submodel_string": "'land_use_type_id=development_project_proposal.disaggregate(parcel.land_use_type_id)'", 
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
                              "parcel_filter_for_redevelopment":"'low_improvement_ratio=urbansim_parcel.parcel.improvement_value / ( urbansim_parcel.parcel.unit_price * urbansim_parcel.parcel.existing_units ) < 0.1'",
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
        }
        
        for model in my_controller_configuration.keys():
            if model not in self["models_configuration"].keys():
                self["models_configuration"][model] = {}
            self['models_configuration'][model]['controller'] = my_controller_configuration[model]
        
        #settings for the HLCM
        hlcm_controller = self["models_configuration"]["household_location_choice_model"]["controller"]
        hlcm_controller["init"]["arguments"]["location_set"] = "building"
        hlcm_controller["init"]["arguments"]["location_id_string"] = "'building_id'"
        hlcm_controller["init"]["arguments"]["estimation_weight_string"] = "'urbansim_parcel.building.vacant_residential_units'"
        hlcm_controller["init"]["arguments"]["capacity_string"] = "'vacant_residential_units'"
        hlcm_controller["init"]["arguments"]['sample_size_locations']=30
        hlcm_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
        #hlcm_controller["init"]["arguments"]["submodel_string"] = "'urbansim.household.income_category'"
        hlcm_controller["init"]["arguments"]["estimation_size_agents"] = None
        #hlcm_controller["init"]["arguments"]["number_of_units_string"] = None
        hlcm_controller["init"]["arguments"]["variable_package"] = "'urbansim_parcel'"
        hlcm_controller["init"]["arguments"]["run_config"] = "{'lottery_max_iterations': 7}"
        hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(urbansim_parcel.building.is_residential, numpy.logical_and(numpy.logical_and(building.residential_units, building.sqft_per_unit), urbansim_parcel.building.unit_price > 0))'" 
#        hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(numpy.logical_and(building.residential_units, building.sqft_per_unit), numpy.logical_and(urbansim_parcel.building.unit_price > %s, urbansim_parcel.building.unit_price< %s))'" % (UNIT_PRICE_RANGE[0], UNIT_PRICE_RANGE[1])
        #hlcm_controller["init"]["arguments"]["filter"] = "'numpy.logical_and(building.residential_units, building.sqft_per_unit)'"
        hlcm_controller["init"]["arguments"]["estimate_config"] = "{'wesml_sampling_correction_variable':'psrc_parcel.building.wesml_sampling_correction_variable'}"
        hlcm_controller["prepare_for_estimate"]["arguments"]["agents_for_estimation_table"] = "'households_for_estimation'"
        hlcm_controller["prepare_for_estimate"]["arguments"]["filter"] = "'numpy.logical_and(household.building_id>0, household.disaggregate(building.sqft_per_unit>0))'" # filtering out agents for estimation with valid location
        hlcm_controller["run"]["arguments"]["chunk_specification"] ="{'records_per_chunk':50000}"
        hlcm_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = True
        hlcm_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = None
        # settng estimation procedure
        hlcm_controller["estimate"]["arguments"]["procedure"] = "'bhhh_wesml_mnl_estimation'"
        #hlcm_controller["estimate"]["arguments"]["procedure"] = "'bhhh_mnl_estimation'"
        
        models_configuration['household_location_choice_model']["controller"].replace(hlcm_controller)
                
        self["datasets_to_preload"] = {
                'zone':{},
                'household':{},
                'building':{},
                'parcel':{'package_name':'urbansim_parcel'},
                "building_type":{'package_name':'urbansim_parcel'},
                'travel_data':{}
                }
        
config = UrbansimParcelConfiguration()
