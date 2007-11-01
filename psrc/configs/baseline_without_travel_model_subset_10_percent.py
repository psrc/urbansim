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

import os

from opus_core.database_management.database_configuration import DatabaseConfiguration
from psrc.configs.baseline_without_travel_model import run_configuration as config

run_configuration = config.copy()
run_configuration['input_configuration'] = DatabaseConfiguration(
    database_name = 'PSRC_2000_baseyear_sampled_10_percent',
    ),
run_configuration['datasets_to_cache_after_each_model'] = []