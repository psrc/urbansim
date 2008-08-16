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

from washtenaw.configs.baseline import Baseline
from opus_core.database_management.flatten_scenario_database_chain \
    import FlattenScenarioDatabaseChain
from opus_core.database_management.database_server_configuration \
    import DatabaseServerConfiguration

"""
This utility creates a new flattened database containing the
necessary files from the scenario database chain pointed to by
the baseline washtenaw configuration.
"""

server_config = DatabaseServerConfiguration()

run_configuration = Baseline()
config = {
    'tables_to_copy':run_configuration['creating_baseyear_cache_configuration'].tables_to_cache,
    'db_server_config_from':server_config,
    'from_database_name':'wastenaw_baseyear',
    'db_server_config_to':server_config,
    'to_database_name':'washtenaw_flattened'
    }

copier = FlattenScenarioDatabaseChain()
copier.copy_scenario_database(**config)