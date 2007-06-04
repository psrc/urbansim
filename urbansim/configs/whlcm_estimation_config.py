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

from urbansim.configs.estimation_base_config import run_configuration as config
"""estimation config for HLCM with worker specific accessibility"""

run_configuration = config.copy()

estimation_configuration = {}
estimation_configuration["models"] = [
    #{"land_price_model": ["run"]},                                      
    {"household_relocation_model": ["run"]},
    {"worker_specific_household_location_choice_model": ["estimate"]}
]

estimation_configuration["datasets_to_preload"] = {
        'gridcell':{},
        'household':{},
        'person':{'package_name':'psrc'}
        }

run_configuration.merge(estimation_configuration)

#add persons to tables_to_cache
run_configuration["creating_baseyear_cache_configuration"].tables_to_cache += ["persons"]

run_configuration["models_configuration"]["worker_specific_household_location_choice_model"] = \
    run_configuration["models_configuration"]["household_location_choice_model"].copy()
    
controller = run_configuration["models_configuration"]["worker_specific_household_location_choice_model"]["controller"]                              
controller["init"]["arguments"]["submodel_string"] = "'psrc.household.nonhome_based_workers_category'"
#the persons set must have all persons in both the households and households_for_estimation
controller["prepare_for_estimate"]["arguments"]["join_datasets"] = False  
run_configuration["models_configuration"]["worker_specific_household_location_choice_model"]["controller"].merge(controller)
