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
from psrc.configs.baseline import Baseline
from urbansim.flatten_scenario_database_chain import FlattenScenarioDatabaseChain

"""
This utility creates a new flattened database containing the
necessary files from the scenario database chain pointed to by
PSRC_2000_baseyear.
"""

run_configuration = Baseline()
config = {
    'tables_to_copy':run_configuration['creating_baseyear_cache_configuration'].tables_to_cache,
    'from_host_name':'trondheim.cs.washington.edu',
    'from_database_name':'PSRC_2000_baseyear',
    'from_user_name':os.environ['MYSQLUSERNAME'],
    'from_password':os.environ['MYSQLPASSWORD'],
    'to_host_name':'trondheim.cs.washington.edu',
    'to_database_name':'PSRC_2000_baseyear_flattened',
    'to_user_name':os.environ['MYSQLUSERNAME'],
    'to_password':os.environ['MYSQLPASSWORD'],
    'mode':'sql',
    }
copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(config)