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