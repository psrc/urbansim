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
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from psrc.configs.subset_configuration import SubsetConfiguration
from urbansim.flatten_scenario_database_chain import FlattenScenarioDatabaseChain

"""
This utility creates, on localhost, a flattened copy of the subset 
test database chain located on trondheim..
"""

run_configuration = SubsetConfiguration()
config = {
    'tables_to_copy':run_configuration['creating_baseyear_cache_configuration'].tables_to_cache,
    'from_host_name':'trondheim.cs.washington.edu',
    'from_database_name':run_configuration['input_configuration'].database_name,
    'from_user_name':os.environ['MYSQLUSERNAME'],
    'from_password':os.environ['MYSQLPASSWORD'],
    'to_host_name':'localhost',
    'to_database_name':run_configuration['input_configuration'].database_name,
    'to_user_name':os.environ['MYSQLUSERNAME'],
    'to_password':os.environ['MYSQLPASSWORD'],
    'mode':'python',
    }
copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(config)