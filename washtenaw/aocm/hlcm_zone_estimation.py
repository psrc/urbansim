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

from urbansim.configs.hlcm_estimation_config import run_configuration as config

run_configuration = config.copy()

run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sample_size_locations']=None
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]['sampler']=None#"'opus_core.samplers.weighted_sampler'"
#run_configuration["models_configuration"]["household_location_choice_model"]["init"]["arguments"]["estimate_config"] = {"weights_for_estimation_string":"urbansim.zone.vacant_residential_units"}
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["join_datasets"] = 'True'
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["prepare_for_estimate"]["arguments"]["index_to_unplace"] = 'None'

run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_set"] = "zone"
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["location_id_string"] = "'urbansim.household.zone_id'"
run_configuration["datasets_to_preload"].merge({'zone':{}})
run_configuration['models'] = [
    {'household_location_choice_model':['estimate']} ]

if __name__ == '__main__':
    from washtenaw.estimation.my_estimation_config import my_configuration
    from urbansim.estimation.estimator import Estimator
    from urbansim.estimation.estimator import update_controller_by_specification_from_module

    run_configuration = update_controller_by_specification_from_module(
                            run_configuration, "household_location_choice_model",
                            "washtenaw.aocm.hlcm_zone_specification")
    run_configuration.merge(my_configuration)
    estimator = Estimator(run_configuration, save_estimation_results=False)
    estimator.estimate()
