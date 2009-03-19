# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from hlcm_estimation_config import run_configuration as config

run_configuration = config.copy()
run_configuration["datasets_to_preload"] = {
        'parcel':{},
        'household':{}
        }

controller = run_configuration["models_configuration"]["household_location_choice_model"]["controller"]
controller["init"]["arguments"]["location_set"] = "parcel"
controller["init"]["arguments"]["estimate_config"] = \
            "{'weights_for_estimation_string': 'psrc.parcel.residential_units_when_has_eg_1_households_and_is_in_county_033'}"

run_configuration["models_configuration"]["household_location_choice_model"]["controller"].merge(controller)