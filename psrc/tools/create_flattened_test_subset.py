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

from psrc.configs.subset_configuration import SubsetConfiguration
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.database_server_configuration \
    import DatabaseServerConfiguration

"""
This utility creates, on localhost, a flattened copy of the subset 
test database chain located on trondheim..
"""
server_config_to = DatabaseServerConfiguration(host_name = 'localhost')
server_config_from = DatabaseServerConfiguration()

run_configuration = SubsetConfiguration()
config = {
    'tables_to_copy':run_configuration['creating_baseyear_cache_configuration'].tables_to_cache,
    'db_server_config_from':server_config_from,
    'from_database_name':run_configuration['input_configuration'].database_name,
    'db_server_config_to':server_config_to,
    'to_database_name':run_configuration['input_configuration'].database_name,
    }
copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(**config)