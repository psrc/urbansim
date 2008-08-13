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

from hlcm_estimation_config import estimation_configuration
from estimation_zone_config import run_configuration as config

run_configuration = config.copy()
run_configuration.merge(estimation_configuration)
#residential_price_model = {"real_estate_price_model": {"group_members": ["residential"]}}
#run_configuration["models"] = [residential_price_model] + \
#                               run_configuration["models"]
run_configuration["datasets_to_preload"] = {
        'gridcell': {},
        'job': {},
        'zone':{},
        'household':{},
        'building': {},
        'faz':{},
        }


#run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["init"]["arguments"]["sample_size_locations"] = 50