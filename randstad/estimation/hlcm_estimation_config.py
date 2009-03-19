# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from randstad.run_config.randstad_baseline import run_configuration as config
from urbansim.configs.hlcm_estimation_config import run_configuration as hlcm_estimation_config

run_configuration = config.copy()
run_configuration['models'] = [
#    {'housing_price_model':['run']},
#    {'household_relocation_model':['run']},                               
    {'household_location_choice_model':['estimate']} ]

my_controller = hlcm_estimation_config["models_configuration"]["household_location_choice_model"]["controller"]
my_controller["init"]["arguments"]['sample_size_locations']=30
my_controller["init"]["arguments"]['sampler']="'opus_core.samplers.weighted_sampler'"
my_controller["controller"]["init"]["arguments"]["submodel_string"] = "'incomecat'"
my_controller["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
my_controller["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'

run_configuration["models_configuration"]['household_location_choice_model']["controller"].merge(my_controller)
